from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
OUT=Path(r'C:\Users\xandao\Documents\GitHub\3DC\artifacts\piloto-feminino-01\revisao-rosto-02')
def font(n,bold=False):return ImageFont.truetype('C:/Windows/Fonts/seguisb.ttf' if bold else 'C:/Windows/Fonts/segoeui.ttf',n)
labels={'frente':'Frente','perfil':'Perfil','tres_quartos':'Três quartos','costas':'Costas'}
def sheet(name,views,modes):
    pw=390;ph=470;top=142;left=30
    width=left*2+pw*len(modes)*2;height=top+ph*len(views)+48
    im=Image.new('RGB',(width,height),'#eef1f4');d=ImageDraw.Draw(im)
    d.text((30,18),'RCL / 3DC · Revisão limitada do rosto',font=font(29,True),fill='#1d3345')
    d.text((30,62),'Mesmas câmeras, escala de enquadramento, materiais e iluminação',font=font(21),fill='#536977')
    for k,mode in enumerate(modes):
        for v,version in enumerate(['antes','depois']):
            x=left+(k*2+v)*pw
            label=('Base isolada' if mode=='base' else 'Montagem')+' · '+version.upper()
            d.text((x+12,108),label,font=font(22,True),fill='#386b78' if v else '#526574')
            for row,view in enumerate(views):
                y=top+row*ph
                d.rounded_rectangle((x+3,y,x+pw-3,y+ph-9),radius=12,fill='#e1e8ee')
                d.text((x+15,y+9),labels[view],font=font(19),fill='#506476')
                src=Image.open(OUT/'imagens'/f'{version}_{mode}_{view}.png').convert('RGBA')
                src.thumbnail((pw-16,ph-40),Image.Resampling.LANCZOS)
                im.paste(src,(x+(pw-src.width)//2,y+30+(ph-40-src.height)//2),src)
    d.text((30,height-36),'Cabelo e encaixe craniano preservados · 24 cm tratados como referência provisória',font=font(20),fill='#536977')
    im.save(OUT/'imagens'/name)
sheet('antes_depois_resumo.png',['frente','tres_quartos'],['base','montada'])
sheet('antes_depois_base.png',list(labels),['base'])
sheet('antes_depois_montagem.png',list(labels),['montada'])
print('Pranchas compostas com os renders, sem retoque da forma.')
