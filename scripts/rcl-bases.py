"""Build the five reference silhouettes from the existing R02 master.
Preview first; export/round-trip is a separate delivery step.
Run with Blender --background <R02.blend> --python scripts/rcl-bases.py.
"""
import bpy,bmesh,math,json,sys
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'artifacts/conjunto-feminino-v1';OUT.mkdir(parents=True,exist_ok=True)
(OUT/'previas').mkdir(exist_ok=True)
scene=bpy.data.scenes['RCL_R02_DEPOIS'];bpy.context.window.scene=scene
scene.name='RCL_Cinco_Bases_Cabelo_Unico'
original=next(o for o in scene.objects if o.get('module_id')=='base-f-01')
hair=next(o for o in scene.objects if o.get('module_id')=='hair-f-01')
hair.name='RCL_Corte_Feminino_01'
hair['compatibility']='rcl-female-scalp-v1'
root=original.parent
root.name='RCL_HEAD_ROOT';root['contract']='rcl-female-scalp-v1'
# Capture the existing hair. Every variant uses precisely this object and transform.
bpy.context.view_layer.update()
hair_bvh=BVHTree.FromObject(hair,bpy.context.evaluated_depsgraph_get())
def smooth(a,b,x):
    t=max(0.,min(1.,(x-a)/(b-a)));return t*t*(3-2*t)
source=[v.co.copy() for v in original.data.vertices]
groups={g.name:g.index for g in original.vertex_groups}
scalp={v.index for v in original.data.vertices if any(g.group==groups['COURO_CABELUDO'] for g in v.groups)}
protect={i for i,p in enumerate(source) if p.z>=.211 or i in scalp or p.z<.001}
clearance=[hair_bvh.find_nearest(p)[3] for p in source]
mask=[0 if i in protect else smooth(.006,.022,clearance[i]) for i in range(len(source))]
# Round the provisional orbital depression without adding any facial module.
for i,p in enumerate(source):
    if p.y<-.025 and .151<p.z<.202 and i not in protect:
        old=sum(max(0,1-((p.x-s*.037)/.023)**2-((p.z-.175)/.021)**2)**.70 for s in [-1,1])
        new=sum(max(0,1-((p.x-s*.037)/.024)**2-((p.z-.175)/.023)**2)**2 for s in [-1,1])
        p.y+=mask[i]*(-.019*old+.020*new)
# Smooth only the underside/neck transition of the shared source.
neighbors=[set() for _ in source]
for e in original.data.edges:
    a,b=e.vertices;neighbors[a].add(b);neighbors[b].add(a)
for _ in range(5):
    updated=[p.copy() for p in source]
    for i,p in enumerate(source):
        w=mask[i]*smooth(.008,.030,p.z)*(1-smooth(.090,.122,p.z))*smooth(-.055,-.015,p.y)*.32
        if w:
            avg=sum((source[j] for j in neighbors[i]),Vector())/len(neighbors[i])
            updated[i]=p.lerp(avg,w)
    source=updated

