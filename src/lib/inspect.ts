import {
  Bone,
  Material,
  Mesh,
  Object3D,
  RGBAFormat,
  SkinnedMesh,
  Texture,
} from 'three';

export interface ExportStats {
  nodes: number;
  meshes: number;
  skinnedMeshes: number;
  points: number;
  lines: number;
  triangles: number;
  vertices: number;
  materials: number;
  textures: number;
  morphTargets: number;
  maxDepth: number;
}

export interface ExportReport {
  stats: ExportStats;
  /** o que será preservado, com números */
  preserved: string[];
  /** sai diferente do original, mas exporta */
  warnings: string[];
  /** impede a exportação por gerar arquivo inválido ou erro no exportador */
  blockers: string[];
}

const GLTF_FRIENDLY = new Set([
  'MeshStandardMaterial',
  'MeshPhysicalMaterial',
  'MeshBasicMaterial',
]);

function imageIsCanvasDrawable(image: unknown): boolean {
  if (!image) return false;
  if (typeof HTMLImageElement !== 'undefined' && image instanceof HTMLImageElement) return true;
  if (typeof HTMLCanvasElement !== 'undefined' && image instanceof HTMLCanvasElement) return true;
  if (typeof ImageBitmap !== 'undefined' && image instanceof ImageBitmap) return true;
  if (typeof OffscreenCanvas !== 'undefined' && image instanceof OffscreenCanvas) return true;
  return false;
}

/**
 * Percorre o que será exportado e descreve, antes de gerar o arquivo, o que é
 * preservado e o que fica fora do suporte validado desta V1.
 *
 * @param root grupo do personagem
 * @param animationsByPart quantidade de clipes de animação presentes em cada GLB em uso
 */
