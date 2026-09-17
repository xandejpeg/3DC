// Non-UI integration test: real application slot manager, bundled GLBs and exporter.
import { readFile, writeFile, mkdir } from 'node:fs/promises';
import { resolve } from 'node:path';
import { pathToFileURL } from 'node:url';
import assert from 'node:assert/strict';
import ts from 'typescript';
import { Group, Box3, Vector3, PerspectiveCamera } from 'three';
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js';

async function appModule(file) {
  const source = await readFile(file, 'utf8');
  const compiled = ts.transpileModule(source, { compilerOptions: { target: ts.ScriptTarget.ES2022, module: ts.ModuleKind.ESNext } }).outputText
    .replace(/from ['"](three(?:\/[^'"]+)?)['"]/g, (_, spec) => `from ${JSON.stringify(pathToFileURL(resolve('node_modules', spec === 'three' ? 'three/build/three.module.js' : spec)).href)}`);
  return import(`data:text/javascript;base64,${Buffer.from(compiled).toString('base64')}`);
}
globalThis.FileReader = class {
  readAsArrayBuffer(blob) { blob.arrayBuffer().then(result => { this.result = result; this.onloadend?.(); }).catch(error => this.onerror?.(error)); }
};
const { SceneManager } = await appModule('src/three/SceneManager.ts');
const { exportGroupToGlb } = await appModule('src/lib/exportGlb.ts');
const loader = new GLTFLoader();
const load = async (name) => {
  const bytes = await readFile(resolve('public/models/rcl-feminino-v2', name));
  return loader.parseAsync(bytes.buffer.slice(bytes.byteOffset, bytes.byteOffset + bytes.byteLength), '');
};
const signature = (root) => {
  root.updateMatrixWorld(true);
  const list = [];
  root.traverse(o => {
    if (!o.isMesh) return;
    const p=o.geometry.attributes.position,index=o.geometry.index;
    const triangles=[];
    for(let i=0;i<(index?.count ?? p.count);i+=3){
      const tri=[];
      for(let j=0;j<3;j++){
        const v=new Vector3().fromBufferAttribute(p,index ? index.getX(i+j) : i+j).applyMatrix4(o.matrixWorld);
        tri.push(v.toArray().map(n=>n.toFixed(6)).join(','));
      }
      triangles.push(tri.sort().join('|'));
    }
    list.push({triangles:triangles.sort(),color:o.material.color.toArray().map(n=>n.toFixed(6)),roughness:o.material.roughness});
  });
  return list.sort((a,b)=>JSON.stringify(a).localeCompare(JSON.stringify(b)));
};
// Skip the renderer constructor: test assembly/export without browser automation.
const manager=Object.create(SceneManager.prototype);
manager.character=new Group();manager.slots=new Map();
manager.camera=new PerspectiveCamera();manager.camera.position.set(0,.16,1);
manager.controls={target:new Vector3(0,.16,0),update(){}};
const hair=(await load('corte-feminino-01.glb')).scene;
manager.setSlotObject('hair',hair);manager.setHairPreviewVisible(true);
const hairSignature=signature(hair),uuid=hair.uuid;
const eyes=(await load('olho-01-par.glb')).scene;
const nose=(await load('nariz-01.glb')).scene;
manager.setSlotObject('eyes',eyes);manager.setSlotObject('nose',nose);
const shared=[['hair',hair],['eyes',eyes],['nose',nose]].map(([slot,obj])=>({slot,obj,uuid:obj.uuid,signature:signature(obj)}));
const results=[];
const out=resolve('artifacts/conjunto-feminino-v2/exportacoes-app');await mkdir(out,{recursive:true});
for(let i=1;i<=5;i++){
  const base=(await load(`base-feminina-${String(i).padStart(2,'0')}.glb`)).scene;
  manager.setSlotObject('base',base);
  assert.equal(manager.character.children.length,4);
  for(const item of shared){
    assert.equal(manager.slots.get(item.slot).children[0].uuid,item.uuid);
    assert.deepEqual(signature(item.obj),item.signature);
  }
  assert.equal(manager.slots.get('hair').children[0].uuid,uuid);
  assert.deepEqual(signature(hair),hairSignature);
  for(const view of ['front','side','threeQuarter','back'])manager.setView(view);
  manager.setHairPreviewVisible(false);
  assert.equal(manager.camera.layers.isEnabled(1),false);
  assert.equal(hair.visible,true); // isolated preview must not discard hair on export
  const before=signature(manager.character);
  const buffer=await exportGroupToGlb(manager.character);
  const imported=(await loader.parseAsync(buffer,'')).scene;
  assert.deepEqual(signature(imported),before);
  assert.equal(manager.slots.get('hair').children[0],hair);
  const box=new Box3().setFromObject(imported);
  await writeFile(resolve(out,`base-${i}-corte-1.glb`),Buffer.from(buffer));
  manager.setHairPreviewVisible(true);
  results.push({base:i,hair_same_instance:true,eyes_same_instance:true,nose_same_instance:true,shared_geometry_unchanged:true,export_reimport_equal:true,bounds:[box.min.toArray(),box.max.toArray()]});
}
manager.setSlotObject('base',null);assert.equal(manager.character.children.length,3);
assert.equal(manager.slots.get('hair').children[0],hair);
await writeFile(resolve(out,'resultado.json'),JSON.stringify({test:'non-UI application integration',passed:true,results},null,2));
console.log('PASS: five base swaps; hair/eye/nose instances and geometry preserved; hidden-hair preview; app export/reimport positions, triangles and materials.');
