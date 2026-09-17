import bpy,bmesh,json
from pathlib import Path
from mathutils.bvhtree import BVHTree
OUT=Path(r"C:\Users\xandao\Documents\GitHub\3DC\artifacts\piloto-feminino-01")
base=bpy.data.objects["Base_Feminina_01"];hair=bpy.data.objects["Corte_Feminino_01"]
deps=bpy.context.evaluated_depsgraph_get();b=BVHTree.FromObject(base,deps)
inner=set(i for p in hair.data.polygons if p.material_index==4 for i in p.vertices)
for i in inner:
    v=hair.data.vertices[i];p,n,fi,d=b.find_nearest(v.co);v.co+=n*.003
bm=bmesh.new();bm.from_mesh(hair.data);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(hair.data);bm.free()
hair.data.update();hair["revision"]="p01-r3"
bpy.context.view_layer.update()
h=BVHTree.FromObject(hair,bpy.context.evaluated_depsgraph_get())
result={"correction":"inner scalp shell moved outward by 0.003 m along nearest base surface normal; exterior and locks unchanged","inner_vertices_changed":len(inner),"surface_overlap_pairs_after":len(b.overlap(h))}
(OUT/"verificacao/correcao_calota.json").write_text(json.dumps(result,indent=2),encoding="utf-8")
print(json.dumps(result))
