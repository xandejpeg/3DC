import bpy,json,hashlib
from pathlib import Path
from mathutils import Vector
PARENT=Path(r'C:\Users\xandao\Documents\GitHub\3DC\artifacts\piloto-feminino-01')
OUT=PARENT/'revisao-rosto-02'
# Reuse the existing export/reimport checks, without running the old modelling or render code.
code=(PARENT/'scripts/05_exportar_validar.py').read_text(encoding='utf-8').split('# Render the reimported')[0]
code=code.replace('OUT=Path(r"C:\\Users\\xandao\\Documents\\GitHub\\3DC\\artifacts\\piloto-feminino-01")','OUT=Path(r"'+str(OUT)+'")')
code=code.replace('source=bpy.data.scenes["RCL_Piloto_Feminino_01"]','source=bpy.data.scenes["RCL_R02_DEPOIS"]')
code=code.replace('base=bpy.data.objects["Base_Feminina_01"];hair=bpy.data.objects["Corte_Feminino_01"];root=bpy.data.objects["RCL_HEAD_ROOT"]','base=next(o for o in source.objects if o.get("module_id")=="base-f-01");hair=next(o for o in source.objects if o.get("module_id")=="hair-f-01");root=base.parent')
code=code.replace('RCL_QA_GLB_SEPARADOS','RCL_R02_QA_SEPARADOS').replace('RCL_QA_GLB_MONTAGEM','RCL_R02_QA_MONTAGEM')
assert 'use_active_scene' in bpy.ops.export_scene.gltf.get_rna_type().properties
code=code.replace('use_selection=True,','use_selection=True,use_active_scene=True,')
code=code.replace('def pair(s):return {o.get("module_id"):o for o in s.objects if o.type=="MESH"}', '''def pair(s):
    meshes=[o for o in s.objects if o.type=="MESH"]
    assert len(meshes)==2, (s.name,len(meshes))
    assert sorted(o.get("module_id","") for o in meshes)==["base-f-01","hair-f-01"]
    return {o.get("module_id"):o for o in meshes}''')
code=code.replace('bpy.context.window.scene=s\n    deps=', 'bpy.context.window.scene=s\n    bpy.context.view_layer.update()\n    deps=')
exec(compile(code,'existing_export_validation_adapted','exec'))
assert report['passed'], 'GLB round trip failed'
pres=json.loads((OUT/'verificacao/parametros_e_preservacao.json').read_text(encoding='utf-8'))
pres['original_files_still_unchanged']=all(hashlib.sha256((PARENT/n).read_bytes()).hexdigest()==h for n,h in pres['original_file_sha256'].items())
cams=json.loads((OUT/'verificacao/cameras_comparacao.json').read_text(encoding='utf-8'))
pres['comparisons_have_identical_cameras_and_lighting']=all(
 {k:v for k,v in a.items() if k!='version'}=={k:v for k,v in b.items() if k!='version'}
 for a in cams if a['version']=='antes' for b in cams if b['version']=='depois' and a['view']==b['view'] and a['mode']==b['mode'])
assert pres['original_files_still_unchanged'] and pres['comparisons_have_identical_cameras_and_lighting']
(OUT/'verificacao/parametros_e_preservacao.json').write_text(json.dumps(pres,indent=2,ensure_ascii=False),encoding='utf-8')
# Save a regular .blend with the new version active and the baseline/QA in separate scenes.
bpy.context.window.scene=source
cam=source.camera;cam.location=(.53,-.8,.29)
cam.rotation_euler=(Vector((0,0,.165))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.ortho_scale=.395
source['validation_report']='verificacao/reimportacao.json'
source['revision_report']='RELATORIO_REVISAO.md'
for ob in source.objects:ob.select_set(False)
base.select_set(True);hair.select_set(True);bpy.context.view_layer.objects.active=base
for area in bpy.context.screen.areas:
    if area.type=='VIEW_3D':
        area.spaces.active.region_3d.view_location=(0,0,.165)
        area.spaces.active.region_3d.view_distance=.52
        area.spaces.active.region_3d.view_rotation=cam.rotation_euler.to_quaternion()
        area.spaces.active.clip_start=.001
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'piloto-feminino-01-rosto-r02.blend'))
print('RCL_REVISION_VALIDATED',json.dumps({'passed':report['passed'],'height_m':report['measurements']['head_height_m'],'original_files_unchanged':pres['original_files_still_unchanged'],'identical_comparison_cameras':pres['comparisons_have_identical_cameras_and_lighting']}),flush=True)
