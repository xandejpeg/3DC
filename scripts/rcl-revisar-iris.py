"""Fix only the spherical iris/pupil surfaces in the saved V2, keeping all other geometry."""
import bpy,math
from mathutils import Vector
from pathlib import Path
R=Path(__file__).resolve().parents[1];s=bpy.data.scenes['RCL_Faciais_01'];bpy.context.window.scene=s
for o in s.objects:
    mid=str(o.get('module_id',''))
    if not any(mid.endswith('-'+k) for k in ['iris','pupil','highlight']):continue
    spherecx=-.037 if mid.startswith('eye-L') else .037
    center=o.data.vertices[0].co.copy();cx,cz=center.x,center.z
    kind=mid.split('-')[-1];radius={'iris':.0105,'pupil':.0052,'highlight':.0015}[kind]
    offset={'iris':.0002,'pupil':.00035,'highlight':.00055}[kind];N=12 if kind=='highlight' else 24
    def pt(x,z):return (x,-.060-math.sqrt(max(.000001,.022**2-(x-spherecx)**2-(z-.177)**2))-offset,z)
    v=[pt(cx,cz)];f=[]
    for r in [.2,.4,.6,.8,1]:
        for i in range(N):
            th=2*math.pi*i/N;v.append(pt(cx+radius*r*math.cos(th),cz+radius*r*math.sin(th)))
    for i in range(N):f.append((0,1+i,1+(i+1)%N))
    for k in range(4):
        for i in range(N):
            a=1+k*N+i;b=1+k*N+(i+1)%N;f.append((a,b,b+N,a+N))
    o.data.clear_geometry();o.data.from_pydata(v,[],f);o.data.update()
    for p in o.data.polygons:
        p.use_smooth=True
        if kind=='iris':p.material_index=(p.index*7)%4
    ns=[(Vector(p)-Vector((spherecx,-.060,.177))).normalized() for p in v]
    o.data.normals_split_custom_set_from_vertices(ns)
bpy.ops.wm.save_as_mainfile(filepath=str(R/'artifacts/conjunto-feminino-v2/conjunto-feminino-v2.blend'))
