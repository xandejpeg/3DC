import bpy, bmesh, math, json
from mathutils import Vector
from pathlib import Path
OUT=Path(r"C:\Users\xandao\Documents\GitHub\3DC\artifacts\piloto-feminino-01")
SCENE_NAME="RCL_Piloto_Feminino_01"
if SCENE_NAME in bpy.data.scenes:
    raise RuntimeError("Pilot scene already exists; use an explicit revision script.")
scene=bpy.data.scenes.new(SCENE_NAME)
bpy.context.window.scene=scene
scene.unit_settings.system="METRIC"
scene.unit_settings.scale_length=1.0
scene.render.engine="BLENDER_EEVEE"
scene.render.resolution_x=900
scene.render.resolution_y=1000
scene.render.resolution_percentage=100
scene.render.image_settings.file_format="PNG"
scene.render.image_settings.color_mode="RGBA"
scene.render.film_transparent=True
scene.view_settings.view_transform="AgX"
scene.world=bpy.data.worlds.new("RCL_StudioWorld")
scene.world.use_nodes=True
bg=next(n for n in scene.world.node_tree.nodes if n.type=="BACKGROUND")
bg.inputs["Color"].default_value=(0.22,0.27,0.34,1)
bg.inputs["Strength"].default_value=0.38
modules=bpy.data.collections.new("01_MODULOS_FONTE")
studio=bpy.data.collections.new("02_ESTUDIO_NAO_EXPORTAR")
scene.collection.children.link(modules)
scene.collection.children.link(studio)
root=bpy.data.objects.new("RCL_HEAD_ROOT",None)
modules.objects.link(root)
root.empty_display_type="PLAIN_AXES"
root.empty_display_size=.035
root["contract"]="RCL-head-pilot-0.2"
root["coordinate_frame"]="metres; Z up; -Y forward; origin centre of neck cut at z=0"
root["head_height_m"]=.24
root["chin_z_m"]=.065
root["crown_z_m"]=.305

def material(name,color,rough=.85):
    m=bpy.data.materials.new(name)
    m.use_nodes=True
    m.diffuse_color=(*color,1)
    p=next(n for n in m.node_tree.nodes if n.type=="BSDF_PRINCIPLED")
    p.inputs["Base Color"].default_value=(*color,1)
    p.inputs["Roughness"].default_value=rough
    p.inputs["Metallic"].default_value=0
    return m

skin=material("RCL_Pele_Piloto",(0.64,.29,.115))
profiles=[
(0,.043,.017,.061,0),
(.012,.037,.015,.058,0),
(.035,.029,.012,.055,0),
(.052,.028,.012,.051,0),
(.065,.025,.058,.052,.040),
(.073,.037,.064,.057,.035),
(.085,.050,.069,.064,.030),
(.102,.064,.072,.070,.023),
(.122,.074,.074,.077,.017),
(.143,.082,.076,.083,.009),
(.165,.085,.077,.088,.003),
(.187,.085,.079,.092,0),
(.210,.087,.080,.094,0),
(.233,.087,.077,.092,0),
(.253,.080,.069,.086,0),
(.272,.067,.054,.074,0),
(.286,.049,.037,.056,0),
(.297,.029,.018,.035,0),
(.303,.012,.006,.018,0),
(.305,0,-.004,.004,0)]

def profile(z):
    for a,b in zip(profiles,profiles[1:]):
        if a[0]<=z<=b[0]:
            t=(z-a[0])/(b[0]-a[0])
            return [a[k]*(1-t)+b[k]*t for k in range(1,5)]
    return list(profiles[-1][1:])

def head_point(theta,z,features=True):
    w,f,b,lift=profile(z)
    c=math.cos(theta); sn=math.sin(theta)
    x=w*sn
    # A broad frontal plane, rounded temporal and occipital volumes.
    y=-f*(c**.58) if c>=0 else b*(-c)**.86
    zz=z+lift*((1-c)/2)**.72
    if features and c>.32 and .105<zz<.216:
        orbital=sum(math.exp(-((x-s*.037)/.024)**4-((zz-.175)/.021)**4) for s in [-1,1])
        y+=.0135*orbital
        # No nose: editable low-relief nasal receiving region only.
        y+=.0015*math.exp(-(x/.014)**4-((zz-.144)/.030)**4)
    return (x,y,zz)

zs=sorted(set([p[0] for p in profiles[:-1]]+[.078,.094,.112,.132,.150,.156,.162,.169,.175,.181,.193,.201,.220,.243,.263,.280,.292,.300]))
N=80
verts=[head_point(2*math.pi*j/N,z) for z in zs for j in range(N)]
faces=[]
for k in range(len(zs)-1):
    for j in range(N):
        a=k*N+j; b=k*N+(j+1)%N; c=(k+1)*N+(j+1)%N; d=(k+1)*N+j
        # Stable diagonals, dense enough to keep the orbital region editable.
        if (j+k)%2: faces.extend([(a,b,d),(b,c,d)])
        else: faces.extend([(a,b,c),(a,c,d)])
