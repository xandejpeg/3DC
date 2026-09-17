"""Archive the supplied reference inventory without changing any original image.

Run once on the machine holding inventory.absolute_path. Already archived images
are verified and reused on any clone. No image generation or visual re-analysis.
"""
from pathlib import Path
import hashlib,json,shutil,re

ROOT=Path(__file__).resolve().parents[1]
DOC=ROOT/'docs/referencias-rcl'
inventory=json.loads((DOC/'Inventario_completo_referencias_RCL.json').read_text(encoding='utf8'))
out=DOC/'originais';out.mkdir(exist_ok=True)
catalog=[]
lines=['# Referências originais do catálogo RCL','',
       'Cópias binárias verificadas pelos SHA-256 do inventário recebido. A numeração R001–R100 segue a ordem desse inventário; não representa novos modelos. Nomes curtos evitam caminhos excessivamente longos no Windows. Os arquivos originais externos não foram alterados.','',
       '| ID / imagem | Caminho original relativo a Imagem base |','| --- | --- |']
for i,entry in enumerate(inventory['files'],1):
    ident=f'R{i:03d}';filename=ident+Path(entry['path']).suffix.lower();dest=out/filename
    if not dest.exists():
        source=Path(entry['absolute_path'])
        assert hashlib.sha256(source.read_bytes()).hexdigest()==entry['sha256'],source
        shutil.copy2(source,dest)
    assert hashlib.sha256(dest.read_bytes()).hexdigest()==entry['sha256'],dest
    catalog.append({'id':ident,'path':'originais/'+filename,'original_path':entry['path'],'sha256':entry['sha256'],'bytes':dest.stat().st_size})
    lines.append(f"| [{ident}]({filename}) | {entry['path']} |")
(DOC/'Catalogo_portatil.json').write_text(json.dumps({'root':'.','count':len(catalog),'files':catalog},ensure_ascii=False,indent=2)+'\n',encoding='utf8')
(out/'README.md').write_text('\n'.join(lines)+'\n',encoding='utf8')
# Keep contract citations navigable on GitHub and on another computer.
contract=DOC/'Contrato_pecas_interfaces_RCL.md';text=contract.read_text(encoding='utf8')
byid={e['id']:e['path'] for e in catalog}
text=re.sub(r'^\[(R\d{3})\]: .*$',lambda m:f'[{m[1]}]: <{byid[m[1]]}>',text,flags=re.M)
contract.write_text(text,encoding='utf8')
print(f'{len(catalog)} referências arquivadas; todos os hashes conferem.')