# Gains are local shape controls, never whole-head scaling.
specs=[
 {'id':1,'label':'Suave','chin':0,'depth':0},
 {'id':2,'label':'Angular','chin':-.001,'depth':.001},
 {'id':3,'label':'Arredondada','chin':.006,'depth':.003},
 {'id':4,'label':'Alongada','chin':-.019,'depth':-.002},
 {'id':5,'label':'Macas largas','chin':-.004,'depth':.001}
]
gains={1:[],2:[(.18,.098,.039)],3:[(.22,.105,.041)],4:[(-.25,.100,.043)],5:[(-.18,.090,.027),(.08,.140,.023)]}
bases=[]
for spec in specs:
    b=original.copy();b.data=original.data.copy();scene.collection.objects.link(b)
    b.name=f'RCL_Base_Feminina_{spec["id"]:02d}';b.data.name=b.name+'_Malha'
    deltas=[]
    for i,v in enumerate(b.data.vertices):
        p=source[i].copy();x,y,z=p
        # Front and lateral face vary; posterior scalp keeps its common fit.
        region=1-smooth(.010,.052,y)
        neck=1-smooth(.040,.075,z)
        w=mask[i]*max(region,neck)
        dz=spec['chin']*smooth(.016,.077,z)*(1-smooth(.080,.158,z))*w
        gain=sum(amount*math.exp(-((z-center)/radius)**2) for amount,center,radius in gains[spec['id']])
        dx=x*gain*smooth(.010,.055,z)*(1-smooth(.140,.170,z))*w
        dy=-spec['depth']*smooth(.080,.110,z)*(1-smooth(.130,.155,z))*w
        delta=Vector((dx,dy,dz))
        # No variant is permitted to consume the fixed scalp clearance.
        max_motion=max(0,clearance[i]-.003)*.70
        if delta.length>max_motion and delta.length:delta*=max_motion/delta.length
        deltas.append(delta)
    # Smooth the deformation field, not the facial landmarks or scalp.
    # This avoids ridges where hair-clearance masks vary across neighboring vertices.
    for _ in range(8):
        updated=[d.copy() for d in deltas]
        for i,d in enumerate(deltas):
            if mask[i]>0:
                avg=sum((deltas[j] for j in neighbors[i]),Vector())/len(neighbors[i])
                updated[i]=d.lerp(avg,.38)*min(1,mask[i]*4)
        deltas=updated
    for i,v in enumerate(b.data.vertices):v.co=source[i]+deltas[i]
    # Remove small lower-jaw ridges from the inherited radial mesh while preserving
    # the common scalp, orbital area and the broad silhouette differences.
    for _ in range(10):
        coords=[v.co.copy() for v in b.data.vertices]
        for i,v in enumerate(b.data.vertices):
            p=coords[i]
            w=mask[i]*smooth(.045,.080,p.z)*(1-smooth(.118,.149,p.z))*.38
            if w:
                avg=sum((coords[j] for j in neighbors[i]),Vector())/len(neighbors[i])
                v.co=p.lerp(avg,w)
    b.data.update()
    b['module_id']=f'base-f-{spec["id"]:02d}';b['revision']='rcl-set-v1'
    b['reference_ids']=f'R{75+spec["id"]:03d},R{87+spec["id"]:03d},R049'
    b['compatibility']='rcl-female-scalp-v1';b['shape_label']=spec['label']
    b['head_height_m']=b.data.vertices[b['crown_vertex_index']].co.z-b.data.vertices[b['chin_vertex_index']].co.z
    b.hide_render=True;bases.append(b)
# Keep the baseline file intact; only remove its object from this new working scene.
for c in list(original.users_collection):
    if c in list(scene.collection.children) or c==scene.collection:c.objects.unlink(original)
if original.name in scene.objects:scene.collection.objects.unlink(original)
scene['base_variants']=';'.join(b.name for b in bases)
scene['single_hair_object']=hair.name
for b in bases:b.hide_set(b!=bases[0]);b.hide_render=(b!=bases[0])
scene.camera.data.ortho_scale=.395
scene.camera.location=(.53,-.8,.29)
scene.camera.rotation_euler=(Vector((0,0,.165))-scene.camera.location).to_track_quat('-Z','Y').to_euler()
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'conjunto-feminino-v1.blend'))
(OUT/'parametros.json').write_text(json.dumps({'variants':specs,'width_gaussians':gains,'gaussian_fields':['relative_width_gain','center_z_m','radius_m']},indent=2,ensure_ascii=False),encoding='utf-8')
# Lightweight previews: a single camera, identical framing, no export yet.
scene.render.resolution_x=420;scene.render.resolution_y=470;scene.render.resolution_percentage=100
scene.eevee.taa_render_samples=32
for b in bases:
    for other in bases:other.hide_set(other!=b);other.hide_render=(other!=b)
    for mode in ['base','montada']:
        hair.hide_render=(mode=='base')
        scene.render.filepath=str(OUT/'previas'/f'{b["module_id"]}_{mode}.png')
        bpy.ops.render.render(write_still=True)
hair.hide_render=False
print('RCL_PREVIEWS_READY',flush=True)
