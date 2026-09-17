"""Publish only validated hair checkpoints and build a compact visual comparison.

Run with normal Python after Blender delivery. Existing base/eye/nose/hair-1
entries are retained byte-for-byte in the manifest; no runtime export changes.
"""
import json,hashlib
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
R=Path(__file__).resolve().parents[1];O=R/'artifacts/cabelos-femininos-v1';P=R/'public/models/rcl-feminino-v2'
manifest=json.loads((P/'manifest.json').read_text(encoding='utf8'))
old={p['id']:p for p in manifest['parts']}
reports=[]
for cut in range(2,13):
    d=O/f'corte-{cut:02d}';report=json.loads((d/'progresso.json').read_text(encoding='utf8'))
    assert report['status'] in ('validated','integrated'),(cut,report['status'])
    assert report['roundtrip_geometry_equal'] and report['roundtrip_materials_equal']
    assert all(not any(c.values()) for c in report['intersections'].values())
    file=f'corte-feminino-{cut:02d}.glb';src=d/file
    assert src.read_bytes()==(P/file).read_bytes()
    report['sha256']=hashlib.sha256(src.read_bytes()).hexdigest()
    report['bytes']=src.stat().st_size
    old[f'rcl-v2-hair-{cut:02d}']={
        'id':f'rcl-v2-hair-{cut:02d}','slotId':'hair','name':f'Corte Feminino {cut}',
        'fileName':file,'fileSize':report['bytes']}
    reports.append(report)
manifest['parts']=sorted(old.values(),key=lambda p:(['base','hair','eyes','nose'].index(p['slotId']),int(p['id'].rsplit('-',1)[1])))
(P/'manifest.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+'\n',encoding='utf8')
(O/'catalogo.json').write_text(json.dumps({'product':'3DC Lab v1','cuts':reports},indent=2,ensure_ascii=False)+'\n',encoding='utf8')

# Keep original references untouched: this sheet only lays out scaled copies.
font=lambda n:ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf',n)
im=Image.new('RGB',(1260,1530),'#e8edf1');draw=ImageDraw.Draw(im)
draw.text((24,14),'3DC Lab v1 · cortes femininos 2–12',font=font(28),fill='#203848')
draw.text((24,55),'Referência isolada | montagem na mesma Base 1, Olho 1 e Nariz 1',font=font(19),fill='#486273')
for i,report in enumerate(reports):
    cut=report['cut'];x=18+(i%3)*414;y=102+(i//3)*354
    draw.rounded_rectangle((x,y,x+400,y+339),radius=10,fill='#f6f8fa')
    draw.text((x+12,y+7),f'Corte {cut} · {report["label"]}',font=font(15),fill='#203848')
    ref=Image.open(R/f'docs/referencias-rcl/originais/R{51+cut:03d}.jpeg').convert('RGB');ref.thumbnail((160,220))
    im.paste(ref,(x+8,y+65+(220-ref.height)//2))
    preview=Image.open(O/f'corte-{cut:02d}/frente.png').convert('RGBA');preview.thumbnail((234,295))
    im.paste(preview,(x+168+(228-preview.width)//2,y+35),preview)
    draw.text((x+28,y+310),'Referência',font=font(14),fill='#486273')
    draw.text((x+223,y+310),'Montagem',font=font(14),fill='#486273')
x=18+2*414;y=102+3*354
draw.text((x+10,y+35),'11 novos GLBs independentes',font=font(23),fill='#203848')
draw.text((x+10,y+85),'5 bases · 12 cortes no seletor',font=font(21),fill='#203848')
draw.text((x+10,y+133),'Corte 1 e peças faciais preservados.',font=font(17),fill='#486273')
draw.text((x+10,y+178),'Frente comum; laterais e costas',font=font(17),fill='#486273')
draw.text((x+10,y+204),'nos checkpoints de cada corte.',font=font(17),fill='#486273')
draw.text((x+10,y+251),'Volumes ocultos ainda estimados.',font=font(17),fill='#486273')
im.save(O/'comparacao-referencias.jpg',quality=92)
im=Image.new('RGB',(1320,1040),'#e8edf1');draw=ImageDraw.Draw(im)
for idx,(cut,view) in enumerate((c,v) for c in range(2,13) for v in ('perfil','costas')):
    x=220*(idx%6);y=260*(idx//6)
    draw.text((x+10,y+6),f'Corte {cut} / {view}',font=font(17),fill='#203848')
    src=Image.open(O/f'corte-{cut:02d}/{view}.png').convert('RGBA');src.thumbnail((220,230))
    im.paste(src,(x+(220-src.width)//2,y+28),src)
im.save(O/'conferencia-perfil-costas.jpg',quality=88)
print('11 cabelos validados publicados no catálogo; comparação salva.')