export function inspectForExport(
  root: Object3D,
  animationsByPart: { partName: string; clips: number }[],
): ExportReport {
  const stats: ExportStats = {
    nodes: 0,
    meshes: 0,
    skinnedMeshes: 0,
    points: 0,
    lines: 0,
    triangles: 0,
    vertices: 0,
    materials: 0,
    textures: 0,
    morphTargets: 0,
    maxDepth: 0,
  };

  const warnings = new Set<string>();
  const blockers = new Set<string>();

  const materials = new Set<Material>();
  const textures = new Set<Texture>();
  const graphNodes = new Set<Object3D>();

  root.traverseVisible((object) => graphNodes.add(object));

  root.traverseVisible((object) => {
    stats.nodes++;
    let depth = 0;
    for (let p = object.parent; p && p !== root.parent; p = p.parent) depth++;
    stats.maxDepth = Math.max(stats.maxDepth, depth);

    const asMesh = object as Mesh;
    const isMeshLike = asMesh.isMesh || (object as never as { isPoints?: boolean }).isPoints || (object as never as { isLine?: boolean }).isLine;
    if (!isMeshLike) return;

    if ((object as never as { isPoints?: boolean }).isPoints) stats.points++;
    else if ((object as never as { isLine?: boolean }).isLine) stats.lines++;
    else stats.meshes++;

    const geometry = asMesh.geometry;
    if (geometry) {
      const position = geometry.getAttribute('position');
      if (position) stats.vertices += position.count;
      if (asMesh.isMesh) {
        stats.triangles += geometry.index
          ? geometry.index.count / 3
          : position
            ? position.count / 3
            : 0;
      }
      if (geometry.morphAttributes) {
        const names = Object.keys(geometry.morphAttributes);
        const unsupported = names.filter((n) => n !== 'position' && n !== 'normal');
        stats.morphTargets += geometry.morphAttributes.position?.length ?? 0;
        if (unsupported.length > 0) {
          warnings.add(
            `Morph targets em atributos ${unsupported.join(', ')} serão descartados: o GLTFExporter só grava POSITION e NORMAL.`,
          );
        }
      }
    }

    if ((object as SkinnedMesh).isSkinnedMesh) {
      stats.skinnedMeshes++;
      const skinned = object as SkinnedMesh;
      const bones: Bone[] = skinned.skeleton?.bones ?? [];
      if (bones.length === 0) {
        blockers.add(
          `"${skinned.name || 'malha sem nome'}" é SkinnedMesh sem ossos no esqueleto; o exportador geraria um skin inválido.`,
        );
      } else {
        const missing = bones.filter((bone) => !graphNodes.has(bone));
        if (missing.length > 0) {
          blockers.add(
            `"${skinned.name || 'malha sem nome'}" usa ${missing.length} osso(s) que não estão dentro da peça exportada. ` +
              'O glTF sairia com joints indefinidos. Exporte o GLB de origem com o esqueleto completo dentro do arquivo.',
          );
        } else {
          warnings.add(
            'Há skinning na montagem. O esqueleto e os pesos são exportados, mas nenhuma animação acompanha o arquivo nesta V1.',
          );
        }
      }
    }

    const material = asMesh.material;
    if (!material) return;
    for (const m of Array.isArray(material) ? material : [material]) materials.add(m);
  });

  for (const material of materials) {
    stats.materials++;
    if (material.type === 'ShaderMaterial' || material.type === 'RawShaderMaterial') {
      warnings.add(
        `Material "${material.name || material.type}" é ShaderMaterial. O GLTFExporter avisa "not supported" e grava a malha sem esse material.`,
      );
    } else if (!GLTF_FRIENDLY.has(material.type)) {
      warnings.add(
        `Material "${material.name || material.type}" (${material.type}) não tem equivalente direto em glTF. ` +
          'Ele é gravado como PBR metallic-roughness aproximado; só as propriedades compatíveis sobrevivem.',
      );
    }

    for (const value of Object.values(material)) {
      if (value instanceof Texture) textures.add(value);
    }
  }

  for (const texture of textures) {
    stats.textures++;
    const anyTexture = texture as unknown as {
      isCompressedTexture?: boolean;
      isDataTexture?: boolean;
      isVideoTexture?: boolean;
    };
    if (anyTexture.isCompressedTexture) {
      blockers.add(
        `Textura "${texture.name || 'sem nome'}" é comprimida (KTX2/Basis/DDS). O GLTFExporter lança "Invalid image type" sem um textureUtils, que esta V1 não injeta.`,
      );
    } else if (anyTexture.isVideoTexture) {
      blockers.add(`Textura "${texture.name || 'sem nome'}" é de vídeo e não tem representação em glTF.`);
    } else if (anyTexture.isDataTexture) {
      if (texture.format !== RGBAFormat) {
        blockers.add(
          `Textura de dados "${texture.name || 'sem nome'}" não está em RGBAFormat; o exportador só aceita RGBA nesse caso.`,
        );
      }
    } else if (!imageIsCanvasDrawable(texture.image)) {
      blockers.add(
        `Textura "${texture.name || 'sem nome'}" tem imagem em formato que o exportador não consegue desenhar em canvas.`,
      );
    }
  }

  for (const { partName, clips } of animationsByPart) {
    if (clips > 0) {
      warnings.add(
        `"${partName}" traz ${clips} clipe(s) de animação. Animação está fora do escopo desta V1 e não será gravada no arquivo exportado.`,
      );
    }
  }

  if (stats.meshes + stats.points + stats.lines === 0) {
    blockers.add('Nenhuma peça selecionada: não há nada para exportar.');
  }

  const preserved: string[] = [
    `${stats.nodes} nós de hierarquia (profundidade máxima ${stats.maxDepth}), sem achatamento`,
    `${stats.meshes} malha(s), ${Math.round(stats.triangles)} triângulos, ${stats.vertices} vértices`,
    `${stats.materials} material(is) e ${stats.textures} textura(s) embutidas no .glb`,
  ];
  if (stats.skinnedMeshes > 0) {
    preserved.push(`${stats.skinnedMeshes} malha(s) com skin e seus esqueletos`);
  }
  if (stats.morphTargets > 0) {
    preserved.push(`${stats.morphTargets} morph target(s) de posição`);
  }
  if (stats.points > 0) preserved.push(`${stats.points} objeto(s) Points`);
  if (stats.lines > 0) preserved.push(`${stats.lines} objeto(s) Line`);
  preserved.push('Posição, rotação e escala de cada peça como vieram do arquivo importado');

  return {
    stats,
    preserved,
    warnings: [...warnings],
    blockers: [...blockers],
  };
}
