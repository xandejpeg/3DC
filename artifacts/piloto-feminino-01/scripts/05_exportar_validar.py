import bpy,bmesh,json,hashlib,math
from pathlib import Path
from collections import Counter
from mathutils import Vector
from mathutils.kdtree import KDTree
from mathutils.bvhtree import BVHTree
OUT=Path(r"C:\Users\xandao\Documents\GitHub\3DC\artifacts\piloto-feminino-01")
source=bpy.data.scenes["RCL_Piloto_Feminino_01"];bpy.context.window.scene=source
base=bpy.data.objects["Base_Feminina_01"];hair=bpy.data.objects["Corte_Feminino_01"];root=bpy.data.objects["RCL_HEAD_ROOT"]
# Only explicitly selected source modules, never studio or other scenes.
for filename,objs in [
("base-feminina-01.glb",[root,base]),
("corte-feminino-01.glb",[root,hair]),
("montagem-feminina-01.glb",[root,base,hair])]:
    for ob in source.objects:ob.select_set(False)
    for ob in objs:ob.select_set(True)
    bpy.context.view_layer.objects.active=objs[-1]
    bpy.ops.export_scene.gltf(filepath=str(OUT/filename),export_format="GLB",use_selection=True,
      export_extras=True,export_yup=True,export_apply=False,export_materials="EXPORT",
      export_normals=True,export_texcoords=True,export_animations=False,export_cameras=False,export_lights=False)
def verification_scene(name,files):
    if name in bpy.data.scenes:raise RuntimeError("Verification scene already exists")
    s=bpy.data.scenes.new(name);bpy.context.window.scene=s
    s.unit_settings.system="METRIC";s.unit_settings.scale_length=1
    for filename in files:bpy.ops.import_scene.gltf(filepath=str(OUT/filename),import_shading="NORMALS",merge_vertices=False)
    bpy.context.view_layer.update()
    return s
individual=verification_scene("RCL_QA_GLB_SEPARADOS",["base-feminina-01.glb","corte-feminino-01.glb"])
mounted=verification_scene("RCL_QA_GLB_MONTAGEM",["montagem-feminina-01.glb"])
def points(ob):return [ob.matrix_world@v.co for v in ob.data.vertices]
def kdt(points):
    tree=KDTree(len(points))
    for i,p in enumerate(points):tree.insert(p,i)
    tree.balance();return tree
def maxdist(a,b):
    tree=kdt(b);return max(tree.find(p)[2] for p in a)
def triangles(ob):
    ob.data.calc_loop_triangles()
    pts=points(ob)
    return Counter(tuple(sorted(tuple(round(v,6) for v in pts[i]) for i in t.vertices)) for t in ob.data.loop_triangles)
def colors(ob):
    result=[]
    for m in ob.data.materials:
        p=next(n for n in m.node_tree.nodes if n.type=="BSDF_PRINCIPLED")
        result.append({"rgba":[round(float(x),6) for x in p.inputs["Base Color"].default_value],"roughness":round(float(p.inputs["Roughness"].default_value),6),"metallic":round(float(p.inputs["Metallic"].default_value),6)})
    return result
def pair(s):return {o.get("module_id"):o for o in s.objects if o.type=="MESH"}
report={"scope":["base-f-01","hair-f-01"],"comparison_tolerance_m":1e-6,"checks":{},"files":{}}
source_pair=pair(source)
for label,s in [("individuals",individual),("assembly",mounted)]:
    imported=pair(s);checks={}
    for mid,original in source_pair.items():
        ob=imported[mid];a=points(original);b=points(ob)
        ca=triangles(original);cb=triangles(ob)
        checks[mid]={"vertices_source":len(a),"vertices_reimport":len(b),"triangles_source":sum(ca.values()),"triangles_reimport":sum(cb.values()),"max_vertex_distance_m":max(maxdist(a,b),maxdist(b,a)),"triangle_geometry_equal_1um":ca==cb,"materials_equal":colors(original)==colors(ob),"world_transform":[list(row) for row in ob.matrix_world]}
    bpy.context.window.scene=s
    deps=bpy.context.evaluated_depsgraph_get()
    checks["base_hair_triangle_intersections"]=len(BVHTree.FromObject(imported["base-f-01"],deps).overlap(BVHTree.FromObject(imported["hair-f-01"],deps)))
    report["checks"][label]=checks
