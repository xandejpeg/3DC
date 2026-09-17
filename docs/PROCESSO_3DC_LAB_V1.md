# Processo do 3DC Lab v1

O 3DC Lab v1 produz dois resultados: combinações de personagens em GLB para o Real Car Lifestyle e um histórico verificável de como essas combinações foram construídas. A geometria é criada no Blender; o aplicativo React/Three.js monta os módulos e exporta a seleção. Não há geração de malha a partir de imagem dentro do aplicativo nesta versão.

## Versões e fontes de verdade

| Identificação | Significado |
| --- | --- |
| 3DC Lab v1 | Fase atual do produto/laboratório |
| `package.json: 0.1.0` | Versão técnica do protótipo web |
| `piloto-feminino-01` / `revisao-rosto-02` | Experimentos preservados de base 1 e cabelo |
| `conjunto-feminino-v1` | Primeira revisão com cinco bases e um cabelo |
| `conjunto-feminino-v2` / `rcl-female-v2` | Revisão dos assets com componentes faciais; catálogo ativo |
| `cabelos-femininos-v1` | Primeira entrega dos cortes 2–12, compatível com as bases faciais existentes |
| Contrato 0.5 | Revisão do documento de interfaces |

O usuário define conceito, aparência pretendida e escopo. A implementação interpreta as imagens e registra as escolhas. Legendas de referências, dimensões propostas e relatórios anteriores são contexto revisável. A escala inicial de 24 cm não se tornou uma obrigação estética.

## 1. Referências e contrato

A análise recebida cobriu 100 imagens de peças, montagens e personagens completos. Foi reutilizada; a modelagem voltou às imagens relevantes a cada etapa, sem repetir todo o inventário. As imagens mostram intenção visual, não topologia, medidas calibradas ou prova de encaixe tridimensional.

- [Análise completa](referencias-rcl/Analise_completa_referencias_RCL.md) e [contrato vigente](referencias-rcl/Contrato_pecas_interfaces_RCL.md).
- [Originais arquivados](referencias-rcl/originais/README.md) e [catálogo portátil](referencias-rcl/Catalogo_portatil.json). Cada caminho é relativo à pasta do catálogo.
- O inventário recebido conserva os caminhos absolutos históricos. Para outro computador, usar o catálogo portátil. `scripts/arquivar-referencias-rcl.py` copia e verifica os hashes, sem modificar os originais ou alegar nova análise visual.

Referências principais: R049 (vistas/decomposição feminina), R052 (cabelo isolado), R076–R080 (bases), R088–R092 (montagens), R033 (Olho 1) e R019 (Nariz 1). A ficha isolada e a montagem têm funções complementares. A menção a rosto feminino 6 em outra prancha permaneceu uma inconsistência; não geramos essa sexta base.

## 2. Piloto e revisão da base

O primeiro piloto criou base feminina 1 com pescoço e Corte 1 como objetos separados na mesma cena, em metros. Scripts do [piloto](../artifacts/piloto-feminino-01/scripts/) registram base, cabelo, refinamento, folga interna, exportação e comparação.

A [revisão do rosto](../artifacts/piloto-feminino-01/revisao-rosto-02/) alterou bochechas, mandíbula, queixo e transição para o pescoço, preservando cabelo e encaixe craniano. O antes/depois usa as mesmas câmeras. A altura deixou de ser normalizada aos 24 cm: a forma guiada pela referência prevaleceu sobre a convenção inicial.

Esses scripts históricos preservam caminhos locais da execução e exigem adaptação de `OUT`/`PARENT` em outra máquina. As cenas salvas são os checkpoints utilizáveis; não é necessário executar todos os experimentos para abrir o resultado atual.

## 3. Cinco rostos com um cabelo

`scripts/rcl-bases.py` parte da cena R02. Campos de deformação alteram o terço inferior, mantendo o couro cabeludo protegido e limitando deslocamentos perto do cabelo. As variantes são suave, angular, arredondada, alongada e maçãs largas. Os parâmetros estão em [parametros.json](../artifacts/conjunto-feminino-v1/parametros.json).

O cabelo é um objeto compartilhado. Não foi remodelado ou reposicionado por rosto. Prévias pequenas permitiram comparar os cinco formatos antes de `scripts/rcl-exportar.py` gerar os módulos e as cinco montagens. O GLB de montagem usa os próprios objetos dos módulos, sem criar outra cabeça independente.

