"""Export and round-trip only the new V2 facial set; reuse the completed hair GLB."""
import bpy,json,hashlib,shutil,sys
from pathlib import Path
from collections import Counter
from mathutils import Vector
from mathutils.bvhtree import BVHTree
R=Path(__file__).resolve().parents[1];O=R/'artifacts/conjunto-feminino-v2';P=R/'public/models/rcl-feminino-v2'
P.mkdir(exist_ok=True);(O/'montagens').mkdir(exist_ok=True)
s=bpy.data.scenes['RCL_Faciais_01'];bpy.context.window.scene=s
bases=sorted([o for o in s.objects if str(o.get('module_id','')).startswith('base-f-') and not o.get('base_id')],key=lambda o:o['module_id'])
hair=next(o for o in s.objects if o.get('module_id')=='hair-f-01');root=hair.parent
eyes=[o for o in s.objects if str(o.get('module_id','')).startswith('eye-')]
nose=[o for o in s.objects if str(o.get('module_id','')).startswith('nose')]
fixed={b['module_id']:[o for o in s.objects if o.get('base_id')==b['module_id']] for b in bases}
def export(path,objects):
    bpy.context.window.scene=s
    for o in s.objects:o.hide_set(False);o.select_set(False)
    for o in [root,*objects]:o.select_set(True)
    bpy.context.view_layer.objects.active=objects[0]
    bpy.ops.export_scene.gltf(filepath=str(path),export_format='GLB',use_selection=True,use_active_scene=True,export_extras=True,export_yup=True,export_materials='EXPORT',export_animations=False,export_cameras=False,export_lights=False)
def points(o):return [o.matrix_world@v.co for v in o.data.vertices]
def triangles(o):
    o.data.calc_loop_triangles();p=points(o)
    return Counter(tuple(sorted(tuple(round(n,6) for n in p[i]) for i in t.vertices)) for t in o.data.loop_triangles)
def materials(o):
    values=[]
    for m in o.data.materials:
        n=next(n for n in m.node_tree.nodes if n.type=='BSDF_PRINCIPLED')
        values.append(tuple(round(x,6) for x in (*n.inputs['Base Color'].default_value,n.inputs['Roughness'].default_value,n.inputs['Metallic'].default_value)))
    return sorted(values)
def bvh(o):return BVHTree.FromPolygons(points(o),[p.vertices[:] for p in o.data.polygons])
interfaces=json.loads((O/'interfaces.json').read_text())
def seams(objects,baseid):
    basepts=points(objects[baseid]);result={}
    for name,info in interfaces.items():
        modulepts=points(objects[name+'-skin'])
        errors=[max(min((Vector(p)-q).length for q in basepts),min((Vector(p)-q).length for q in modulepts)) for p in info['positions']]
        result[name]=max(errors)
    return result
