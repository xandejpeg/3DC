import { createRoot } from 'react-dom/client';
import App from './App';
import './styles.css';

const container = document.getElementById('root');
if (!container) throw new Error('Elemento #root não encontrado.');

// Sem StrictMode: o modo estrito monta e desmonta os efeitos duas vezes, o que
// criaria e destruiria o contexto WebGL a cada render de desenvolvimento.
createRoot(container).render(<App />);
