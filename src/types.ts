export interface PartMeta {
  id: string;
  name: string;
  slotId: string;
  fileName: string;
  fileSize: number;
  addedAt: number;
  /** Peça incluída no projeto, disponível sem importação manual. */
  bundled?: boolean;
}

export interface PartBlob {
  id: string;
  data: ArrayBuffer;
}

export type SlotStatus =
  | { state: 'idle' }
  | { state: 'loading' }
  | { state: 'error'; message: string };
