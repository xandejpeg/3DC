import bpy, bmesh, math, json
from mathutils import Vector
from pathlib import Path
OUT=Path(r"C:\Users\xandao\Documents\GitHub\3DC\artifacts\piloto-feminino-01")
scene=bpy.data.scenes["RCL_Piloto_Feminino_01"]
bpy.context.window.scene=scene
base=bpy.data.objects["Base_Feminina_01"]
root=bpy.data.objects["RCL_HEAD_ROOT"]
modules=bpy.data.collections["01_MODULOS_FONTE"]
# Load geometry-only definitions from stage 1 without re-running its scene creation.
source=(OUT/"scripts/01_base.py").read_text(encoding="utf-8")
exec(source[source.index("profiles=["):source.index("zs=sorted")])
# Round provisional orbital hollows; geometry stays explicit and editable.
old_head_point=head_point
def head_point(theta,z,features=True):
    x,y,zz=old_head_point(theta,z,False)
    if features and math.cos(theta)>.32 and .105<zz<.216:
        orbital=sum(math.exp(-1.7*((x-s*.037)/.027)**2-1.7*((zz-.175)/.023)**2) for s in [-1,1])
        y+=.020*orbital
        y+=.0015*math.exp(-(x/.014)**4-((zz-.144)/.030)**4)
    return (x,y,zz)
# Original topology and vertex groups retained, no remesh.
zs=sorted(set([p[0] for p in profiles[:-1]]+[.078,.094,.112,.132,.150,.156,.162,.169,.175,.181,.193,.201,.220,.243,.263,.280,.292,.300]))
N=80
for k,z in enumerate(zs):
    for j in range(N): base.data.vertices[k*N+j].co=head_point(2*math.pi*j/N,z)
for p in base.data.polygons: p.use_smooth=True
base.data.update()
base["revision"]="p01-r2"
# Studio exposure correction, keeping light placement consistent.
for name,e in [("RCL_Key",3.2),("RCL_Fill",1.8),("RCL_Rim",3.8)]: bpy.data.objects[name].data.energy=e
if "Corte_Feminino_01" in bpy.data.objects: raise RuntimeError("Hair already exists; use revision script.")
def mat(name,col):
    m=bpy.data.materials.new(name);m.use_nodes=True;m.diffuse_color=(*col,1)
    p=next(n for n in m.node_tree.nodes if n.type=="BSDF_PRINCIPLED")
    p.inputs["Base Color"].default_value=(*col,1)
    p.inputs["Roughness"].default_value=.82
    return m
mats=[
mat("RCL_Cabelo_Castanho",(.071,.035,.018)),
mat("RCL_Cabelo_PlanoClaro",(.094,.048,.026)),
mat("RCL_Cabelo_PlanoMedio",(.081,.040,.021)),
mat("RCL_Cabelo_PlanoEscuro",(.050,.024,.012)),
mat("RCL_Cabelo_Interior",(.032,.015,.008))]
V=[];F=[];MI=[];groups={}
def face(ids,mi): F.append(tuple(ids));MI.append(mi)
# Closed scalp shell with matched inner/outer topology.
n=64; rows=13
def cap_end(theta):
    c=math.cos(theta)
    return .132+.108*max(c,0)**3
def surf(theta,z,offset):
    x,y,zz=head_point(theta,z,False)
    radial=Vector((math.sin(theta),-math.cos(theta),.25))
    radial.normalize()
    return Vector((x,y,z))+radial*offset
for layer in range(2):
    for k in range(rows):
        t=(k+1)/rows
        for j in range(n):
            a=2*math.pi*j/n
            z=.305+(.0+cap_end(a)-.305)*t
            off=.006 if layer==0 else .0015
            p=surf(a,z,off)
            p.z+= (.011 if layer==0 else .0015)*(1-t)**1.2
            V.append(tuple(p))
for layer in range(2):
    st=layer*rows*n
    for k in range(rows-1):
        for j in range(n):
            a=st+k*n+j;b=st+k*n+(j+1)%n;c=st+(k+1)*n+(j+1)%n;d=st+(k+1)*n+j
            ids=(a,b,c,d) if layer==0 else (d,c,b,a)
            face(ids,0 if layer==0 else 4)
    pole=len(V);V.append((0,.004,.316 if layer==0 else .3065))
    for j in range(n): face((pole,st+j,st+(j+1)%n) if layer==0 else (pole,st+(j+1)%n,st+j),0 if layer==0 else 4)
for j in range(n):
    a=(rows-1)*n+j;b=(rows-1)*n+(j+1)%n;c=rows*n+(rows-1)*n+(j+1)%n;d=rows*n+(rows-1)*n+j
    face((a,d,c,b),3)
groups["CALOTA_INTERNA_EDITAVEL"]=list(range(rows*n,rows*n*2))
groups["CALOTA_EXTERNA"]=list(range(rows*n))
def bezier(cs,t):
    a,b,c,d=map(Vector,cs)
    return a*(1-t)**3+b*3*(1-t)**2*t+c*3*(1-t)*t*t+d*t**3
