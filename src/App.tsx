import { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import { ExportDialog } from './components/ExportDialog';
import { SlotPanel } from './components/SlotPanel';
import { Viewer } from './components/Viewer';
import {
  addPartFromBuffer,
  BASE_SLOT,
  clearSelectionUsingPart,
  deletePart,
  getPartData,
  listParts,
  loadSelection,
  newId,
  readStorageInfo,
  requestPersistentStorage,
  saveSelection,
  SLOTS,
  type StorageInfo,
} from './lib/db';
import { assertGlb, downloadGlb, exportGroupToGlb } from './lib/exportGlb';
import { inspectForExport, type ExportReport } from './lib/inspect';
import { disposePart, instantiate, loadPartGltf } from './lib/partCache';
import { STORAGE_NOTE } from './limits';
import { bundledParts, currentBundledId } from './lib/catalog';
import type { SceneManager } from './three/SceneManager';
import type { PartMeta, SlotStatus } from './types';

function describeError(error: unknown): string {
  if (error instanceof Error) return error.message;
  return String(error);
}

function formatBytes(bytes: number): string {
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
  return `${(bytes / (1024 * 1024)).toFixed(2)} MB`;
}

export default function App() {
  const managerRef = useRef<SceneManager | null>(null);
  const selectionRef = useRef<Record<string, string | null>>({});
  const tokensRef = useRef(new Map<string, number>());
  const animationsRef = useRef(new Map<string, number>());
  const framedRef = useRef(false);

  const [ready, setReady] = useState(false);
  const [parts, setParts] = useState<PartMeta[]>([]);
  const [selection, setSelection] = useState<Record<string, string | null>>({});
  const [status, setStatus] = useState<Record<string, SlotStatus>>({});
  const [busy, setBusy] = useState(false);
  const [notice, setNotice] = useState<string | null>(null);
  const [storage, setStorage] = useState<StorageInfo | null>(null);
  const [gridVisible, setGridVisible] = useState(true);
  const [hairPreviewVisible, setHairPreviewVisible] = useState(true);
  const [report, setReport] = useState<ExportReport | null>(null);
  const [exportBusy, setExportBusy] = useState(false);
  const [exportError, setExportError] = useState<string | null>(null);

  const partsById = useMemo(() => new Map(parts.map((part) => [part.id, part])), [parts]);
  const partsBySlot = useMemo(() => {
    const map: Record<string, PartMeta[]> = {};
    for (const slot of SLOTS) map[slot.id] = parts.filter((part) => part.slotId === slot.id);
    return map;
  }, [parts]);

  const refreshStorage = useCallback(() => {
    readStorageInfo().then(setStorage).catch(() => setStorage(null));
  }, []);

  /* ------------------------------------------------------------ montagem */

  const mountPart = useCallback(async (slotId: string, partId: string | null) => {
    const manager = managerRef.current;
    if (!manager) return;

    const token = (tokensRef.current.get(slotId) ?? 0) + 1;
    tokensRef.current.set(slotId, token);
    const isCurrent = () => tokensRef.current.get(slotId) === token;

    if (!partId) {
      manager.setSlotObject(slotId, null);
      setStatus((prev) => ({ ...prev, [slotId]: { state: 'idle' } }));
      return;
    }

    setStatus((prev) => ({ ...prev, [slotId]: { state: 'loading' } }));
    try {
      const data = await getPartData(partId);
      const gltf = await loadPartGltf(partId, data);
      // Uma troca mais recente já aconteceu: descarta este resultado.
      if (!isCurrent()) return;
      animationsRef.current.set(partId, gltf.animations.length);
      manager.setSlotObject(slotId, instantiate(gltf));
      setStatus((prev) => ({ ...prev, [slotId]: { state: 'idle' } }));
      if (!framedRef.current) {
        framedRef.current = true;
        manager.frameCharacter();
      }
    } catch (error) {
      if (!isCurrent()) return;
      manager.setSlotObject(slotId, null);
      setStatus((prev) => ({
        ...prev,
        [slotId]: { state: 'error', message: describeError(error) },
      }));
    }
  }, []);

  const selectPart = useCallback(
    (slotId: string, partId: string | null) => {
      if (selectionRef.current[slotId] === partId) return;
      selectionRef.current = { ...selectionRef.current, [slotId]: partId };
      setSelection((prev) => ({ ...prev, [slotId]: partId }));
      void saveSelection(slotId, partId);
      void mountPart(slotId, partId);
    },
    [mountPart],
  );

  /** Troca só a base; preservar cabelo, olhos e nariz demonstra o encaixe modular. */
  const stepBase = useCallback(
    (direction: -1 | 1) => {
      const bases = parts.filter((part) => part.slotId === BASE_SLOT);
      if (bases.length === 0) return;
      const current = bases.findIndex((part) => part.id === selectionRef.current[BASE_SLOT]);
      const next = current < 0 ? 0 : (current + direction + bases.length) % bases.length;
      selectPart(BASE_SLOT, bases[next].id);
    },
    [parts, selectPart],
  );

  useEffect(() => {
    function onKeyDown(event: KeyboardEvent) {
      if (event.key !== 'ArrowLeft' && event.key !== 'ArrowRight') return;
      if (event.ctrlKey || event.altKey || event.metaKey) return;
      const target = event.target as HTMLElement | null;
      // Nos campos de formulário as setas têm significado próprio.
      if (target && /^(INPUT|SELECT|TEXTAREA)$/.test(target.tagName)) return;
      if (report) return;
      event.preventDefault();
      stepBase(event.key === 'ArrowLeft' ? -1 : 1);
    }
    window.addEventListener('keydown', onKeyDown);
    return () => window.removeEventListener('keydown', onKeyDown);
  }, [report, stepBase]);

  /* ---------------------------------------------------------- carregamento */

  useEffect(() => {
    if (!ready) return;
    let cancelled = false;
    (async () => {
      try {
        const [storedParts, storedSelection] = await Promise.all([listParts(), loadSelection()]);
        if (cancelled) return;
        setParts(storedParts);
        // Uma peça pode ter sido apagada fora desta sessão.
        const known = new Set(storedParts.map((part) => part.id));
        const valid: Record<string, string | null> = {};
        for (const slot of SLOTS) {
          const partId = currentBundledId(storedSelection[slot.id]);
          valid[slot.id] = partId && known.has(partId)
            ? partId
            : bundledParts.find((part) => part.slotId === slot.id)?.id ?? null;
        }
        selectionRef.current = valid;
        setSelection(valid);
        await Promise.all(SLOTS.map((slot) => mountPart(slot.id, valid[slot.id])));
        if (!cancelled) managerRef.current?.frameCharacter();
        refreshStorage();
      } catch (error) {
        if (!cancelled) setNotice(`Não foi possível abrir a biblioteca: ${describeError(error)}`);
      }
    })();
    return () => {
      cancelled = true;
    };
  }, [ready, mountPart, refreshStorage]);

  /* --------------------------------------------------------------- import */

  const importFiles = useCallback(
    async (files: File[], slotId: string) => {
      setBusy(true);
      setNotice(null);
      const failures: string[] = [];
      const added: PartMeta[] = [];
      for (const file of files) {
        try {
          const data = await file.arrayBuffer();
          assertGlb(data, 'O arquivo escolhido');
          // Parse de verificação: um arquivo corrompido não entra na biblioteca.
          const probeId = newId();
          await loadPartGltf(probeId, data);
          await disposePart(probeId);
          added.push(
            await addPartFromBuffer(data, {
              slotId,
              name: file.name.replace(/\.glb$/i, ''),
              fileName: file.name,
            }),
          );
        } catch (error) {
          failures.push(`${file.name}: ${describeError(error)}`);
        }
      }
      const nextParts = await listParts();
      setParts(nextParts);
      refreshStorage();
      setBusy(false);
      setNotice(failures.length > 0 ? `Não importado — ${failures.join(' | ')}` : null);
      // Primeiro arquivo do slot entra montado, para ver o resultado na hora.
      if (added.length > 0 && !selectionRef.current[slotId]) {
        selectPart(slotId, added[0].id);
      }
    },
    [refreshStorage, selectPart],
  );

  const removePart = useCallback(
    async (part: PartMeta) => {
      setBusy(true);
      try {
        const remaining = parts.filter(
          (item) => item.slotId === part.slotId && item.id !== part.id,
        );
        if (selectionRef.current[part.slotId] === part.id) {
          selectPart(part.slotId, remaining[0]?.id ?? null);
        }
        await deletePart(part.id);
        await clearSelectionUsingPart(part.id);
        // Nenhum clone dela continua na cena, então os recursos podem ir embora.
        await disposePart(part.id);
        animationsRef.current.delete(part.id);
        setParts(await listParts());
        refreshStorage();
      } catch (error) {
        setNotice(`Falha ao excluir: ${describeError(error)}`);
      } finally {
        setBusy(false);
      }
    },
    [parts, refreshStorage, selectPart],
  );

  /* ------------------------------------------------------------ exportação */

  const openExport = useCallback(() => {
    const manager = managerRef.current;
    if (!manager) return;
    setExportError(null);
    const usedParts = Object.values(selectionRef.current)
      .filter((partId): partId is string => Boolean(partId))
      .map((partId) => ({
        partName: partsById.get(partId)?.name ?? partId,
        clips: animationsRef.current.get(partId) ?? 0,
      }));
    setReport(inspectForExport(manager.character, usedParts));
  }, [partsById]);

  const confirmExport = useCallback(async () => {
    const manager = managerRef.current;
    if (!manager) return;
    setExportBusy(true);
    setExportError(null);
    try {
      const buffer = await exportGroupToGlb(manager.character);
      const stamp = new Date().toISOString().replace(/[:.]/g, '-').slice(0, 19);
      downloadGlb(buffer, `personagem-${stamp}.glb`);
      setReport(null);
      setNotice(
        `GLB gerado com ${(buffer.byteLength / 1024).toFixed(1)} KB, container binário conferido.`,
      );
    } catch (error) {
      setExportError(describeError(error));
    } finally {
      setExportBusy(false);
    }
  }, []);

  /* ----------------------------------------------------------------- render */

  const libraryEmpty = parts.length === 0;
  const anythingMounted = Object.values(selection).some(Boolean);
  const mounting = Object.values(status).some((slot) => slot.state !== 'idle');

  return (
    <div className="app">
      <header className="app-header">
        <div className="brand">
          <strong>3DC Lab · v1</strong>
          <span>5 bases · 12 cortes · Olho 1 · Nariz 1</span>
        </div>
        <div className="header-actions">
          <button type="button" onClick={() => managerRef.current?.frameCharacter()}>
            Restaurar enquadramento
          </button>
          <button
            type="button"
            className="ghost"
            onClick={() => {
              const next = !gridVisible;
              setGridVisible(next);
              managerRef.current?.setGridVisible(next);
            }}
          >
            {gridVisible ? 'Ocultar grade' : 'Mostrar grade'}
          </button>
          <button type="button" className="primary" disabled={!anythingMounted || mounting || busy} onClick={openExport}>
            Exportar montagem GLB
          </button>
        </div>
      </header>

      <main className="stage">
        <Viewer
          onReady={(manager) => {
            managerRef.current = manager;
            manager.setGridVisible(gridVisible);
            manager.setHairPreviewVisible(hairPreviewVisible);
            setReady(true);
          }}
          onDispose={() => {
            managerRef.current = null;
            framedRef.current = false;
            setReady(false);
          }}
        />
        <div className="view-actions" aria-label="Vistas do personagem">
          {([['front', 'Frente'], ['side', 'Perfil'], ['threeQuarter', 'Três quartos'], ['back', 'Costas']] as const).map(([view, label]) => (
            <button key={view} type="button" onClick={() => managerRef.current?.setView(view)}>{label}</button>
          ))}
          <button type="button" aria-pressed={!hairPreviewVisible} title="Oculta o cabelo só na visualização; a exportação mantém a montagem." onClick={() => {
            const visible = !hairPreviewVisible;
            setHairPreviewVisible(visible);
            managerRef.current?.setHairPreviewVisible(visible);
          }}>{hairPreviewVisible ? 'Ocultar cabelo' : 'Mostrar cabelo'}</button>
        </div>
        {libraryEmpty ? (
          <div className="stage-empty">
            <strong>Nenhum arquivo importado ainda.</strong>
            <p>
              O conjunto RCL aparece automaticamente. Você também pode importar outras peças nos slots ao lado.
            </p>
          </div>
        ) : (
          <p className="viewer-hint">
            ◀ ▶ ou setas do teclado trocam a base · arraste para girar · roda do mouse aproxima
          </p>
        )}
      </main>

      <aside className="panel">
        {notice && (
          <div className="notice">
            <span>{notice}</span>
            <button type="button" onClick={() => setNotice(null)} aria-label="Fechar aviso">
              ×
            </button>
          </div>
        )}

        <div className="panel-scroll">
          <p className="catalog-note">Troque o rosto ou o cabelo: os outros módulos permanecem montados. Sobrancelhas, boca e orelhas acompanham cada base.</p>
          {SLOTS.map((slot) => (
            <SlotPanel
              key={slot.id}
              slot={slot}
              parts={partsBySlot[slot.id] ?? []}
              selectedId={selection[slot.id] ?? null}
              status={status[slot.id] ?? { state: 'idle' }}
              busy={busy}
              showCycler={slot.id === BASE_SLOT}
              onImport={(files) => void importFiles(files, slot.id)}
              onSelect={(partId) => selectPart(slot.id, partId)}
              onDelete={(part) => void removePart(part)}
              onStep={stepBase}
            />
          ))}

          <section className="panel-block storage">
            <h2>Armazenamento</h2>
            <p className="hint">{STORAGE_NOTE}</p>
            {storage && (
              <p className="hint">
                Em uso: {storage.usageBytes !== null ? formatBytes(storage.usageBytes) : '—'}
                {storage.quotaBytes !== null && ` de ${formatBytes(storage.quotaBytes)}`}
                {storage.persistent !== null &&
                  ` · persistência ${storage.persistent ? 'concedida' : 'não concedida'}`}
              </p>
            )}
            {storage?.persistent === false && (
              <button
                type="button"
                className="ghost"
                onClick={() => {
                  void requestPersistentStorage().then(refreshStorage);
                }}
              >
                Pedir armazenamento persistente
              </button>
            )}
          </section>
        </div>
      </aside>

      {report && (
        <ExportDialog
          report={report}
          busy={exportBusy}
          error={exportError}
          onCancel={() => setReport(null)}
          onConfirm={() => void confirmExport()}
        />
      )}
    </div>
  );
}
