import { Object3D, Scene } from 'three';
import { GLTFExporter } from 'three/examples/jsm/exporters/GLTFExporter.js';

const GLB_MAGIC = 0x46546c67; // 'glTF' little-endian

/** Confirma que os bytes são mesmo um container GLB e não JSON renomeado. */
export function assertGlb(buffer: ArrayBuffer, subject = 'O arquivo'): void {
  if (buffer.byteLength < 12) {
    throw new Error(`${subject} é curto demais para ser um GLB.`);
  }
  const header = new DataView(buffer);
  const magic = header.getUint32(0, true);
  const version = header.getUint32(4, true);
  const length = header.getUint32(8, true);
  if (magic !== GLB_MAGIC) {
    throw new Error(`${subject} não começa com o magic "glTF" — não é um GLB binário.`);
  }
  if (version !== 2) {
    throw new Error(`${subject} usa uma versão de container GLB inesperada: ${version}.`);
  }
  if (length !== buffer.byteLength) {
    throw new Error(
      `${subject} declara ${length} bytes no cabeçalho, mas tem ${buffer.byteLength}.`,
    );
  }
}

/**
 * Exporta apenas o grupo do personagem. O grupo é movido para uma cena
 * temporária durante a exportação, de modo que piso, grade, luzes e câmera do
 * visualizador jamais entram no arquivo. Ao final ele volta para o lugar.
 */
export async function exportGroupToGlb(group: Object3D): Promise<ArrayBuffer> {
  const previousParent = group.parent;
  const previousIndex = previousParent ? previousParent.children.indexOf(group) : -1;

  const exportScene = new Scene();
  exportScene.name = 'Personagem';
  exportScene.add(group); // Object3D.add remove o grupo do pai anterior

  try {
    const exporter = new GLTFExporter();
    const result = await exporter.parseAsync(exportScene, {
      binary: true,
      onlyVisible: true,
      trs: true,
      includeCustomExtensions: false,
      // maxTextureSize fica no padrão (Infinity) para não reduzir texturas em silêncio.
    });
    if (!(result instanceof ArrayBuffer)) {
      throw new Error('GLTFExporter não devolveu um ArrayBuffer com binary: true.');
    }
    assertGlb(result, 'O resultado da exportação');
    return result;
  } finally {
    if (previousParent) {
      previousParent.add(group);
      if (previousIndex >= 0 && previousIndex < previousParent.children.length - 1) {
        previousParent.children.splice(previousParent.children.indexOf(group), 1);
        previousParent.children.splice(previousIndex, 0, group);
      }
    } else {
      exportScene.remove(group);
    }
  }
}

export function downloadGlb(buffer: ArrayBuffer, fileName: string): void {
  const blob = new Blob([buffer], { type: 'model/gltf-binary' });
  const url = URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.href = url;
  link.download = fileName;
  document.body.appendChild(link);
  link.click();
  link.remove();
  setTimeout(() => URL.revokeObjectURL(url), 10_000);
}
