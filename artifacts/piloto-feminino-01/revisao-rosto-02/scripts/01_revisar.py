import bpy, math, json, hashlib, bmesh, shutil
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
from mathutils.kdtree import KDTree

PARENT=Path(r'C:\Users\xandao\Documents\GitHub\3DC\artifacts\piloto-feminino-01')
OUT=PARENT/'revisao-rosto-02'
for p in [OUT/'imagens',OUT/'verificacao']:p.mkdir(parents=True,exist_ok=True)
if 'RCL_R02_ANTES' in bpy.data.scenes:raise RuntimeError('Revision already exists')
oldfiles=['piloto-feminino-01.blend','base-feminina-01.glb','corte-feminino-01.glb','montagem-feminina-01.glb']
oldhash={n:hashlib.sha256((PARENT/n).read_bytes()).hexdigest() for n in oldfiles}
# Append the saved baseline, leaving the live user's scenes and unsaved changes alone.
baseline=OUT/'anterior-preservado.blend'
if not baseline.exists():shutil.copy2(PARENT/oldfiles[0],baseline)
assert hashlib.sha256(baseline.read_bytes()).hexdigest()==oldhash[oldfiles[0]]
with bpy.data.libraries.load(str(baseline),link=False) as (src,dst):
    dst.scenes=['RCL_Piloto_Feminino_01']
before=dst.scenes[0];before.name='RCL_R02_ANTES'
after=before.copy();after.name='RCL_R02_DEPOIS'
for c in list(after.collection.children):after.collection.children.unlink(c)
for o in list(after.collection.objects):after.collection.objects.unlink(o)
objects={}
for old in before.objects:
    o=old.copy()
    if old.type in {'MESH','CAMERA'}:o.data=old.data.copy()
    after.collection.objects.link(o);objects[old]=o
for old,o in objects.items():
    if old.parent:o.parent=objects.get(old.parent,old.parent)
after.camera=objects[before.camera]
base0=next(o for o in before.objects if o.get('module_id')=='base-f-01')
hair0=next(o for o in before.objects if o.get('module_id')=='hair-f-01')
base=objects[base0];hair=objects[hair0]
base.name='Base_Feminina_01_R02';hair.name='Corte_Feminino_01_Preservado'
base.data.name='BaseF01_Revisao_Rosto_Editavel'
original=[v.co.copy() for v in base.data.vertices]
def smooth(a,b,x):
    t=max(0,min(1,(x-a)/(b-a)));return t*t*(3-2*t)
def interp(table,z):
    for (a,x),(b,y) in zip(table,table[1:]):
        if a<=z<=b:
            t=smooth(a,b,z);return x+(y-x)*t
    return table[0][1] if z<table[0][0] else table[-1][1]
groupids={g.name:g.index for g in base.vertex_groups}
fixedids={groupids[n] for n in ['COURO_CABELUDO','INTERFACE_ORBITAL_L_PROVISORIA','INTERFACE_ORBITAL_R_PROVISORIA','INTERFACE_NASAL_PROVISORIA','CORTE_PESCOCO_PROVISORIO']}
fixed={v.index for v in base.data.vertices if any(g.group in fixedids and g.weight>0 for g in v.groups)}
fixed.update(i for i,p in enumerate(original) if p.z>=.150)
kd=KDTree(len(fixed))
for i,j in enumerate(sorted(fixed)):kd.insert(original[j],i)
kd.balance()
bpy.context.window.scene=before;bpy.context.view_layer.update()
hbvh=BVHTree.FromObject(hair0,bpy.context.evaluated_depsgraph_get())
chin0=original[base['chin_vertex_index']].z
crown0=original[base['crown_vertex_index']].z
lower_height=.175-chin0
params={
 'lower_face_height_reduction_ratio':.1272727273,
 'chin_raise_m':lower_height*.1272727273,
 'width_factors_by_original_z_m':[[0,1],[.012,1.04],[.035,1.16],[.052,1.19],[.065,1.24],[.085,1.18],[.102,1.10],[.122,1.055],[.140,1.015],[.150,1]],
 'neck_front_fill_m':.004,'chin_depth_reduction_m':.002,
 'protected_boundary_blend_m':.010,'hair_freeze_distance_m':.006,'hair_blend_distance_m':.018,
 'scale_policy':'metres; previous 0.24 m is a provisional reference, no global scaling or height enforcement',
 'reference_ids':['R076','R088','R049','R052']}
