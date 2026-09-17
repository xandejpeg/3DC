import {
  ACESFilmicToneMapping,
  Box3,
  Color,
  DirectionalLight,
  Group,
  GridHelper,
  HemisphereLight,
  MathUtils,
  Object3D,
  PerspectiveCamera,
  PMREMGenerator,
  Scene,
  SRGBColorSpace,
  Sphere,
  Vector3,
  WebGLRenderer,
} from 'three';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls.js';
import { RoomEnvironment } from 'three/examples/jsm/environments/RoomEnvironment.js';

const DEFAULT_TARGET = new Vector3(0, 0.55, 0);
const DEFAULT_RADIUS = 0.9;

/**
 * Dono do renderizador, da câmera e do grupo do personagem.
 * Somente o grupo "Personagem" recebe peças; luzes, grade e câmera vivem fora
 * dele e por isso nunca chegam à exportação.
 */
export class SceneManager {
  readonly scene = new Scene();
  readonly character = new Group();

  private readonly renderer: WebGLRenderer;
  private readonly camera: PerspectiveCamera;
  private readonly controls: OrbitControls;
  private readonly grid: GridHelper;
  private readonly slots = new Map<string, Group>();
  private readonly observer: ResizeObserver;
  private disposed = false;

  constructor(private readonly container: HTMLElement) {
    this.renderer = new WebGLRenderer({ antialias: true, alpha: false });
    this.renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    this.renderer.outputColorSpace = SRGBColorSpace;
    this.renderer.toneMapping = ACESFilmicToneMapping;
    this.renderer.toneMappingExposure = 1;
    container.appendChild(this.renderer.domElement);

    this.scene.background = new Color(0x15171c);

    const pmrem = new PMREMGenerator(this.renderer);
    this.scene.environment = pmrem.fromScene(new RoomEnvironment(), 0.04).texture;
    pmrem.dispose();

    this.character.name = 'Personagem';
    this.scene.add(this.character);

    const hemisphere = new HemisphereLight(0xffffff, 0x2b2f38, 1.2);
    hemisphere.name = 'ViewerHemisphereLight';
    const key = new DirectionalLight(0xffffff, 2.0);
    key.position.set(1.5, 2.5, 2);
    key.name = 'ViewerKeyLight';
    const fill = new DirectionalLight(0xffffff, 0.6);
    fill.position.set(-2, 1, -1.5);
    fill.name = 'ViewerFillLight';
    this.scene.add(hemisphere, key, fill);

    this.grid = new GridHelper(4, 16, 0x3a3f4b, 0x262a33);
    this.grid.name = 'ViewerGrid';
    this.scene.add(this.grid);

    this.camera = new PerspectiveCamera(35, 1, 0.01, 200);
    this.camera.name = 'ViewerCamera';
    this.camera.position.set(0, 0.7, 2.4);

    this.controls = new OrbitControls(this.camera, this.renderer.domElement);
    this.controls.enableDamping = true;
    this.controls.dampingFactor = 0.08;
    this.controls.minDistance = 0.05;
    this.controls.maxDistance = 50;
    this.controls.target.copy(DEFAULT_TARGET);

    this.observer = new ResizeObserver(() => this.resize());
    this.observer.observe(container);
    this.resize();

    this.renderer.setAnimationLoop(() => {
      this.controls.update();
      this.renderer.render(this.scene, this.camera);
    });
  }

  get domElement(): HTMLCanvasElement {
    return this.renderer.domElement;
  }

  setGridVisible(visible: boolean): void {
    this.grid.visible = visible;
  }

  /** Só a câmera oculta o cabelo; o módulo continua montado e exportável. */
  setHairPreviewVisible(visible: boolean): void {
    if (visible) this.camera.layers.enable(1);
    else this.camera.layers.disable(1);
  }

  setView(view: 'front' | 'side' | 'threeQuarter' | 'back'): void {
    const distance = this.camera.position.distanceTo(this.controls.target);
    const directions = {
      front: new Vector3(0, 0, 1),
      side: new Vector3(1, 0, 0),
      threeQuarter: new Vector3(.55, .13, 1).normalize(),
      back: new Vector3(0, 0, -1),
    };
    this.camera.position.copy(this.controls.target).addScaledVector(directions[view], distance);
    this.controls.update();
  }

  /** Substitui o conteúdo de um slot sem tocar nos demais. */
  setSlotObject(slotId: string, object: Object3D | null): void {
    let slot = this.slots.get(slotId);
    if (!object) {
      if (slot) {
        // clear() apenas desanexa: geometrias, materiais e texturas continuam
        // vivos no cache porque podem estar em uso por outro slot.
        slot.clear();
        this.character.remove(slot);
        this.slots.delete(slotId);
      }
      return;
    }
    if (!slot) {
      slot = new Group();
      slot.name = `Slot_${slotId}`;
      this.character.add(slot);
      this.slots.set(slotId, slot);
    }
    slot.clear();
    if (slotId === 'hair') object.traverse((node) => node.layers.set(1));
    slot.add(object);
  }

  removeAllSlots(): void {
    for (const slotId of [...this.slots.keys()]) this.setSlotObject(slotId, null);
  }

  /** Reenquadra a câmera no que estiver montado. */
  frameCharacter(): void {
    const box = new Box3().setFromObject(this.character);
    let center = DEFAULT_TARGET.clone();
    let radius = DEFAULT_RADIUS;
    if (!box.isEmpty()) {
      const sphere = box.getBoundingSphere(new Sphere());
      if (sphere.radius > 1e-6) {
        center = sphere.center.clone();
        radius = sphere.radius;
      }
    }
    const fov = MathUtils.degToRad(this.camera.fov);
    const distance = (radius / Math.sin(fov / 2)) * 1.25;
    const direction = new Vector3(0.35, 0.18, 1).normalize();
    this.camera.position.copy(center).addScaledVector(direction, distance);
    this.camera.near = Math.max(distance / 1000, 0.001);
    this.camera.far = distance * 100;
    this.camera.updateProjectionMatrix();
    this.controls.target.copy(center);
    this.controls.update();
  }

  private resize(): void {
    if (this.disposed) return;
    const width = this.container.clientWidth || 1;
    const height = this.container.clientHeight || 1;
    this.renderer.setSize(width, height, false);
    this.camera.aspect = width / height;
    this.camera.updateProjectionMatrix();
  }

  dispose(): void {
    this.disposed = true;
    this.observer.disconnect();
    this.renderer.setAnimationLoop(null);
    this.controls.dispose();
    this.removeAllSlots();
    this.scene.environment?.dispose();
    this.grid.geometry.dispose();
    this.renderer.dispose();
    this.renderer.domElement.remove();
  }
}
