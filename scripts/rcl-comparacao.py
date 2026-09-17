from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
OUT=Path(__file__).resolve().parents[1]/'artifacts/conjunto-feminino-v1'
font=lambda n:ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf',n)
im=Image.new('RGB',(1500,780),'#e8edf1');d=ImageDraw.Draw(im)
d.text((24,12),'3DC · Cinco bases femininas / mesmo cabelo',font=font(28),fill='#203848')
names=['1 · Suave','2 · Angular','3 · Arredondada','4 · Alongada','5 · Maçãs largas']
for i,label in enumerate(names):
    d.text((i*300+18,56),label,font=font(20),fill='#203848')
    for row,mode in enumerate(['base','montada']):
        src=Image.open(OUT/'previas'/f'base-f-{i+1:02d}_{mode}.png').convert('RGBA')
        src.thumbnail((300,335),Image.Resampling.LANCZOS)
        im.paste(src,(i*300+(300-src.width)//2,90+row*340),src)
im.save(OUT/'comparacao.png')