weights=[]
for i,v in enumerate(base.data.vertices):
    p=original[i];x,y,z=p
    distance=hbvh.find_nearest(p)[3]
    w=0 if i in fixed else smooth(0,.010,kd.find(p)[2])*smooth(.006,.018,distance)
    # The nape and posterior cranium stay fixed; the low neck can become less pinched.
    face=1-smooth(-.025,.032,y)
    neck=1-smooth(.058,.085,z)
    region=max(face,neck)
    w*=region
    factor=interp(params['width_factors_by_original_z_m'],z)
    dz=params['chin_raise_m']*smooth(.018,.065,z)*(1-smooth(.065,.150,z))*w
    dx=x*(factor-1)*w
    throat=smooth(.005,.035,z)*(1-smooth(.052,.089,z))*(1-smooth(-.005,.035,y))
    chin=smooth(.052,.065,z)*(1-smooth(.065,.110,z))*(1-smooth(-.045,-.020,y))
    dy=(-params['neck_front_fill_m']*throat+params['chin_depth_reduction_m']*chin)*w
    v.co=p+Vector((dx,dy,dz));weights.append(w)
base.data.update()
base['revision']='p01-rosto-r02'
base['head_height_m']=base.data.vertices[base['crown_vertex_index']].co.z-base.data.vertices[base['chin_vertex_index']].co.z
base['scale_status']='0.24 m provisional; local silhouette correction, no global rescaling'
base['revision_parameters']='verificacao/parametros_e_preservacao.json'
root=base.parent
root['head_height_m']=base['head_height_m'];root['chin_z_m']=base.data.vertices[base['chin_vertex_index']].co.z
root['contract']='RCL-head-pilot-0.3'
vg=base.vertex_groups.new(name='REV02_INFLUENCIA_ROSTO_PESCOCO')
for i,w in enumerate(weights):
    if w>0:vg.add([i],w,'REPLACE')
bpy.context.window.scene=after;bpy.context.view_layer.update()
deps=bpy.context.evaluated_depsgraph_get()
intersections=len(BVHTree.FromObject(base,deps).overlap(BVHTree.FromObject(hair,deps)))
changes=[(v.co-original[v.index]).length for v in base.data.vertices]
report={'parameters':params,'original_file_sha256':oldhash,
 'vertices_changed':sum(d>1e-8 for d in changes),'max_displacement_m':max(changes),
 'protected_vertex_count':len(fixed),'protected_max_displacement_m':max(changes[i] for i in fixed),
 'hair_vertices_exactly_equal':all(tuple(a.co)==tuple(b.co) for a,b in zip(hair0.data.vertices,hair.data.vertices)),
 'hair_transform_exactly_equal':hair0.matrix_world==hair.matrix_world,
 'hair_topology_equal':[(tuple(p.vertices),p.material_index) for p in hair0.data.polygons]==[(tuple(p.vertices),p.material_index) for p in hair.data.polygons],
 'base_hair_triangle_intersections':intersections,
 'measurements':{'before_head_height_m':crown0-chin0,'after_head_height_m':base['head_height_m'],'before_chin_z_m':chin0,'after_chin_z_m':base.data.vertices[base['chin_vertex_index']].co.z,'crown_z_m':crown0},
 'landmarks':[]}
for z in [.035,.065,.085,.102,.122,.143]:
    # Comparable original ring locations: lateral front 45 degrees, central front and side.
    for angle,name in [(0,'frente'),(math.pi/4,'diagonal'),(math.pi/2,'lateral')]:
        candidates=[(abs(p.z-z),i) for i,p in enumerate(original) if (abs(math.atan2(p.x,-p.y)-angle)<.09)]
        if candidates:
            _,i=min(candidates)
            report['landmarks'].append({'original_z_target':z,'position':name,'vertex':i,'before':list(original[i]),'after':list(base.data.vertices[i].co)})
bm=bmesh.new();bm.from_mesh(base.data)
report['base_topology']={'boundary_edges':sum(e.is_boundary for e in bm.edges),'non_manifold_edges':sum(not e.is_manifold for e in bm.edges)};bm.free()
assert report['protected_max_displacement_m']==0
assert report['hair_vertices_exactly_equal'] and report['hair_transform_exactly_equal'] and report['hair_topology_equal']
assert intersections==0, str(intersections)+' intersections; do not deliver'
(OUT/'verificacao/parametros_e_preservacao.json').write_text(json.dumps(report,indent=2,ensure_ascii=False),encoding='utf-8')
before['revision_role']='saved original baseline, unchanged geometry'
after['revision_role']='lower face and neck only, hair and scalp fixed'
after['revision_directory']=str(OUT)
bpy.data.libraries.write(str(OUT/'piloto-feminino-01-rosto-r02.blend'),{before,after},fake_user=True)
print(json.dumps({k:v for k,v in report.items() if k not in ['landmarks','original_file_sha256','parameters']},indent=2))
