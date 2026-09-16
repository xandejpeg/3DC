import { useEffect, useRef } from 'react';
import { SceneManager } from '../three/SceneManager';

interface ViewerProps {
  onReady: (manager: SceneManager) => void;
  onDispose: () => void;
}

export function Viewer({ onReady, onDispose }: ViewerProps) {
  const containerRef = useRef<HTMLDivElement>(null);
  const readyRef = useRef(onReady);
  const disposeRef = useRef(onDispose);
  readyRef.current = onReady;
  disposeRef.current = onDispose;

  useEffect(() => {
    const container = containerRef.current;
    if (!container) return;
    const manager = new SceneManager(container);
    manager.frameCharacter();
    readyRef.current(manager);
    return () => {
      disposeRef.current();
      manager.dispose();
    };
  }, []);

  return <div className="viewer" ref={containerRef} />;
}
