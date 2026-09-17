import { openDB, type DBSchema, type IDBPDatabase } from 'idb';
import type { PartBlob, PartMeta } from '../types';
import { bundledParts, getBundledData } from './catalog';

const DB_NAME = 'montador-3dc';
const DB_VERSION = 2;

export const BASE_SLOT = 'base';
export const HAIR_SLOT = 'hair';

export interface SlotDef {
  id: string;
  name: string;
  hint: string;
}

/** Os únicos slots do app. Não são editáveis pelo usuário. */
export const SLOTS: SlotDef[] = [
  {
    id: BASE_SLOT,
    name: 'Base feminina',
    hint: 'Um .glb por base (cabeça/rosto, sem cabelo).',
  },
  {
    id: HAIR_SLOT,
    name: 'Cabelo',
    hint: 'O corte que fica montado enquanto as bases são trocadas.',
  },
  {
    id: 'eyes',
    name: 'Olhos',
    hint: 'Olho 1 em par, com pálpebras. Compartilhado pelas cinco bases RCL.',
  },
  {
    id: 'nose',
    name: 'Nariz',
    hint: 'Nariz 1 com borda de contato comum às cinco bases RCL.',
  },
];

export interface SlotRecord {
  slotId: string;
  partId: string | null;
}

interface MontadorSchema extends DBSchema {
  parts: { key: string; value: PartMeta };
  blobs: { key: string; value: PartBlob };
  slots: { key: string; value: SlotRecord };
}

/** Formato da v1: categorias livres e `categoryId` no lugar de `slotId`. */
type LegacyPart = Omit<PartMeta, 'slotId'> & { slotId?: string; categoryId?: string };

let dbPromise: Promise<IDBPDatabase<MontadorSchema>> | null = null;

function getDb(): Promise<IDBPDatabase<MontadorSchema>> {
  if (!dbPromise) {
    dbPromise = openDB<MontadorSchema>(DB_NAME, DB_VERSION, {
      async upgrade(db, oldVersion, _newVersion, tx) {
        if (oldVersion < 1) {
          db.createObjectStore('parts', { keyPath: 'id' });
          db.createObjectStore('blobs', { keyPath: 'id' });
        }

        if (oldVersion < 2) {
          // A v1 tinha categorias editáveis e um transform por slot; os dois
          // deixaram de existir, então os stores antigos são refeitos.
          const raw = db as unknown as IDBDatabase;
          for (const name of ['categories', 'slots']) {
            if (raw.objectStoreNames.contains(name)) raw.deleteObjectStore(name);
          }
          db.createObjectStore('slots', { keyPath: 'slotId' });

          if (oldVersion >= 1) {
            const parts = tx.objectStore('parts');
            const blobs = tx.objectStore('blobs');
            (parts as unknown as IDBObjectStore).deleteIndex('byCategory');
            for (const legacy of (await parts.getAll()) as LegacyPart[]) {
              const slotId = legacy.slotId ?? legacy.categoryId;
              const isFixture = legacy.fileName.startsWith('FIXT_');
              if (isFixture || (slotId !== BASE_SLOT && slotId !== HAIR_SLOT)) {
                await parts.delete(legacy.id);
                await blobs.delete(legacy.id);
                continue;
              }
              await parts.put({
                id: legacy.id,
                name: legacy.name,
                slotId,
                fileName: legacy.fileName,
                fileSize: legacy.fileSize,
                addedAt: legacy.addedAt,
              });
            }
          }
        }
      },
    });
  }
  return dbPromise;
}

export function newId(): string {
  return crypto.randomUUID();
}

/* -------------------------------------------------------------------- peças */

/** Ordena como o usuário lê: "base 2" antes de "base 10". */
function byName(a: PartMeta, b: PartMeta): number {
  return a.name.localeCompare(b.name, 'pt-BR', { numeric: true, sensitivity: 'base' });
}

export async function listParts(): Promise<PartMeta[]> {
  const db = await getDb();
  const all = await db.getAll('parts');
  return [...bundledParts, ...all].sort(byName);
}

export async function addPartFromBuffer(
  data: ArrayBuffer,
  info: { slotId: string; name: string; fileName: string },
): Promise<PartMeta> {
  const meta: PartMeta = {
    id: newId(),
    name: info.name,
    slotId: info.slotId,
    fileName: info.fileName,
    fileSize: data.byteLength,
    addedAt: Date.now(),
  };
  const db = await getDb();
  const tx = db.transaction(['parts', 'blobs'], 'readwrite');
  await tx.objectStore('parts').put(meta);
  await tx.objectStore('blobs').put({ id: meta.id, data });
  await tx.done;
  return meta;
}

export async function deletePart(id: string): Promise<void> {
  if (bundledParts.some((part) => part.id === id)) return;
  const db = await getDb();
  const tx = db.transaction(['parts', 'blobs'], 'readwrite');
  await tx.objectStore('parts').delete(id);
  await tx.objectStore('blobs').delete(id);
  await tx.done;
}

/** Devolve os bytes originais, exatamente como foram importados. */
export async function getPartData(id: string): Promise<ArrayBuffer> {
  const bundled = await getBundledData(id);
  if (bundled) return bundled;
  const db = await getDb();
  const record = await db.get('blobs', id);
  if (!record) throw new Error(`Arquivo da peça ${id} não está mais na biblioteca.`);
  return record.data;
}

/* -------------------------------------------------------------------- slots */

export async function loadSelection(): Promise<Record<string, string | null>> {
  const db = await getDb();
  const stored = await db.getAll('slots');
  const byId = new Map(stored.map((s) => [s.slotId, s.partId]));
  const result: Record<string, string | null> = {};
  for (const slot of SLOTS) result[slot.id] = byId.get(slot.id) ?? null;
  return result;
}

export async function saveSelection(slotId: string, partId: string | null): Promise<void> {
  const db = await getDb();
  await db.put('slots', { slotId, partId });
}

/** Tira dos slots a peça que acabou de sair da biblioteca. */
export async function clearSelectionUsingPart(partId: string): Promise<string[]> {
  const db = await getDb();
  const stored = await db.getAll('slots');
  const affected: string[] = [];
  const tx = db.transaction('slots', 'readwrite');
  for (const slot of stored) {
    if (slot.partId === partId) {
      affected.push(slot.slotId);
      await tx.store.put({ ...slot, partId: null });
    }
  }
  await tx.done;
  return affected;
}

/* ------------------------------------------------------------- armazenamento */

export interface StorageInfo {
  usageBytes: number | null;
  quotaBytes: number | null;
  persistent: boolean | null;
}

export async function readStorageInfo(): Promise<StorageInfo> {
  if (!('storage' in navigator)) {
    return { usageBytes: null, quotaBytes: null, persistent: null };
  }
  const estimate = navigator.storage.estimate
    ? await navigator.storage.estimate()
    : { usage: undefined, quota: undefined };
  const persistent = navigator.storage.persisted ? await navigator.storage.persisted() : null;
  return {
    usageBytes: estimate.usage ?? null,
    quotaBytes: estimate.quota ?? null,
    persistent,
  };
}

export async function requestPersistentStorage(): Promise<boolean> {
  if (!('storage' in navigator) || !navigator.storage.persist) return false;
  return navigator.storage.persist();
}
