import bpy,bmesh,json,hashlib,shutil
from pathlib import Path
from collections import Counter
from mathutils import Vector
from mathutils.bvhtree import BVHTree
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'artifacts/conjunto-feminino-v1';PUBLIC=ROOT/'public/models/rcl-feminino-v1'
PUBLIC.mkdir(parents=True,exist_ok=True)
(OUT/'montagens').mkdir(exist_ok=True)
scene=bpy.data.scenes['RCL_Cinco_Bases_Cabelo_Unico'];bpy.context.window.scene=scene
bases=sorted([o for o in scene.objects if str(o.get('module_id','')).startswith('base-f-')],key=lambda o:o['module_id'])
assert len(bases)==5
hair=next(o for o in scene.objects if o.get('module_id')=='hair-f-01');root=hair.parent
for k in ['head_height_m','chin_z_m']:
    if k in root:del root[k]
def select(objs):
    bpy.context.window.scene=scene
    for o in scene.objects:o.hide_set(False);o.select_set(False)
    for o in objs:o.select_set(True);o.hide_render=False
    bpy.context.view_layer.objects.active=objs[-1]
def export(path,objs):
    select([root,*objs])
    bpy.ops.export_scene.gltf(filepath=str(path),export_format='GLB',use_selection=True,use_active_scene=True,
        export_extras=True,export_yup=True,export_apply=False,export_materials='EXPORT',export_normals=True,
        export_animations=False,export_cameras=False,export_lights=False)
def points(o):return [o.matrix_world@v.co for v in o.data.vertices]
def triangles(o):
    o.data.calc_loop_triangles();p=points(o)
    return Counter(tuple(sorted(tuple(round(n,6) for n in p[i]) for i in t.vertices)) for t in o.data.loop_triangles)
def materials(o):
    out=[]
    for m in o.data.materials:
        p=next(n for n in m.node_tree.nodes if n.type=='BSDF_PRINCIPLED')
        out.append([*[round(v,6) for v in p.inputs['Base Color'].default_value],round(p.inputs['Roughness'].default_value,6),round(p.inputs['Metallic'].default_value,6)])
    return out
def bvh(o):return BVHTree.FromPolygons(points(o),[list(p.vertices) for p in o.data.polygons])
def imported(s,paths):
    bpy.context.window.scene=s
    for path in paths:bpy.ops.import_scene.gltf(filepath=str(path),import_shading='NORMALS',merge_vertices=False)
    bpy.context.view_layer.update()
    ms=[o for o in s.objects if o.type=='MESH'];assert len(ms)==2
    assert len({o.get('module_id') for o in ms})==2
    return {o['module_id']:o for o in ms}
hairfile='corte-feminino-01.glb';export(PUBLIC/hairfile,[hair])
report={'bases':[],'common_scalp_equal':True,'single_hair_file':hairfile}
scalp=next(g.index for g in bases[0].vertex_groups if g.name=='COURO_CABELUDO')
fixed=[v.index for v in bases[0].data.vertices if any(g.group==scalp for g in v.groups)]
report['common_scalp_equal']=all(tuple(b.data.vertices[i].co)==tuple(bases[0].data.vertices[i].co) for b in bases for i in fixed)
manifest={'version':'rcl-female-v1','parts':[]}
names=['Suave','Angular','Arredondada','Alongada','Maçãs largas']
for idx,b in enumerate(bases,1):
    filename=f'base-feminina-{idx:02d}.glb';assembly=OUT/'montagens'/f'base-{idx:02d}-corte-01.glb'
    export(PUBLIC/filename,[b]);export(assembly,[b,hair])
    checks=[]
    for label,paths in [('separados',[PUBLIC/filename,PUBLIC/hairfile]),('montagem',[assembly])]:
        s=bpy.data.scenes.new(f'RCL_Validacao_{idx:02d}_{label}')
        pair=imported(s,paths)
        check={'kind':label,'geometry_equal':all(triangles(o)==triangles(pair[o['module_id']]) for o in [b,hair]),
               'materials_equal':all(materials(o)==materials(pair[o['module_id']]) for o in [b,hair]),
               'intersections':len(bvh(pair[b['module_id']]).overlap(bvh(pair[hair['module_id']]))) }
        assert check['geometry_equal'] and check['materials_equal'] and check['intersections']==0,check
        checks.append(check)
    bm=bmesh.new();bm.from_mesh(b.data)
    manifold=all(e.is_manifold for e in bm.edges);bm.free();assert manifold
    report['bases'].append({'id':b['module_id'],'height_m':b['head_height_m'],'manifold':manifold,'checks':checks})
    manifest['parts'].append({'id':f'rcl-v1-base-{idx:02d}','slotId':'base','name':f'Base {idx} · {names[idx-1]}',
                              'fileName':filename,'fileSize':(PUBLIC/filename).stat().st_size})
manifest['parts'].append({'id':'rcl-v1-hair-01','slotId':'hair','name':'Corte Feminino 1','fileName':hairfile,'fileSize':(PUBLIC/hairfile).stat().st_size})
assert report['common_scalp_equal']
report['files']={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in PUBLIC.glob('*.glb')}
(PUBLIC/'manifest.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False),encoding='utf-8')
(OUT/'validacao.json').write_text(json.dumps(report,indent=2,ensure_ascii=False),encoding='utf-8')
# Inspect front/profile/back without producing large reports.
bpy.context.window.scene=scene
scene.render.resolution_x=420;scene.render.resolution_y=470;scene.render.resolution_percentage=100;scene.eevee.taa_render_samples=32
target=Vector((0,0,.165))
for view,pos in [('frente',(0,-.9,.165)),('perfil',(.9,0,.165)),('costas',(0,.9,.165))]:
    scene.camera.location=pos;scene.camera.rotation_euler=(target-scene.camera.location).to_track_quat('-Z','Y').to_euler()
    for b in bases:
        for o in bases:o.hide_render=(o!=b);o.hide_set(o!=b)
        scene.render.filepath=str(OUT/'previas'/f'{b["module_id"]}_{view}.png');bpy.ops.render.render(write_still=True)
for b in bases:b.hide_render=(b!=bases[0]);b.hide_set(b!=bases[0])
scene.camera.location=(.53,-.8,.29);scene.camera.rotation_euler=(target-scene.camera.location).to_track_quat('-Z','Y').to_euler()
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'conjunto-feminino-v1.blend'))
print('RCL_DELIVERY_VALIDATED',json.dumps({'bases':5,'hair':1,'checks':10,'scalp_equal':True}),flush=True)