def lock(name,cs,width,thick=.006,tone=0):
    start=len(V); steps=7; ring=5
    for k in range(steps):
        t=k/steps
        p=bezier(cs,t)
        tangent=(bezier(cs,min(1,t+.005))-bezier(cs,max(0,t-.005))).normalized()
        outward=Vector((p.x,p.y,(p.z-.19)*.58))
        outward.normalize()
        outward=outward-tangent*outward.dot(tangent)
        if outward.length<.1:outward=Vector((0,-1,0))
        outward.normalize()
        side=tangent.cross(outward).normalized()
        taper=math.sin(math.pi*(.15+.85*t))**.80
        w=width*taper
        h=thick*taper
        # A flattened, ridged lock; broad face planes instead of round tubes.
        section=[(-w/2,0),(-w*.28,h*.80),(w*.12,h),(w/2,0),(0,-h*.35)]
        for u,v in section:V.append(tuple(p+side*u+outward*v))
    tip=len(V);V.append(tuple(Vector(cs[-1])))
    for k in range(steps-1):
        for j in range(ring):
            a=start+k*ring+j;b=start+k*ring+(j+1)%ring;c=start+(k+1)*ring+(j+1)%ring;d=start+(k+1)*ring+j
            # A diagonal on broad upper planes creates large controlled facets.
            color=(tone+[0,1,2,3,3][j])%4
            if j<3:
                face((a,b,c),color);face((a,c,d),color if k%2 else min(3,color+1))
            else:face((a,b,c,d),3)
    face(tuple(reversed(range(start,start+ring))),3)
    for j in range(ring):face((start+(steps-1)*ring+j,start+(steps-1)*ring+(j+1)%ring,tip),min(3,tone))
    groups[name]=list(range(start,len(V)))
# Rear and side masses: two overlapping layers with a diagonal flow from the part.
for j in range(15):
    a=.65+(2*math.pi-1.30)*j/14
    sign=1 if a<math.pi else -1
    ar=a-.24*sign
    rootp=surf(ar,.279,.012)
    mid1=surf(a-.10*sign,.250,.017)
    mid2=surf(a+.08*sign,.197,.018)
    tip=surf(a+.14*sign,.134+(j%3)*.009,.012)
    tip.z-=.017
    lock("MECHA_NUCA_%02d"%j,[rootp,mid1,mid2,tip],.030,.006,j%2)
for j in range(11):
    a=.70+(2*math.pi-1.4)*j/10
    ar=a-.34
    pp=[surf(ar,.299,.010),surf(a-.15,.281,.018),surf(a+.06,.249,.022),surf(a+.21,.211+(j%3)*.010,.021)]
    lock("MECHA_COROA_%02d"%j,pp,.034,.007,j%2)
# Sweeping left fringe: explicit 3D curves preserve the long, asymmetrical silhouette.
front_locks=[
("FRANJA_01",[(.034,-.025,.322),(.009,-.065,.329),(-.082,-.069,.267),(-.112,-.047,.238)],.033,.008),
("FRANJA_02",[(.042,-.037,.320),(.010,-.084,.309),(-.086,-.087,.233),(-.102,-.063,.187)],.038,.009),
("FRANJA_03",[(.039,-.049,.310),(.012,-.098,.302),(-.076,-.100,.203),(-.086,-.077,.132)],.037,.009),
("FRANJA_04",[(.030,-.061,.300),(.003,-.100,.282),(-.057,-.099,.194),(-.066,-.073,.112)],.034,.008),
("FRANJA_05",[(.018,-.069,.292),(-.005,-.099,.266),(-.044,-.093,.199),(-.048,-.077,.157)],.026,.006),
("TOPO_01",[(.042,.006,.310),(.032,-.018,.344),(-.011,-.021,.331),(-.066,-.018,.307)],.033,.009),
("TOPO_02",[(.021,.033,.305),(.014,.008,.334),(-.032,-.010,.332),(-.069,-.031,.291)],.029,.008),
("DIREITA_01",[(.040,-.030,.306),(.073,-.035,.315),(.097,-.040,.290),(.110,-.031,.271)],.033,.007),
("DIREITA_02",[(.042,-.043,.291),(.081,-.065,.294),(.097,-.060,.251),(.107,-.041,.231)],.030,.007),
("DIREITA_03",[(.053,-.054,.274),(.083,-.069,.263),(.087,-.071,.227),(.082,-.055,.193)],.025,.006),
]
for i,(name,cs,w,h) in enumerate(front_locks):lock(name,cs,w,h,i%2)
mesh=bpy.data.meshes.new("CorteF01_MechasEditaveis")
mesh.from_pydata(V,[],F);mesh.update()
bm=bmesh.new();bm.from_mesh(mesh);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(mesh);bm.free()
hair=bpy.data.objects.new("Corte_Feminino_01",mesh);modules.objects.link(hair);hair.parent=root
for m in mats:mesh.materials.append(m)
for p,mi in zip(mesh.polygons,MI):p.material_index=mi;p.use_smooth=False
for name,ids in groups.items():
    vg=hair.vertex_groups.new(name=name);vg.add(ids,1.0,"REPLACE")
hair["module_id"]="hair-f-01";hair["revision"]="p01-r1"
hair["reference_ids"]="R052,R088,R049,R099"
hair["representation"]="closed scalp shell and individually editable broad faceted locks, one mesh object"
hair["interface_status"]="provisional scalp clearance; only tested against base-f-01"
cam=scene.camera
cam.location=(.46,-.8,.30)
cam.rotation_euler=(Vector((0,0,.164))-cam.location).to_track_quat("-Z","Y").to_euler()
cam.data.ortho_scale=.395
for area in bpy.context.screen.areas:
    if area.type=="VIEW_3D":
        area.spaces.active.overlay.show_overlays=False
        area.spaces.active.region_3d.view_rotation=cam.rotation_euler.to_quaternion()
for o in bpy.context.selected_objects:o.select_set(False)
hair.select_set(True);bpy.context.view_layer.objects.active=hair
scene.render.filepath=str(OUT/"imagens/revisao_montagem_tres_quartos.png")
bpy.ops.render.render(write_still=True)
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/"piloto-feminino-01.blend"))
print(json.dumps({"hair_vertices":len(V),"hair_polygons":len(F),"locks":len(groups)-2}))
