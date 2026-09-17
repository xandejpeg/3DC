import bpy,json
from pathlib import Path
from mathutils import Vector
OUT=Path(r'C:\Users\xandao\Documents\GitHub\3DC\artifacts\piloto-feminino-01\revisao-rosto-02')
views=[('frente',(0,-.9,.165)),('perfil',(.9,0,.165)),('tres_quartos',(.53,-.8,.29)),('costas',(0,.9,.165))]
target=Vector((0,0,.165));manifest=[]
for view,pos in views:
    for label,scene_name in [('antes','RCL_R02_ANTES'),('depois','RCL_R02_DEPOIS')]:
        s=bpy.data.scenes[scene_name];bpy.context.window.scene=s
        hair=next(o for o in s.objects if o.get('module_id')=='hair-f-01')
        s.render.resolution_x=900;s.render.resolution_y=1000;s.render.resolution_percentage=100
        s.render.image_settings.file_format='PNG';s.render.image_settings.color_mode='RGBA';s.render.film_transparent=True
        s.eevee.taa_render_samples=128
        cam=s.camera;cam.data.ortho_scale=.395;cam.location=pos
        cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler()
        for mode in ['base','montada']:
            hair.hide_render=(mode=='base')
            s.render.filepath=str(OUT/'imagens'/f'{label}_{mode}_{view}.png')
            bpy.ops.render.render(write_still=True)
            manifest.append({'version':label,'mode':mode,'view':view,'camera_position':list(cam.location),'camera_rotation':list(cam.rotation_euler),'ortho_scale':cam.data.ortho_scale,'resolution':[900,1000],'world':s.world.name,'view_transform':s.view_settings.view_transform,'exposure':s.view_settings.exposure,'gamma':s.view_settings.gamma,'lights':[{'name':o.data.name,'position':list(o.location),'rotation':list(o.rotation_euler),'energy':o.data.energy,'size':o.data.size} for o in s.objects if o.type=='LIGHT']})
        hair.hide_render=False
        print('RCL_RENDER_COMPLETE',label,view,flush=True)
(OUT/'verificacao/cameras_comparacao.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
print('RCL_COMPARISON_COMPLETE',flush=True)
