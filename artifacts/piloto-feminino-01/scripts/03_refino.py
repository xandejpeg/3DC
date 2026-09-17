from pathlib import Path
import bpy
OUT=Path(r"C:\Users\xandao\Documents\GitHub\3DC\artifacts\piloto-feminino-01")
old=bpy.data.objects.get("Corte_Feminino_01")
if old is None or old.get("module_id")!="hair-f-01":raise RuntimeError("Expected task-owned hair not found")
bpy.data.objects.remove(old,do_unlink=True)
code=(OUT/"scripts/02_cabelo.py").read_text(encoding="utf-8")
code=code.replace('exec(source[source.index("profiles=["):source.index("zs=sorted")])','exec(source[source.index("profiles=["):source.index("zs=sorted")].replace("**.72","**1.25"))')
code=code.replace('orbital=sum(math.exp(-1.7*((x-s*.037)/.027)**2-1.7*((zz-.175)/.023)**2) for s in [-1,1])','orbital=sum(max(0,1-((x-s*.037)/.023)**2-((zz-.175)/.021)**2)**.70 for s in [-1,1])')
code=code.replace('y+=.020*orbital','y+=.019*orbital')
code=code.replace('return .132+.108*max(c,0)**3','return .095+.145*max(c,0)**3+.030*math.sin(theta)**2+.006*math.sin(theta*13)')
code=code.replace('groups["CALOTA_EXTERNA"]=list(range(rows*n))','groups["CALOTA_EXTERNA"]=list(range(rows*n))\nfrom mathutils.bvhtree import BVHTree\ncap_bvh=BVHTree.FromPolygons(V,[f for f,m in zip(F,MI) if m==0],all_triangles=False)')
code=code.replace('start=len(V); steps=7; ring=5','cs=list(cs)\n    nearest=cap_bvh.find_nearest(Vector(cs[0]))\n    if nearest[0] is not None:\n        p=nearest[0]; outward=Vector((p.x,p.y,(p.z-.19)*.6)).normalized();cs[0]=tuple(p+outward*.002)\n    start=len(V); steps=7; ring=5')
code=code.replace('tip=surf(a+.14*sign,.134+(j%3)*.009,.012)\n    tip.z-=.017','tip=surf(a+.14*sign,.088+.029*math.sin(a)**2+(j%3)*.006,.013)\n    tip.z-=.010')
code=code.replace('],.030,.006,j%2)','],.039,.008,j%2)')
code=code.replace('(.032,-.018,.344)','(.032,-.018,.329)')
code=code.replace('(.014,.008,.334)','(.014,.008,.319)')
code=code.replace('(-.032,-.010,.332)','(-.032,-.010,.320)')
code=code.replace('(.073,-.035,.315)','(.073,-.035,.301)')
code=code.replace('(.094,.048,.026)','(.082,.039,.019)')
code=code.replace('(.081,.040,.021)','(.075,.035,.017)')
code=code.replace('(.050,.024,.012)','(.060,.027,.013)')
code=code.replace('hair["revision"]="p01-r1"','hair["revision"]="p01-r2"')
code=code.replace('base["revision"]="p01-r2"','base["revision"]="p01-r3"')
# Smooth the neck/jaw transition locally without touching the chin or crown landmarks.
code=code.replace('base.data.update()','''base.data.update()
bm=bmesh.new();bm.from_mesh(base.data)
vs=[v for v in bm.verts if .035<v.co.z<.112 and v.co.y>-.042]
for _ in range(5):bmesh.ops.smooth_vert(bm,verts=vs,factor=.4,use_axis_x=True,use_axis_y=True,use_axis_z=True)
bm.to_mesh(base.data);bm.free()
scene.eevee.taa_render_samples=256
''')
exec(compile(code,"02_cabelo_refinado","exec"))
from mathutils import Vector
cam=scene.camera
for name,pos in [("frente",(0,-.9,.17)),("perfil",(.9,0,.17)),("costas",(0,.9,.17))]:
    cam.location=pos;cam.rotation_euler=(Vector((0,0,.167))-cam.location).to_track_quat("-Z","Y").to_euler()
    scene.render.filepath=str(OUT/"imagens"/("revisao2_"+name+".png"))
    bpy.ops.render.render(write_still=True)
print("Refinement: round sockets, softer chin/neck, roots seated on cap, irregular nape.")
