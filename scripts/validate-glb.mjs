#!/usr/bin/env node
/**
 * Roda o Khronos glTF Validator em um ou mais arquivos .glb.
 *   node scripts/validate-glb.mjs artifacts/personagem.glb
 *
 * O validador não substitui a conferência visual: ele checa a integridade do
 * arquivo, não se o personagem ficou correto.
 */
import { readFile } from 'node:fs/promises';
import { basename, resolve } from 'node:path';

const files = process.argv.slice(2);
if (files.length === 0) {
  console.error('Uso: node scripts/validate-glb.mjs <arquivo.glb> [...]');
  process.exit(2);
}

const mod = await import('gltf-validator');
const validateBytes = mod.validateBytes ?? mod.default?.validateBytes;
if (typeof validateBytes !== 'function') {
  console.error('Não foi possível carregar validateBytes de gltf-validator.');
  process.exit(2);
}

let failed = false;

for (const file of files) {
  const path = resolve(file);
  const bytes = new Uint8Array(await readFile(path));

  const magic = new DataView(bytes.buffer, bytes.byteOffset, 12).getUint32(0, true);
  if (magic !== 0x46546c67) {
    console.error(`${basename(path)}: não começa com o magic "glTF" — não é GLB binário.`);
    failed = true;
    continue;
  }

  const report = await validateBytes(bytes, {
    uri: basename(path),
    externalResourceFunction: (uri) => {
      throw new Error(`Recurso externo referenciado (${uri}); o GLB deveria ser autossuficiente.`);
    },
  });

  const { numErrors, numWarnings, numInfos, numHints } = report.issues;
  console.log(`\n=== ${basename(path)} (${bytes.byteLength} bytes) ===`);
  console.log(`validador ${report.validatorVersion} · gerador: ${report.info?.generator ?? '—'}`);
  if (report.info) {
    console.log(
      `versão glTF ${report.info.version} · ` +
        `desenhos: ${report.info.drawCallCount} · ` +
        `triângulos: ${report.info.totalTriangleCount} · ` +
        `vértices: ${report.info.totalVertexCount} · ` +
        `materiais: ${report.info.materialCount}`,
    );
    if (report.info.resources?.length) {
      // storage: 'glb' (chunk binário), 'buffer-view' (imagem dentro do buffer),
      // 'data-uri' (embutida em base64) ou 'external' (arquivo separado).
      const external = report.info.resources.filter((r) => r.storage === 'external');
      const inside = report.info.resources.length - external.length;
      console.log(`recursos dentro do arquivo: ${inside}; externos: ${external.length}`);
      for (const r of report.info.resources) {
        console.log(`  ${r.pointer} · ${r.storage}${r.mimeType ? ` · ${r.mimeType}` : ''}${r.byteLength ? ` · ${r.byteLength} bytes` : ''}`);
      }
    }
  }
  console.log(`erros: ${numErrors} · avisos: ${numWarnings} · infos: ${numInfos} · dicas: ${numHints}`);

  for (const message of report.issues.messages) {
    console.log(`  [${message.severity === 0 ? 'ERRO' : message.severity === 1 ? 'AVISO' : 'INFO'}] ${message.code} ${message.pointer ?? ''} ${message.message}`);
  }

  if (numErrors > 0) failed = true;
}

process.exit(failed ? 1 : 0);