faces.append(tuple(reversed(range(N))))
verts.append((0,.004,.305)); top=len(verts)-1
for j in range(N): faces.append(((len(zs)-1)*N+j,(len(zs)-1)*N+(j+1)%N,top))
mesh=bpy.data.meshes.new("BaseF01_MalhaEditavel")
mesh.from_pydata(verts,[],faces); mesh.update()
bm=bmesh.new(); bm.from_mesh(mesh); bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces)); bm.to_mesh(mesh); bm.free()
base=bpy.data.objects.new("Base_Feminina_01",mesh)
modules.objects.link(base); base.parent=root; base.data.materials.append(skin)
for p in mesh.polygons: p.use_smooth=False
for name,predicate in [
("INTERFACE_ORBITAL_L_PROVISORIA",lambda x,y,z: y<-.025 and ((x-.037)/.033)**2+((z-.175)/.030)**2<1),
("INTERFACE_ORBITAL_R_PROVISORIA",lambda x,y,z: y<-.025 and ((x+.037)/.033)**2+((z-.175)/.030)**2<1),
("INTERFACE_NASAL_PROVISORIA",lambda x,y,z:y<-.03 and abs(x)<.021 and .116<z<.175),
("COURO_CABELUDO",lambda x,y,z:z>.211 or (y>.02 and z>.140)),
("PESCOCO",lambda x,y,z:z<.061),
("CORTE_PESCOCO_PROVISORIO",lambda x,y,z:z==0)]:
    vg=base.vertex_groups.new(name=name)
    ix=[i for i,v in enumerate(verts) if predicate(*v)]
    if ix: vg.add(ix,1.0,"REPLACE")
base["module_id"]="base-f-01"; base["revision"]="p01-r1"
base["interface_status"]="orbital recessed editable skin, nasal editable patch; provisional, not modular fit validated"
base["excluded_parts"]="eyes,nose,brows,mouth,ears,beard,body"
base["head_height_m"]=.24
base["chin_vertex_index"]=zs.index(.065)*N
base["crown_vertex_index"]=top
base["reference_ids"]="R076,R088,R049,R099"

def aim(obj,target): obj.rotation_euler=(Vector(target)-obj.location).to_track_quat("-Z","Y").to_euler()
camdata=bpy.data.cameras.new("RCL_Camera_Ortografica")
camdata.type="ORTHO"; camdata.ortho_scale=.40
cam=bpy.data.objects.new("RCL_Camera_Ortografica",camdata)
studio.objects.link(cam); scene.camera=cam
cam.location=(.5,-.8,.35); aim(cam,(0,0,.155))
for name,loc,energy,size in [
("Key",(-.36,-.42,.61),16,.36),
("Fill",(.40,-.2,.32),9,.40),
("Rim",(.16,.30,.50),19,.32)]:
    ld=bpy.data.lights.new("RCL_"+name,"AREA"); ld.energy=energy; ld.shape="DISK"; ld.size=size
    ob=bpy.data.objects.new("RCL_"+name,ld); studio.objects.link(ob); ob.location=loc; aim(ob,(0,0,.16))
# Packed references can be opened in Blender's image editor without external path dependencies.
catalog=json.loads((OUT.parents[1]/"docs/referencias-rcl/Inventario_completo_referencias_RCL.json").read_text(encoding="utf-8-sig"))
for id in [49,52,76,88,99]:
    im=bpy.data.images.load(catalog["files"][id-1]["absolute_path"],check_existing=True)
    im.pack()
# Keep original startup scene untouched; configure only this task's new scene.
bpy.context.view_layer.objects.active=base
base.select_set(True)
for area in bpy.context.screen.areas:
    if area.type=="VIEW_3D":
        area.spaces.active.region_3d.view_distance=.58
        area.spaces.active.region_3d.view_location=(0,0,.15)
        area.spaces.active.region_3d.view_rotation=cam.rotation_euler.to_quaternion()
        area.spaces.active.shading.type="MATERIAL"
        area.spaces.active.clip_start=.001
scene["pilot_scope"]="only Base F01 + Hair F01"
scene["script_source"]="scripts/01_base.py"
scene.render.filepath=str(OUT/"imagens/revisao_base_tres_quartos.png")
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/"piloto-feminino-01.blend"))
bpy.ops.render.render(write_still=True)
print(json.dumps({"scene":scene.name,"base_vertices":len(mesh.vertices),"head_height":verts[top][2]-verts[base["chin_vertex_index"]][2]}))