## 4. Olho 1, Nariz 1 e partes fixas

Na retomada após Ctrl+C, estavam salvos os cinco rostos e o cabelo; não havia novos componentes faciais concluídos. `scripts/rcl-faciais.py` carrega esse conjunto e acrescenta apenas a revisão necessária ao rosto montado.

| Peça | Implementação escolhida e motivo |
| --- | --- |
| Base | Remover as faces substituídas pelos módulos de olho/nariz; padronizar as bordas e uma faixa de transição, mantendo a forma facial fora dessas regiões |
| Olho 1 | Um GLB para o par, com abertura semicerrada, íris castanha, pupila, pálpebras e pele ao redor; não apenas esferas com cor |
| Superfície ocular | Segmento esférico estático fechado atrás; partes ocultas da esfera foram omitidas para evitar atravessar a pálpebra; não está preparado para piscar ou girar |
| Nariz 1 | Superfície separada que ocupa a abertura nasal e compartilha a borda com a base; profundidade interpretada com apoio da vista geral/perfil |
| Sobrancelhas, boca, orelhas | Objetos separados na cena, mas pertencentes ao GLB de cada base; desenho fixo com ajuste à superfície receptora |
| Cabelo | Mesmo arquivo binário da revisão anterior, com SHA-256 igual |

A primeira pálpebra apresentou triângulos cruzados e vazamentos do globo. Foi refeita com triangulação restrita entre borda externa e abertura interna. A íris inicialmente era um disco pouco subdividido e ficava parcialmente atrás da esclera; recebeu anéis radiais para acompanhar a curvatura. `scripts/rcl-revisar-iris.py` registra essa correção localizada; ela também foi incorporada ao construtor facial.

Relações de parâmetros: centro/raio ocular, abertura, pálpebras e íris precisam continuar coerentes; base e módulo precisam compartilhar a borda de pele. A boca acompanha a superfície e 30% do deslocamento anterior do queixo, preservando o desenho. Valores executados: [escolhas.json](../artifacts/conjunto-feminino-v2/escolhas.json); bordas: [interfaces.json](../artifacts/conjunto-feminino-v2/interfaces.json). São escolhas do protótipo, não medidas anatômicas extraídas das imagens.

## 5. Exportação e integração no laboratório

`scripts/rcl-exportar-faciais.py` exporta cinco bases com partes fixas, um par ocular e um nariz; reutiliza o GLB do cabelo. Exporta ainda cinco montagens. Cada peça conserva o referencial da cena mestre. O exportador inclui somente os objetos selecionados da cena ativa, evitando incorporar objetos das cenas históricas de comparação.

O catálogo em `public/models/rcl-feminino-v2/manifest.json` alimenta `src/lib/catalog.ts`. O banco local conserva importações e seleções do usuário. IDs da revisão anterior são mapeados à mesma variante atual. `SceneManager.setSlotObject` substitui apenas o slot escolhido: trocar a base deixa cabelo, olhos e nariz com as mesmas instâncias e transformações.

Contadores por slot descartam carregamentos assíncronos atrasados. A câmera oferece frente, perfil, três quartos e costas. Ocultar o cabelo usa a camada da câmera, sem removê-lo da exportação. O exportador leva somente o grupo do personagem para uma cena temporária; câmeras, grade e luzes do laboratório ficam fora.

## 6. Verificação e seus limites

Prévias leves orientaram as correções; exportação/reimportação completa ficou concentrada nas entregas coerentes e foi repetida após a correção da íris, porque o asset mudou.

- Dez verificações no Blender: cinco conjuntos de módulos separados e cinco montagens. Geometria e materiais preservados, bordas de contato coincidentes e nenhum cruzamento base/cabelo detectado. [Resultados](../artifacts/conjunto-feminino-v2/validacao.json).
- `npm run test:rcl`: usa as classes reais do app, sem navegador/WebGL, e confere cinco trocas, preservação dos três módulos compartilhados e reimportação das exportações. [Resultados](../artifacts/conjunto-feminino-v2/exportacoes-app/resultado.json).
- `npm run build`: verifica TypeScript e empacotamento; permanece o aviso de bundle JavaScript grande.
- Khronos Validator: 18 GLBs sem erros/avisos. [Relatório final](../artifacts/conjunto-feminino-v2/khronos-final.txt).

