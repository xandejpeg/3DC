import type { PartMeta } from '../types';
import manifest from '../../public/models/rcl-feminino-v2/manifest.json';

// "v2" is the asset revision; the product is still 3DC Lab v1.

export const bundledParts: PartMeta[] = manifest.parts.map((part) => ({
  ...part,
  bundled: true,
  addedAt: 0,
}));

/** Keep the selected face when upgrading the included V1 set. Imported files keep their IDs. */
export function currentBundledId(id: string | null | undefined): string | null {
  if (!id) return null;
  const upgraded = id.replace(/^rcl-v1-/, 'rcl-v2-');
  return bundledParts.some((part) => part.id === upgraded) ? upgraded : id;
}

export async function getBundledData(id: string): Promise<ArrayBuffer | null> {
  const part = bundledParts.find((item) => item.id === id);
  if (!part) return null;
  const response = await fetch(`${import.meta.env.BASE_URL}models/rcl-feminino-v2/${part.fileName}`);
  if (!response.ok) throw new Error(`Não foi possível carregar ${part.name} (${response.status}).`);
  return response.arrayBuffer();
}
