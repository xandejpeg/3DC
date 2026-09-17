"""Read-only diagnosis of a failed hair checkpoint; prints groups and regions."""
import bpy,json,sys
from collections import Counter
from mathutils.bvhtree import BVHTree
def bvh(o):return BVHTree.FromPolygons([o.matrix_world@v.co for v in o.data.vertices],[p.vertices[:] for p in o.data.polygons])
s=bpy.context.scene
hair=next(o for o in s.objects if str(o.get('module_id','')).startswith('hair'))
base=next(o for o in s.objects if o.get('module_id')=='base-f-01')
for obstacle in [base,*[o for o in s.objects if o.get('base_id')=='base-f-01']]:
    pairs=bvh(hair).overlap(bvh(obstacle))
    if not pairs:continue
    inds={a for a,b in pairs};names=Counter();verts=set()
    for i in inds:
        for vi in hair.data.polygons[i].vertices:
            verts.add(vi)
            for g in hair.data.vertices[vi].groups:names[hair.vertex_groups[g.group].name]+=1
    coords=[hair.data.vertices[i].co for i in verts]
    print(json.dumps({'obstacle':obstacle.name,'pairs':len(pairs),'groups':names,'bounds':[[min(p[i] for p in coords),max(p[i] for p in coords)] for i in range(3)]}),flush=True)
