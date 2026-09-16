/**
 * Limitações verificadas na versão fixada (three 0.186.0), lidas diretamente
 * de node_modules/three/examples/jsm/exporters/GLTFExporter.js e
 * .../loaders/GLTFLoader.js. São exibidas na interface antes de exportar.
 */

export const THREE_VERSION = '0.186.0';

export interface LimitNote {
  title: string;
  detail: string;
}

export const EXPORT_LIMITS: LimitNote[] = [
  {
    title: 'Animação não faz parte desta V1',
    detail:
      'O GLTFExporter só grava clipes passados em options.animations. Esta versão não passa nenhum clipe, ' +
      'então animações presentes nos GLB importados não entram no arquivo exportado. A geometria, o esqueleto ' +
      'e os morph targets continuam sendo exportados; apenas as faixas de animação são omitidas.',
  },
  {
    title: 'Materiais fora de Standard/Physical/Basic são aproximados',
    detail:
      'GLTFExporter.js emite "Use MeshStandardMaterial or MeshBasicMaterial for best results" para qualquer outro ' +
      'material e grava apenas as propriedades compatíveis com glTF. MeshShaderMaterial é explicitamente ignorado ' +
      '("THREE.ShaderMaterial not supported"). O app avisa antes; nenhum material é trocado silenciosamente.',
  },
  {
    title: 'Texturas são reencodadas via canvas',
    detail:
      'processImage() desenha a imagem em um canvas e grava PNG/JPEG/WebP dentro do .glb. Imagens comprimidas ' +
      '(KTX2/Basis, DDS) lançam "Invalid image type" a menos que se injete textureUtils — não suportado nesta V1. ' +
      'DataTexture só é aceita em RGBAFormat. Não é usado maxTextureSize, então não há redução silenciosa de resolução.',
  },
  {
    title: 'Skin exige que os ossos estejam dentro do que é exportado',
    detail:
      'processSkin() resolve joints por nodeMap.get(bone). Se algum osso do esqueleto não estiver na hierarquia ' +
      'exportada, o índice fica indefinido e o glTF sai inválido. O app bloqueia a exportação nesse caso.',
  },
  {
    title: 'Morph targets: só POSITION e NORMAL',
    detail:
      'O exportador avisa "Only POSITION and NORMAL morph are supported"; morphs de outros atributos são descartados.',
  },
  {
    title: 'Objetos invisíveis não entram',
    detail: 'A exportação usa onlyVisible: true, então peças ocultas ficam de fora — assim como piso, luzes, câmera e grade, que nunca fazem parte do grupo do personagem.',
  },
  {
    title: 'O encaixe entre peças é responsabilidade dos arquivos',
    detail:
      'O app não centraliza, não normaliza escala e não une malhas, e não oferece ajuste de posição ou escala. ' +
      'Base e cabelo só se alinham se os GLB saírem do Blender com a mesma origem, a mesma escala e a mesma orientação.',
  },
  {
    title: 'Compatibilidade com Unity não foi testada',
    detail:
      'O arquivo gerado é glTF 2.0 binário e foi conferido com o Khronos glTF Validator e por reabertura em cena ' +
      'limpa. Importação em Unity não foi verificada e portanto não é afirmada.',
  },
];

export const STORAGE_NOTE =
  'A biblioteca fica no IndexedDB deste navegador, neste computador. Limpar dados do site, usar janela anônima, ' +
  'trocar de navegador ou uma limpeza automática de espaço apagam tudo. Não há servidor nem cópia remota.';
