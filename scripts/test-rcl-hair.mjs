// Exercise the actual application's slot replacement with the delivered GLBs.
// No renderer/browser emulation and no changes to the application's export flow.
import { readFile, writeFile, mkdir } from 'node:fs/promises';
import { resolve } from 'node:path';
import { pathToFileURL } from 'node:url';
import { createHash } from 'node:crypto';
import assert from 'node:assert/strict';
import ts from 'typescript';
import { Group, PerspectiveCamera, Vector3, Box3 } from 'three';
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js';

const compiled = ts.transpileModule(await readFile('src/three/SceneManager.ts','utf8'), {
  compilerOptions:{target:ts.ScriptTarget.ES2022,module:ts.ModuleKind.ESNext},
}).outputText.replace(/from ['"](three(?:\/[^'"]+)?)['"]/g,(_,spec)=>
  `from ${JSON.stringify(pathToFileURL(resolve('node_modules',spec==='three'?'three/build/three.module.js':spec)).href)}`);
const { SceneManager } = await import(`data:text/javascript;base64,${Buffer.from(compiled).toString('base64')}`);
const manifest=JSON.parse(await readFile('public/models/rcl-feminino-v2/manifest.json','utf8'));
const counts=Object.fromEntries(['base','hair','eyes','nose'].map(slot=>[slot,manifest.parts.filter(p=>p.slotId===slot).length]));
assert.deepEqual(counts,{base:5,hair:12,eyes:1,nose:1});
const loader=new GLTFLoader(),loaded=new Map(),assetHashes={};
for(const part of manifest.parts){
  const bytes=await readFile(resolve('public/models/rcl-feminino-v2',part.fileName));
  assert.equal(bytes.byteLength,part.fileSize,part.fileName);
  assetHashes[part.fileName]=createHash('sha256').update(bytes).digest('hex');
  const gltf=await loader.parseAsync(bytes.buffer.slice(bytes.byteOffset,bytes.byteOffset+bytes.byteLength),'');
  loaded.set(part.id,gltf.scene);
}
function fingerprint(root){
  root.updateMatrixWorld(true);
  const hash=createHash('sha256');
  root.traverse(o=>{
    hash.update(JSON.stringify([o.name,o.matrixWorld.elements,o.userData]));
    if(!o.isMesh)return;
    for(const [name,attribute] of Object.entries(o.geometry.attributes)){
      hash.update(name);hash.update(Buffer.from(attribute.array.buffer,attribute.array.byteOffset,attribute.array.byteLength));
    }
    const index=o.geometry.index?.array;if(index)hash.update(Buffer.from(index.buffer,index.byteOffset,index.byteLength));
    for(const m of Array.isArray(o.material)?o.material:[o.material])hash.update(JSON.stringify([m.color.toArray(),m.roughness,m.metalness]));
  });
  return hash.digest('hex');
}
const snapshots=new Map([...loaded].map(([id,o])=>[id,fingerprint(o)]));
const manager=Object.create(SceneManager.prototype);
manager.character=new Group();manager.slots=new Map();manager.camera=new PerspectiveCamera();
manager.camera.position.set(0,.16,1);manager.controls={target:new Vector3(0,.16,0),update(){}};
const bases=manifest.parts.filter(p=>p.slotId==='base'),hairs=manifest.parts.filter(p=>p.slotId==='hair');
const eyes=loaded.get('rcl-v2-eye-01'),nose=loaded.get('rcl-v2-nose-01');
manager.setSlotObject('eyes',eyes);manager.setSlotObject('nose',nose);
const selected=slot=>manager.slots.get(slot)?.children[0];
const results=[];
for(const hair of hairs){
  const object=loaded.get(hair.id);manager.setSlotObject('hair',object);
  for(const base of bases){
    const face=loaded.get(base.id);manager.setSlotObject('base',face);
    assert.equal(selected('hair'),object);assert.equal(selected('eyes'),eyes);assert.equal(selected('nose'),nose);
    assert.equal(manager.character.children.length,4);
    const parts=[];face.traverse(o=>{if(o.userData.module_id)parts.push(o.userData.module_id);});
    for(const kind of ['brow','mouth','ear'])assert.ok(parts.some(id=>id.includes(kind)),`${base.id} lost ${kind}`);
    assert.equal(fingerprint(object),snapshots.get(hair.id));
    assert.equal(fingerprint(face),snapshots.get(base.id));
    const box=new Box3().setFromObject(manager.character);
    results.push({base:base.id,hair:hair.id,kept_eyes_nose:true,kept_fixed_parts:true,bounds:[box.min.toArray(),box.max.toArray()]});
  }
}
// Reverse direction: hair changes must preserve the selected face and all its children.
for(const base of bases){
  const face=loaded.get(base.id);manager.setSlotObject('base',face);
  for(const hair of hairs){
    manager.setSlotObject('hair',loaded.get(hair.id));
    assert.equal(selected('base'),face);assert.equal(selected('eyes'),eyes);assert.equal(selected('nose'),nose);
    assert.equal(fingerprint(face),snapshots.get(base.id));
  }
}
assert.equal(fingerprint(eyes),snapshots.get('rcl-v2-eye-01'));assert.equal(fingerprint(nose),snapshots.get('rcl-v2-nose-01'));
manager.setHairPreviewVisible(false);assert.equal(manager.camera.layers.isEnabled(1),false);
assert.ok(selected('hair').visible);manager.setHairPreviewVisible(true);
for(const view of ['front','side','threeQuarter','back'])manager.setView(view);
const out='artifacts/cabelos-femininos-v1';await mkdir(out,{recursive:true});
await writeFile(`${out}/teste-seletor.json`,JSON.stringify({passed:true,test:'SceneManager real, sem UI/WebGL',counts,base_swaps:60,hair_swaps:60,geometry_unchanged:true,asset_sha256:assetHashes,results},null,2));
console.log('PASS: 12 hairs × 5 faces; 60 face swaps + 60 hair swaps; eyes, nose, fixed parts and geometry preserved.');
