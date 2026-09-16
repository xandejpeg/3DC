import { Material, Mesh, Object3D, Texture } from 'three';
import { GLTFLoader, type GLTF } from 'three/examples/jsm/loaders/GLTFLoader.js';
import { clone as cloneWithSkeleton } from 'three/examples/jsm/utils/SkeletonUtils.js';

const loader = new GLTFLoader();

/**
 * Um GLB importado é parseado uma única vez por peça. Cada uso na montagem é um
 * clone que compartilha geometrias, materiais e texturas com o original — por isso
 * trocar uma peça nunca descarta recursos ainda usados por outra.
 */
const cache = new Map<string, Promise<GLTF>>();

export function loadPartGltf(partId: string, data: ArrayBuffer): Promise<GLTF> {
  let pending = cache.get(partId);
  if (!pending) {
    // Cópia defensiva: o arquivo guardado na biblioteca nunca é entregue ao loader.
    pending = loader.parseAsync(data.slice(0), '');
    pending.catch(() => cache.delete(partId));
    cache.set(partId, pending);
  }
  return pending;
}

export function instantiate(gltf: GLTF): Object3D {
  return cloneWithSkeleton(gltf.scene);
}

export function isCached(partId: string): boolean {
  return cache.has(partId);
}

/**
 * Só deve ser chamado quando a peça sai da biblioteca e nenhum clone dela
 * continua na cena.
 */
export async function disposePart(partId: string): Promise<void> {
  const pending = cache.get(partId);
  if (!pending) return;
  cache.delete(partId);
  const gltf = await pending.catch(() => null);
  if (!gltf) return;

  const textures = new Set<Texture>();
  const materials = new Set<Material>();

  gltf.scene.traverse((object) => {
    const mesh = object as Mesh;
    if (mesh.geometry) mesh.geometry.dispose();
    const material = mesh.material;
    if (!material) return;
    for (const m of Array.isArray(material) ? material : [material]) materials.add(m);
  });

  for (const material of materials) {
    for (const value of Object.values(material)) {
      if (value instanceof Texture) textures.add(value);
    }
    material.dispose();
  }
  for (const texture of textures) texture.dispose();
}
