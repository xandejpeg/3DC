from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
R=Path(__file__).resolve().parents[1];O=R/'artifacts/conjunto-feminino-v2';OLD=R/'artifacts/conjunto-feminino-v1'
font=lambda n:ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf',n)
im=Image.new('RGB',(1500,800),'#e8edf1');d=ImageDraw.Draw(im)
d.text((20,12),'3DC · Cinco rostos / mesmo Olho 1, Nariz 1 e Corte 1',font=font(27),fill='#203848')
d.text((20,51),'GLBs reimportados · acima: sem cabelo · abaixo: montagem completa',font=font(18),fill='#486273')
for i,name in enumerate(['1 · Suave','2 · Angular','3 · Arredondada','4 · Alongada','5 · Maçãs largas']):
    d.text((i*300+16,84),name,font=font(19),fill='#203848')
    for row,mode in enumerate(['sem-cabelo','frente']):
        src=Image.open(O/'previas'/f'base-{i+1:02d}-{mode}.png').convert('RGBA');src.thumbnail((300,340))
        im.paste(src,(i*300+(300-src.width)//2,112+row*340),src)
im.save(O/'comparacao.png')
im=Image.new('RGB',(1000,650),'#e8edf1');d=ImageDraw.Draw(im)
d.text((20,12),'Base 1 · antes / depois · mesmas câmeras',font=font(27),fill='#203848')
items=[(OLD/'previas/base-f-01_frente.png','Antes · frente'),(O/'previas/base-01-frente.png','Depois · frente'),(OLD/'previas/base-f-01_montada.png','Antes · três quartos'),(O/'previas/base-01-tres-quartos.png','Depois · três quartos')]
for i,(p,title) in enumerate(items):
    x=(i%2)*500;y=58+(i//2)*292
    d.text((x+20,y),title,font=font(19),fill='#203848')
    src=Image.open(p).convert('RGBA');src.thumbnail((300,267))
    im.paste(src,(x+(500-src.width)//2,y+23),src)
im.save(O/'antes-depois.png')
