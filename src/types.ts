export interface PartMeta {
  id: string;
  name: string;
  slotId: string;
  fileName: string;
  fileSize: number;
  addedAt: number;
}

export interface PartBlob {
  id: string;
  data: ArrayBuffer;
}

export type SlotStatus =
  | { state: 'idle' }
  | { state: 'loading' }
  | { state: 'error'; message: string };
