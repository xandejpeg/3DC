from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
ROOT=Path(r"C:\Users\xandao\Documents\GitHub\3DC\artifacts\piloto-feminino-01")
def font(size,bold=False):
    return ImageFont.truetype("C:/Windows/Fonts/seguisb.ttf" if bold else "C:/Windows/Fonts/segoeui.ttf",size)
def sheet(filename,items,columns,rows):
    w=1600; panel_w=752; panel_h=810; header=150
    h=header+rows*panel_h+70
    canvas=Image.new("RGB",(w,h),"#edf0f3");d=ImageDraw.Draw(canvas)
    d.text((40,25),"RCL / 3DC  ·  PILOTO FEMININO 01",font=font(20,True),fill="#326777")
    d.text((40,56),"Base feminina 1 + Corte Feminino 1",font=font(38,True),fill="#162532")
    d.text((40,108),"Módulos separados · pescoço incluído · vistas dos GLBs reimportados",font=font(21),fill="#546675")
    for idx,(name,label) in enumerate(items):
        x=32+(idx%columns)*784;y=header+(idx//columns)*panel_h
        d.rounded_rectangle((x,y,x+panel_w,y+panel_h-20),radius=16,fill="#e2e8ed",outline="#cbd5df")
        d.text((x+26,y+18),label,font=font(25,True),fill="#20384c")
        im=Image.open(ROOT/"imagens"/name).convert("RGBA")
        im.thumbnail((panel_w-38,panel_h-88),Image.Resampling.LANCZOS)
        canvas.paste(im,(x+(panel_w-im.width)//2,y+55+(panel_h-88-im.height)//2),im)
    d.text((40,h-47),"0,24 m do queixo ao crânio · interfaces faciais provisórias · sem componentes faciais",font=font(21),fill="#546675")
    canvas.save(ROOT/"imagens"/filename)
sheet("quatro_vistas.png",[("frente.png","01  Frente"),("perfil.png","02  Perfil"),("tres_quartos.png","03  Três quartos"),("costas.png","04  Costas")],2,2)
sheet("modulos_separados.png",[("base_isolada.png","01  Base com pescoço"),("cabelo_isolado.png","02  Cabelo isolado")],2,1)
print("Pranchas criadas a partir dos renders, sem alteração da geometria ou retoque.")