for name in ["base-feminina-01.glb","corte-feminino-01.glb","montagem-feminina-01.glb"]:
    data=(OUT/name).read_bytes()
    report["files"][name]={"bytes":len(data),"sha256":hashlib.sha256(data).hexdigest()}
chin=base.data.vertices[base["chin_vertex_index"]].co.z
crown=base.data.vertices[base["crown_vertex_index"]].co.z
report["measurements"]={"chin_z_m":chin,"crown_z_m":crown,"head_height_m":crown-chin,"neck_cut_z_m":0}
report["source_meshes"]={}
for ob in [base,hair]:
    bm=bmesh.new();bm.from_mesh(ob.data)
    report["source_meshes"][ob.get("module_id")]={"vertices":len(ob.data.vertices),"triangles":len(ob.data.loop_triangles),"boundary_edges":sum(e.is_boundary for e in bm.edges),"non_manifold_edges":sum(not e.is_manifold for e in bm.edges),"vertex_groups":[g.name for g in ob.vertex_groups]}
    bm.free()
report["passed"]=all(
   c[mid]["max_vertex_distance_m"]<1e-6 and c[mid]["triangle_geometry_equal_1um"] and c[mid]["materials_equal"]
   for c in report["checks"].values() for mid in source_pair
) and all(c["base_hair_triangle_intersections"]==0 for c in report["checks"].values())
(OUT/"verificacao/reimportacao.json").write_text(json.dumps(report,indent=2,ensure_ascii=False),encoding="utf-8")
# Render the reimported individual modules assembled at their original coordinates.
qa=individual;bpy.context.window.scene=qa
qa.world=source.world;qa.render.engine=source.render.engine
qa.render.resolution_x=1080;qa.render.resolution_y=1200;qa.render.resolution_percentage=100
qa.render.image_settings.file_format="PNG";qa.render.image_settings.color_mode="RGBA";qa.render.film_transparent=True
qa.view_settings.view_transform=source.view_settings.view_transform
qa.eevee.taa_render_samples=256
for ob in bpy.data.collections["02_ESTUDIO_NAO_EXPORTAR"].objects:qa.collection.objects.link(ob)
qa.camera=source.camera
cam=qa.camera;cam.data.ortho_scale=.395
target=Vector((0,0,.165))
views=[
("frente",(0,-.9,.165)),
("perfil",(.9,0,.165)),
("tres_quartos",(.53,-.8,.29)),
("costas",(0,.9,.165)),
("perfil_oposto",(-.9,0,.165))]
for name,pos in views:
    cam.location=pos;cam.rotation_euler=(target-cam.location).to_track_quat("-Z","Y").to_euler()
    qa.render.filepath=str(OUT/"imagens"/(name+".png"));bpy.ops.render.render(write_still=True)
# Optional isolated inspections, same imported objects; hide only during rendering.
p=pair(qa);cam.location=(.46,-.8,.28);cam.rotation_euler=(target-cam.location).to_track_quat("-Z","Y").to_euler()
for name,hide_id in [("base_isolada","hair-f-01"),("cabelo_isolado","base-f-01")]:
    p[hide_id].hide_render=True
    qa.render.filepath=str(OUT/"imagens"/(name+".png"));bpy.ops.render.render(write_still=True)
    p[hide_id].hide_render=False
# Save the native master active, with verification scenes available separately.
bpy.context.window.scene=source
for ob in source.objects:ob.select_set(False)
base.select_set(True);hair.select_set(True);bpy.context.view_layer.objects.active=base
for area in bpy.context.screen.areas:
    if area.type=="VIEW_3D":
        area.spaces.active.region_3d.view_distance=.48
        area.spaces.active.region_3d.view_location=(0,0,.16)
        area.spaces.active.region_3d.view_rotation=cam.rotation_euler.to_quaternion()
        area.spaces.active.overlay.show_overlays=False
source["validated_glbs"]="base-feminina-01.glb;corte-feminino-01.glb;montagem-feminina-01.glb"
source["validation_report"]="verificacao/reimportacao.json"
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/"piloto-feminino-01.blend"))
print(json.dumps({"passed":report["passed"],"checks":report["checks"],"measurements":report["measurements"]}))
