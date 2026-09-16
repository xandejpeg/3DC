import { EXPORT_LIMITS, THREE_VERSION } from '../limits';
import type { ExportReport } from '../lib/inspect';

interface ExportDialogProps {
  report: ExportReport;
  busy: boolean;
  error: string | null;
  onCancel: () => void;
  onConfirm: () => void;
}

export function ExportDialog({ report, busy, error, onCancel, onConfirm }: ExportDialogProps) {
  const blocked = report.blockers.length > 0;

  return (
    <div className="modal-backdrop" role="dialog" aria-modal="true" aria-label="Exportar GLB">
      <div className="modal">
        <h2>Exportar GLB</h2>
        <p className="hint">
          Conferência feita no grupo do personagem antes de gerar o arquivo. three.js {THREE_VERSION},
          GLTFExporter em modo binário.
        </p>

        {blocked && (
          <section className="report blockers">
            <h3>Bloqueios</h3>
            <ul>
              {report.blockers.map((item) => (
                <li key={item}>{item}</li>
              ))}
            </ul>
          </section>
        )}

        {report.warnings.length > 0 && (
          <section className="report warnings">
            <h3>Sai diferente do original</h3>
            <ul>
              {report.warnings.map((item) => (
                <li key={item}>{item}</li>
              ))}
            </ul>
          </section>
        )}

        <section className="report preserved">
          <h3>O que vai no arquivo</h3>
          <ul>
            {report.preserved.map((item) => (
              <li key={item}>{item}</li>
            ))}
          </ul>
          <p className="hint">
            Ficam de fora: grade, piso, luzes, câmera, gizmos e qualquer peça oculta ou não
            selecionada.
          </p>
        </section>

        <details className="report">
          <summary>Limitações conhecidas desta versão</summary>
          <ul>
            {EXPORT_LIMITS.map((limit) => (
              <li key={limit.title}>
                <strong>{limit.title}.</strong> {limit.detail}
              </li>
            ))}
          </ul>
        </details>

        {error && <p className="error-text">{error}</p>}

        <footer className="modal-actions">
          <button type="button" className="ghost" onClick={onCancel} disabled={busy}>
            Cancelar
          </button>
          <button type="button" onClick={onConfirm} disabled={blocked || busy}>
            {busy ? 'Exportando…' : 'Exportar .glb'}
          </button>
        </footer>
      </div>
    </div>
  );
}