Isso não certifica continuidade perfeita de sombreamento, soldagem de vértices, ausência de toda interseção facial, rigging ou desempenho no jogo. Orelhas/lábios têm contato interno por sobreposição. Ainda há sombra pesada nas pálpebras, nariz anguloso, boca fina e franja excessivamente fechada. A interface atual não teve nova auditoria por cliques; a engine do jogo não foi validada.

## 7. Reabrir e reproduzir

Para estudar ou usar a versão entregue, abrir [conjunto-feminino-v2.blend](../artifacts/conjunto-feminino-v2/conjunto-feminino-v2.blend) e rodar o aplicativo com `npm ci` e `npm run dev`. Não é preciso gerar os modelos novamente.

Para refazer a etapa facial a partir da revisão anterior, usar Blender 5.2.1 LTS (versão usada nesta execução), numa branch de trabalho. Os comandos abaixo sobrescrevem os resultados da revisão 2 dentro dessa cópia de trabalho:

```powershell
$blenderExe = 'C:\Program Files\Blender Foundation\Blender 5.2\blender.exe'
& $blenderExe --factory-startup -b artifacts/conjunto-feminino-v1/conjunto-feminino-v1.blend -t 2 --python-exit-code 1 --python scripts/rcl-faciais.py
& $blenderExe --factory-startup -b artifacts/conjunto-feminino-v2/conjunto-feminino-v2.blend -t 2 --python-exit-code 1 --python scripts/rcl-exportar-faciais.py
python scripts/rcl-comparacao-faciais.py
npm run build
npm run test:rcl
```

O comparador usa Python com Pillow e a fonte Segoe UI do Windows. Os scripts recentes resolvem a raiz a partir do próprio arquivo. Reproduzir o procedimento não promete arquivos binários idênticos entre versões de Blender/exportador: comparar geometria, materiais e aparência.

## 8. Como registrar as próximas etapas

Cada mudança deve deixar uma ligação entre referência, decisão, código/asset, comparação e teste. Usar o [modelo de registro](modelos/registro-etapa.md) para mudanças que alterem o visual ou o contrato de peças. Ajustes pequenos podem ser descritos no corpo do commit, sem criar um relatório a cada parâmetro.

Mensagens de commit devem explicar o problema e o resultado, os módulos afetados, a validação e os limites. Comentários de código explicam invariantes e escolhas (por exemplo, por que a borda deve coincidir), em vez de repetir a instrução que vem logo abaixo. Não inventar testes nem reconstruir uma sequência fictícia de commits históricos.

Versionar cenas e módulos de entrega, referências necessárias, scripts, parâmetros, comparações e resultados de validação. Excluir dependências instaladas, build reproduzível, cache, logs temporários e backups automáticos `.blend1`. Revisões anteriores identificadas por nome continuam disponíveis. O objetivo é permitir que o projeto do jogo rastreie cada GLB até o commit e a cena que o produziram.

## 9. Expansão dos cabelos femininos 2–12

`scripts/rcl-cabelos.py -- --cut N` reutiliza a cena facial entregue como biblioteca, cria apenas o cabelo N e salva antes de renderizar. As mechas, cachos, elásticos e desenhos possuem grupos nomeados para edição no Blender. O mesmo objeto gera a prévia e o GLB; não há cabelo remodelado por rosto. Cada corte tem checkpoint próprio, permitindo retomar uma falha sem executar os demais.

Foram consultados os originais arquivados R053–R063 e as oito combinações R001–R008, cópias verificadas do inventário. Caimento, franja, risca, ritmo dos cachos e volume lateral foram relacionados. Um envelope comum das cinco bases e peças faciais corrige o interior das mechas mais curvas; a origem, as bases, olhos, nariz e partes fixas permanecem preservados. As cores dos raspados acompanham o material de pele existente.

As exportações/reimportações foram concentradas após as prévias, com novas verificações nos cortes que falharam. `rcl-cabelos-catalogo.py` aceita somente entregas sem interseções detectadas. `npm run test:rcl-hair` testa as 60 combinações e a permanência dos outros slots em 120 operações de troca. A expansão do catálogo não alterou o exportador do aplicativo. [Decisões, problemas, evidências e comandos](registros/2026-09-17-cabelos-femininos.md).