eyes_only='--eyes-only' in sys.argv
hairfile='corte-feminino-01.glb'
if not eyes_only:shutil.copy2(R/'public/models/rcl-feminino-v1'/hairfile,P/hairfile)
export(P/'olho-01-par.glb',eyes)
if not eyes_only:export(P/'nariz-01.glb',nose)
manifest={'version':'rcl-female-v2','parts':[]};report={'source':'conjunto-feminino-v1','hair_file_unchanged':True,'checks':[]}
names=['Suave','Angular','Arredondada','Alongada','Maçãs largas']
reference_hair=hashlib.sha256((R/'public/models/rcl-feminino-v1'/hairfile).read_bytes()).hexdigest()
assert hashlib.sha256((P/hairfile).read_bytes()).hexdigest()==reference_hair
for i,b in enumerate(bases,1):
    local=[b,*fixed[b['module_id']]];allparts=[*local,hair,*eyes,*nose]
    basefile=f'base-feminina-{i:02d}.glb';assembly=O/'montagens'/f'cabeca-feminina-{i:02d}.glb'
    if not eyes_only:export(P/basefile,local)
    export(assembly,allparts)
    manifest['parts'].append({'id':f'rcl-v2-base-{i:02d}','slotId':'base','name':f'Base {i} · {names[i-1]}','fileName':basefile,'fileSize':(P/basefile).stat().st_size})
    originals={o['module_id']:o for o in allparts}
    for kind,paths in [('separados',[P/basefile,P/hairfile,P/'olho-01-par.glb',P/'nariz-01.glb']),('montagem',[assembly])]:
        q=bpy.data.scenes.new(f'RCL_V2_QA_{i}_{kind}');bpy.context.window.scene=q
        for p in paths:bpy.ops.import_scene.gltf(filepath=str(p),import_shading='NORMALS',merge_vertices=False)
        bpy.context.view_layer.update();loaded={o['module_id']:o for o in q.objects if o.type=='MESH'}
        assert set(loaded)==set(originals),(set(loaded),set(originals))
        check={'base':i,'kind':kind,'geometry_equal':all(triangles(o)==triangles(loaded[k]) for k,o in originals.items()),'materials_equal':all(materials(o)==materials(loaded[k]) for k,o in originals.items()),'seam_max_m':seams(loaded,b['module_id']),'base_hair_intersections':len(bvh(loaded[b['module_id']]).overlap(bvh(loaded['hair-f-01'])))}
        assert check['geometry_equal'] and check['materials_equal'],check
        assert max(check['seam_max_m'].values())<1e-6 and check['base_hair_intersections']==0,check
        report['checks'].append(check)
        # Render the imported assembly with the same studio, then discard only this temporary QA scene.
        if kind=='montagem':
            q.world=s.world;q.render.engine=s.render.engine;q.view_settings.view_transform=s.view_settings.view_transform
            q.view_settings.look=s.view_settings.look;q.render.film_transparent=True
            q.render.resolution_x=480;q.render.resolution_y=540;q.render.resolution_percentage=100;q.eevee.taa_render_samples=32
            for o in s.objects:
                if o.type in {'CAMERA','LIGHT'}:q.collection.objects.link(o)
            q.camera=s.camera;target=Vector((0,0,.165))
            for view,pos,show_hair in [('frente',(0,-.9,.165),True),('sem-cabelo',(0,-.9,.165),False),('tres-quartos',(.53,-.8,.29),True)]+([('perfil',(.9,0,.165),True),('costas',(0,.9,.165),True)] if i==1 else []):
                loaded['hair-f-01'].hide_render=not show_hair
                q.camera.location=pos;q.camera.rotation_euler=(target-q.camera.location).to_track_quat('-Z','Y').to_euler()
                q.render.filepath=str(O/'previas'/f'base-{i:02d}-{view}.png');bpy.ops.render.render(write_still=True)
        imported_objects=[o for o in q.objects if o.type not in {'CAMERA','LIGHT'}]
        bpy.context.window.scene=s;bpy.data.scenes.remove(q)
        for o in imported_objects:bpy.data.objects.remove(o,do_unlink=True)
for ident,slot,name,file in [('hair-01','hair','Corte Feminino 1',hairfile),('eye-01','eyes','Olho 1 · Castanho','olho-01-par.glb'),('nose-01','nose','Nariz 1','nariz-01.glb')]:
    manifest['parts'].append({'id':'rcl-v2-'+ident,'slotId':slot,'name':name,'fileName':file,'fileSize':(P/file).stat().st_size})
for j,b in enumerate(bases):
    for o in [b,*fixed[b['module_id']]]:o.hide_render=j!=0;o.hide_set(j!=0)
hair.hide_render=False;hair.hide_set(False)
s.camera.location=(.53,-.8,.29);s.camera.rotation_euler=(Vector((0,0,.165))-s.camera.location).to_track_quat('-Z','Y').to_euler()
(P/'manifest.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False),encoding='utf8')
(O/'validacao.json').write_text(json.dumps(report,indent=2),encoding='utf8')
bpy.ops.wm.save_as_mainfile(filepath=str(O/'conjunto-feminino-v2.blend'))
print('V2_EXPORT_REIMPORT_PASS',len(report['checks']),flush=True)
