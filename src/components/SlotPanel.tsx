import { useRef, useState } from 'react';
import type { SlotDef } from '../lib/db';
import type { PartMeta, SlotStatus } from '../types';

interface SlotPanelProps {
  slot: SlotDef;
  parts: PartMeta[];
  selectedId: string | null;
  status: SlotStatus;
  busy: boolean;
  /** só a base ganha ◀ ▶: o cabelo fica montado e imóvel */
  showCycler: boolean;
  onImport: (files: File[]) => void;
  onSelect: (partId: string) => void;
  onDelete: (part: PartMeta) => void;
  onStep: (direction: -1 | 1) => void;
}

function formatBytes(bytes: number): string {
  if (bytes < 1024) return `${bytes} B`;
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
  return `${(bytes / (1024 * 1024)).toFixed(2)} MB`;
}

export function SlotPanel(props: SlotPanelProps) {
  const { slot, parts, selectedId, status, busy, showCycler, onImport, onSelect, onDelete, onStep } =
    props;

  const fileInput = useRef<HTMLInputElement>(null);
  const [dragging, setDragging] = useState(false);

  const index = parts.findIndex((part) => part.id === selectedId);
  const current = index >= 0 ? parts[index] : null;

  return (
    <section className="slot">
      <div className="slot-header">
        <h2>{slot.name}</h2>
        {parts.length > 0 && (
          <span className="badge">
            {index >= 0 ? `${index + 1} / ${parts.length}` : `${parts.length} arquivo(s)`}
          </span>
        )}
        {status.state === 'loading' && <span className="badge loading">carregando…</span>}
        {status.state === 'error' && <span className="badge error">erro</span>}
      </div>

      {showCycler && (
        <div className="slot-picker">
          <button
            type="button"
            disabled={parts.length < 2}
            aria-label={`Base anterior de ${slot.name}`}
            onClick={() => onStep(-1)}
          >
            ◀
          </button>
          <span className="slot-name">{current ? current.name : 'Nenhuma base montada'}</span>
          <button
            type="button"
            disabled={parts.length < 2}
            aria-label={`Próxima base de ${slot.name}`}
            onClick={() => onStep(1)}
          >
            ▶
          </button>
        </div>
      )}

      {status.state === 'error' && <p className="error-text">{status.message}</p>}

      <ul className="part-list">
        {parts.map((part) => (
          <li key={part.id} className={part.id === selectedId ? 'active' : ''}>
            <button
              type="button"
              className="part-pick"
              aria-pressed={part.id === selectedId}
              onClick={() => onSelect(part.id)}
            >
              <span className="part-name">{part.name}</span>
              <span className="file-name" title={part.fileName}>
                {part.fileName} · {formatBytes(part.fileSize)}
              </span>
            </button>
            {!part.bundled && (
              <button
                type="button"
                className="danger"
                disabled={busy}
                aria-label={`Remover ${part.name}`}
                onClick={() => onDelete(part)}
              >
                Remover
              </button>
            )}
          </li>
        ))}
      </ul>

      <div
        className={dragging ? 'drop dragging' : 'drop'}
        onDragOver={(event) => {
          event.preventDefault();
          setDragging(true);
        }}
        onDragLeave={() => setDragging(false)}
        onDrop={(event) => {
          event.preventDefault();
          setDragging(false);
          const files = Array.from(event.dataTransfer.files);
          if (files.length > 0) onImport(files);
        }}
      >
        <input
          ref={fileInput}
          type="file"
          accept=".glb,model/gltf-binary"
          multiple
          disabled={busy}
          aria-label={`Importar .glb para ${slot.name}`}
          onChange={(event) => {
            const files = Array.from(event.target.files ?? []);
            if (files.length > 0) onImport(files);
            event.target.value = '';
          }}
        />
        <p className="hint">Arraste os .glb aqui ou escolha os arquivos. {slot.hint}</p>
      </div>
    </section>
  );
}
