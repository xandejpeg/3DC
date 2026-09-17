# Contrato de peças e interfaces — 3DC / RCL

Data: 17/09/2026. Versão: 0.5 — Olho 1, Nariz 1 e partes faciais fixas nas cinco bases.

## Retomada vigente — componentes faciais

O pedido após Ctrl+C autoriza Olho 1, Nariz 1 e partes faciais fixas, mantendo o encaixe ao alternar os rostos. A v1 estava concluída; não havia novos componentes faciais salvos. Ela foi reaproveitada e permanece preservada. As restrições históricas abaixo sobre fabricar somente base/cabelo foram substituídas por este pedido.

- Olho 1: um GLB com o par, íris castanha, abertura semicerrada, pálpebras e pele de transição, conforme [R033] e [R049]. A superfície esférica visível é fechada atrás como segmento estático; não é um olho preparado para rotação ou piscar.
- Nariz 1: GLB separado, guiado pelo isolado [R019] e pela montagem/perfil de [R049]. A profundidade foi interpretada; não é uma medida extraída da prancha frontal.
- Partes fixas: sobrancelhas, boca e orelhas em objetos separados na cena, exportados dentro do GLB de cada base. A divisão é uma escolha técnica para este conjunto estático. [R049] mantém sobrancelhas/boca na base e ilustra orelhas separadas; não exige que cada objeto seja outro slot.
- Bordas orbital/nasal: remover as faces da base que o módulo substitui; as bordas de contato compartilham posições e normais. Somente essa região e sua transição foram adaptadas. O cabelo não foi remodelado e seu GLB é idêntico ao da v1.
- Parâmetros relacionados: centro e raio ocular, abertura, pálpebras, íris/pupila e curva da pele mudam juntos; borda nasal e base também. A boca segue a superfície de cada rosto e 30% da variação vertical anterior do queixo, preservando seu desenho. Escala permanece em metros, sem impor 24 cm às proporções.

Entrega e verificações: [v2](../../artifacts/conjunto-feminino-v2/ENTREGA.md). Compatibilidade verificada apenas para estas cinco bases + Corte 1 + Olho 1 + Nariz 1; não implica outros padrões oculares ou nasais.

## Histórico — conjunto integrado v1

O usuário autorizou avançar para a troca de bases distintas com o mesmo cabelo, resolvendo autonomamente modelagem e integração. A entrega contém as cinco bases femininas e o Corte Feminino 1 em GLBs separados; o cabelo e a superfície craniana de contato são comuns. A escala anterior não determina as proporções. [Resultado, comparação e limites da validação](../../artifacts/conjunto-feminino-v1/ENTREGA.md).

As restrições históricas de executar apenas o primeiro par e aguardar para a próxima alteração foram substituídas por essa autorização. Olhos, nariz, outros módulos faciais, corpo e randomização continuam fora deste conjunto.

## Histórico — revisão limitada do rosto

O usuário autorizou corrigir somente bochechas, mandíbula, queixo e transição do pescoço da base feminina 1, guiando a forma pelas referências originais. Cabelo e encaixe craniano ficam preservados. Os 24 cm passam a ser referência provisória, sem obrigar uma proporção estética ou normalização da altura.

A revisão resultou em 0,226 m do queixo ao topo craniano, por correção local e sem escala global. Os parâmetros de largura, encurtamento inferior e transição do pescoço, suas relações, imagens antes/depois e verificações estão no [registro R02](../../artifacts/piloto-feminino-01/revisao-rosto-02/RELATORIO_REVISAO.md). A versão anterior permanece preservada. Esta autorização não inclui a próxima alteração, que será decidida após a comparação.

## Decisões provisórias autorizadas para o piloto feminino 01

Execução limitada à base feminina 1 e ao Corte Feminino 1, como módulos separados na mesma montagem. As outras quatro bases e os componentes faciais permanecem fora desta execução.

- Pescoço incluído na base, conforme [R076], [R049] e [R099].
- Escala em metros. O primeiro piloto usou 0,24 m do queixo ao topo do crânio, sem cabelo ou pescoço; a revisão 0.3 trata essa medida como referência provisória, sem impor a mesma altura após a correção local.
- Regiões orbital e nasal editáveis, com interfaces provisórias. Cavidades orbitais e região nasal identificadas na malha; sem fabricar olhos, nariz, sobrancelhas, boca, orelhas ou outros componentes faciais.
- Fonte única na cena mestre: os dois GLBs individuais e a montagem derivam dos mesmos objetos. Reimportação obrigatória para verificar posição, materiais e encaixe.
- Destino: `artifacts/piloto-feminino-01`. As imagens e o registro de problemas dessa execução acompanharão os arquivos.

Estas decisões substituem as pendências de pescoço e escala registradas na versão 0.1. A geometria definitiva das interfaces faciais continua em estudo; este piloto não valida intercambialidade com olhos ou narizes.

**Execução do primeiro par:** arquivos e imagens disponíveis em [piloto-feminino-01](../../artifacts/piloto-feminino-01/RELATORIO_PILOTO.md). Base com pescoço e cabelo foram modelados como dois objetos. Os dois GLBs separados e a montagem foram reimportados: posições, triângulos e materiais preservados, com zero interseções detectadas entre base e cabelo. O relatório registra correções e limitações visuais; as outras bases não foram produzidas.

Este documento transforma a [análise completa](Analise_completa_referencias_RCL.md) em regras de montagem e decisões rastreáveis. A análise foi lida integralmente; o [inventário JSON](Inventario_completo_referencias_RCL.json) foi usado para localizar os originais. Foram reabertas 30 imagens relevantes para este contrato, indicadas nas referências ao final. A auditoria das 100 imagens pertence ao relatório recebido; esta revisão não declara uma nova inspeção visual integral dos 100 arquivos.

**Escopo vigente:** primeiro experimentar formatos de rosto com um único cabelo fixo, conforme a [visão do projeto](../../VISAO_3DC_REAL_CAR_LIFESTYLE.md). O recorte feminino contém cinco bases e o Corte Feminino 1. Olhos, nariz e outros módulos faciais pertencem à expansão. Este contrato não autoriza o piloto ampliado nem registra compatibilidade já comprovada.

## 1. Regras que orientam a continuidade

1. A montagem usa os próprios módulos separados da cena mestre. Peça isolada, cabeça montada, vista explodida e exportação devem compartilhar a mesma fonte de geometria.
2. O cabelo do primeiro teste conserva geometria, posição, orientação e escala quando a base muda. Ajustar o cabelo para cada rosto invalidaria esse teste.
3. As regiões de contato necessárias serão padronizadas; bochechas, mandíbula e queixo conservam a identidade de cada base. O catálogo não prova que todo o crânio seja idêntico.
4. Referências visuais, propostas técnicas e decisões de escopo terão registros distintos. Legendas não definem topologia, medidas ou autorização para adicionar peças.
5. As interfaces orbital e nasal serão planejadas antes da malha definitiva da base. A ausência dos módulos no primeiro teste não determina uma face lisa, fechada ou sem cavidades.
6. A compatibilidade será registrada por combinação testada. A aprovação de base + cabelo não aprova olhos, narizes, outros cortes ou uso entre linhas masculina e feminina.

As regras 1–3 seguem a intenção de troca presente em [R049], [R050], [R051] e nas cinco montagens [R088], [R089], [R090], [R091], [R092], combinada com o escopo explícito do projeto. As regras 4–6 respondem às limitações documentadas na análise completa.

## 2. Quem contém cada parte

| Parte | Responsabilidade proposta e fronteira | Tratamento nesta etapa | Evidência |
|---|---|---|---|
| Base facial/crânio | Silhueta, testa, bochechas, mandíbula, queixo e couro cabeludo; recebe regiões de contato de cabelo, olhos e nariz | Produzir futuramente as bases do conjunto em teste; conteúdo orbital/nasal exato ainda precisa ser fechado | Bases [R076]–[R080], gerais [R049], [R050] |
| Cabelo | Corte completo separado, incluindo seus volumes e a superfície interna necessária | Um único Corte Feminino 1, compartilhado por todas as bases femininas | Isolado [R052]; montagens [R088]–[R092] |
| Olhos | Proposta: globos, íris/pupilas, pálpebras e pele de transição necessária à variante; cílios quando pertinentes | Planejar a interface; não fabricar no primeiro experimento | Fichas [R033], [R038], [R039]; combinação [R006] |
| Nariz | Proposta: ponte, ponta, asas e transição até uma borda de contato compartilhada com a base | Planejar a interface; não fabricar agora | Isolados [R019], [R023]; montagens [R016] |
| Pescoço | Pertence provisoriamente à base da cabeça, com futura junção inferior ao conjunto superior do corpo | Incluído no piloto feminino 01 por decisão do usuário | [R049], [R050], [R099], [R100] |
| Sobrancelhas, boca e barba | Aparecem nas bases ilustradas; sua divisão futura entre geometria/material/módulos não foi definida | Permanecem fora da fabricação inicial de formatos; não copiar automaticamente a expressão desenhada | [R076]–[R080], [R050], [R087] e instrução de escopo |
| Orelhas | São peças separadas na decomposição geral; apoios laterais desenhados não especificam encaixes | Reconhecidas no sistema completo, fora do primeiro experimento | [R049], [R050], [R087] |
| Corpo | Segundo nível: cabeça, conjunto superior e conjunto inferior; interfaces futuras no pescoço e cintura | Contexto para evolução, sem corpo ou rigging nesta etapa | [R099], [R100] |

A base feminina não deve conservar um nariz completo apenas porque ele aparece no desenho de “base sem componentes”. Também não se deve copiar o bloco nasal masculino como se fosse um encaixe medido. Essas formas são ambiguidades a resolver no desenho da interface.

A proposta de agrupar os dois olhos em um GLB conserva objetos esquerdo/direito separados internamente. Ela facilita uma troca coerente de aparência e espaçamento; não exige fundir os olhos em uma malha nem resolve antecipadamente animação ou rig.

## 3. Contrato de interfaces

### Cabelo ↔ base

**Proposta para o primeiro ensaio:** uma região craniana compatível, construída a partir da base piloto e compartilhada pelas cinco bases. Preservar os contornos faciais documentados:

| Base feminina | Identidade a conservar | Isolada / montada |
|---|---|---|
| 1 | Mandíbula suave, queixo pequeno e afunilamento moderado | [R076] / [R088] |
| 2 | Mandíbula mais angular e relativamente larga | [R077] / [R089] |
| 3 | Bochechas cheias, face arredondada e queixo curto | [R078] / [R090] |
| 4 | Terço inferior alongado, estreito e queixo pontudo | [R079] / [R091] |
| 5 | Maçãs largas, queixo fino e contorno mais compacto que 4 | [R080] / [R092] |

A fronteira aqui é uma relação entre superfícies, não uma exigência de soldar cabelo e pele. Conferir interior da calota, linha frontal, têmporas e nuca. Folga, espessura e eventual sobreposição interna precisam ser medidas no piloto; valores antes sugeridos não são cotas do catálogo.

Um cabelo volumoso pode esconder falhas. Cortes rentes exigirão ensaio específico de transição e cor da pele: [R062] isolado e [R004] montado mostram esse problema. Cabelos longos também exigirão conferir pescoço e, na etapa do corpo, ombros. A casca lateral do moicano permanece ambígua em [R010].

A opção masculina 4 significa ausência de módulo: seleção sem cabelo, sem fabricar uma “peça careca”. Evidência: [R067] e [R010]. O catálogo contém 24 escolhas de cabelo, das quais 23 representam cabelo físico.

### Olhos ↔ base

**Proposta a validar:** o módulo ocular inclui uma região de pele ao redor das pálpebras. Seu limite externo deve encontrar uma borda correspondente na base; a abertura palpebral, posição interna dos globos e aparência da pele podem variar dentro desse limite.

As famílias visuais do relatório são semicerrada (1/2/8), aberta (3/4), amendoada (5) e arregalada/afastada (6/7). Isso não fixa o número de malhas. Olheiras pertencem à aparência da pele; trocar somente a cor da íris não reproduz o catálogo.

Os olhos 6/7 têm maior afastamento e órbitas ajustadas em [R038], [R039], com exemplo montado em [R006]. Portanto:

- O contorno externo candidato precisa comportar a abertura e o afastamento extremos sem invadir nariz, sobrancelhas ou silhueta lateral.
- Se isso não funcionar, rever a região orbital da base ou criar uma versão explicitamente compatível da interface. Não ocultar ajustes por combinação como se o encaixe fosse universal.
- A divisão entre base e pele ocular deve deixar um único responsável por cada superfície visível, evitando pele duplicada e sobreposição coplanar.
- O primeiro piloto de base + cabelo não certifica essa interface. Uma cavidade ilustrada tampouco fornece os vértices de um recorte pronto.

### Nariz ↔ base

**Proposta a validar:** um perímetro de junção correspondente na base e nos narizes compatíveis. A superfície facial dentro desse perímetro não poderá competir com a superfície do nariz montado.

A região externa da junção deve conservar posições de contato, transição de cor e sombreamento. A forma da ponte, ponta e asas varia no interior do módulo. Se os extremos do catálogo não couberem nesse perímetro sem perder identidade, revisar a interface antes de produzir todas as variantes.

[R019] e [R023] mostram diferenças frontais; [R016] informa a relação com rostos montados. Projeção da ponta e calombo dorsal permanecem estimados quando não documentados por perfil aplicável. Não inferir profundidade física da grade gráfica.

### Dados que cada interface deverá registrar

Na futura cena mestre, cada interface terá um identificador e revisão, partes participantes, sistema de coordenadas, região de contato e critério de verificação. Para junções de pele, registrar a correspondência ordenada das bordas, posições, estratégia de normais e continuidade de material/UV quando houver textura. Preservar as facetas intencionais; remover a costura artificial não significa suavizar o rosto inteiro.

O cabelo terá uma superfície de referência e envelope de folga; olhos e nariz terão bordas de pele. O piloto feminino 01 testou apenas a calota contra a base 1 e preservação geométrica na exportação com tolerância de 1 µm. Interfaces faciais definitivas continuam não produzidas. Medições e correção da folga interna estão no relatório do piloto.

## 4. Referencial comum e cena mestre

**Convenção técnica proposta, não extraída das imagens:**

- Trabalhar em metros. No Blender, adotar +Z para cima, frente em -Y e plano de simetria X = 0.
- Usar uma única raiz de montagem, em (0, 0, 0), com rotação zero e escala unitária. Definir sua relação com o crânio na base piloto e preservá-la em todas as variantes.
- Manter cada componente em sua posição final relativa a essa raiz. Pivôs internos futuros, como centros dos olhos, não substituem o referencial de montagem.
- Não centralizar ou redimensionar cada arquivo independentemente durante a exportação/importação. Uma eventual conversão de eixos deve ser comum a todas as peças e verificada na reabertura.
- A altura inicial de 0,24 m é referência provisória de escala, medida do queixo ao topo do crânio, sem cabelo e sem pescoço. A revisão local R02 resultou em 0,226 m. Não usar essa altura como proporção estética obrigatória nem normalizar cada variante pela própria caixa delimitadora; preservar o referencial comum e o encaixe craniano.
- A futura ligação ao corpo terá um ponto de conexão próprio. A origem comum de exportação não precisa coincidir com um pivô de animação do pescoço.

A estrutura conceitual é uma raiz com a base selecionada e o cabelo; olhos, nariz e orelhas serão acrescentados conforme o escopo evoluir. Variantes ficam organizadas no mesmo arquivo mestre, mas somente a seleção da montagem entra em cada exportação.

A visualização explodida usa instâncias vinculadas ou deslocamentos temporários de apresentação. As malhas continuam compartilhadas; os deslocamentos de apresentação não entram nos GLBs de montagem. Avaliações de modificadores, se necessárias, devem derivar dos mesmos objetos e das mesmas configurações.

Uma cena glTF pode conter uma hierarquia de nós com transformações próprias. Essa organização permite preservar componentes na montagem; não comprova encaixe nem implica soldagem dos vértices. [Khronos — Scenes and Nodes](https://github.khronos.org/glTF-Tutorials/gltfTutorial/gltfTutorial_004_ScenesNodes.html).

## 5. Sequência de validação e entregáveis futuros

| Etapa | Verificação | Evidência exigida para avançar |
|---|---|---|
| Conteúdo da base | Fechar pescoço e tratamento orbital/nasal; registrar componentes ausentes e regiões estimadas | Decisões documentadas, sem interpretar a exclusão de olhos/nariz como exclusão automática de interfaces |
| Primeiro par | Base feminina 1 + Corte Feminino 1, separados e montados | Frente, ambos os lados, três quartos e costas; contato sem falhas visíveis e silhueta comparada a [R049], [R052], [R076], [R088], [R099] |
| Troca de bases | Cinco bases femininas × o mesmo cabelo | Cinco montagens; malha e transformação do cabelo invariáveis; identidade de cada rosto preservada |
| Exportação | GLB por base, um GLB de cabelo e montagem derivada dos mesmos objetos | Reimportar peças conjuntamente e montagem separadamente; comparar posição mundial, geometria, materiais, nomes e orientação |
| Integração no 3DC | Alternar bases, inspecionar e exportar a seleção | O resultado reaberto conserva a combinação; simples carregamento não aprova o encaixe |
| Ensaio facial posterior | Proposta de duas bases contrastantes × dois narizes × dois olhos × um cabelo | Oito combinações reais; incluir olho 6 ou 7. Depende da ampliação do escopo |

Para rastrear a fonte única, registrar em cada exportação os IDs dos módulos, revisão da geometria, revisão das interfaces e seleção usada. Comparar geometria avaliada e transformações, não exigir igualdade binária entre o GLB individual e o arquivo montado, que possuem estruturas diferentes.

Na leitura atual do código, [SceneManager.ts](../../src/three/SceneManager.ts) adiciona os objetos aos grupos de slots sem corrigir o encaixe. A troca em [App.tsx](../../src/App.tsx) altera a base preservando o cabelo. O experimento deve fornecer peças já compatíveis; slots e controles faciais futuros ainda exigem evolução do aplicativo.

O primeiro par foi produzido e reimportado conforme o relatório do piloto. A matriz de cinco bases, a integração no 3DC e o ensaio facial ampliado permanecem trabalhos futuros.

## 6. Inconsistências e decisões abertas

| Tema | Tratamento neste contrato | Fonte |
|---|---|---|
| Feminino 3 versus 6 | Manter apenas cinco bases individuais no catálogo conhecido. Não criar 6 nem declarar automaticamente que 6 é alias de 3 | Comparar [R016] com [R015] |
| Corte masculino 12 repetido | Preservar as duas ocorrências como exemplos do corte 12; não criar corte 13 | [R013] |
| Nariz/apoios remanescentes | Não tratar como interface técnica ou copiar como componente autorizado | [R049], [R050], [R087] |
| Pescoço na base piloto | Incluído provisoriamente, conforme decisão do usuário; conexão ao corpo ainda futura | [R076]–[R080], [R099], [R100] |
| Órbitas e região nasal | Definir limites e se haverá recorte, cavidade ou superfície provisória substituível; nenhuma solução está validada | [R033], [R038], [R039], [R016] |
| Vistas complementares | Usar as gerais como apoio. Não atribuir os perfis de uma cabeça a todas as variantes | [R049], [R050], [R051] |
| Perfil feminino rotulado | O “perfil esquerdo” é três quartos; não tratá-lo como projeção ortogonal | [R049] |
| Medidas e superfícies ocultas | Escala, espessuras, interior do cabelo, perfil específico e bordas são estimativas/projeto técnico até validação | Relatório completo e limites por arquivo |

A arquitetura definitiva da região orbital/nasal permanece aberta; o piloto usa regiões editáveis e interfaces provisórias. Pescoço e escala foram definidos provisoriamente na versão 0.2. Isso não reabre o escopo de olhos, sobrancelhas, nariz, boca, orelhas ou corpo no primeiro experimento.

## 7. Procedimento obrigatório durante cada etapa

1. Reler a seção da análise completa sobre a família trabalhada e os registros individuais envolvidos.
2. Localizar os arquivos pelo campo `path` no JSON e abrir o `absolute_path` correspondente. Usar o inventário para resolver nomes, sem adivinhar pastas.
3. Abrir a peça isolada, a combinação correspondente e as vistas gerais aplicáveis. Se uma peça não possui determinada vista, registrar a falta para aquela opção.
4. Registrar observação, inferência e escolha técnica separadamente, com os caminhos das imagens e a revisão do módulo.
5. Montar os próprios módulos, comparar isolado/montado/explodido e conservar uma única fonte de geometria.
6. Atualizar as evidências de compatibilidade somente após a inspeção e reabertura dos arquivos exportados.

## Referências originais reabertas nesta revisão

Os identificadores R001–R100 seguem a numeração do registro de cobertura do relatório. Os links abaixo foram obtidos do inventário JSON; apontam para arquivos locais e dependem da raiz de referências informada pelo usuário.

- [R004] — Cabeça & Rosto/Combinações de Cabeças/Combinações de Cabeças Femininas — Olhos, Rostos e Cabelos/olho (4) - exemplos femininos.png
- [R006] — Cabeça & Rosto/Combinações de Cabeças/Combinações de Cabeças Femininas — Olhos, Rostos e Cabelos/olho (6) - exemplos femininos.png
- [R010] — Cabeça & Rosto/Combinações de Cabeças/Combinações de Cabeças Masculinas Olhos,Rostos e Cabelos/Combinação 2.png
- [R013] — Cabeça & Rosto/Combinações de Cabeças/Combinações de Cabeças Masculinas Olhos,Rostos e Cabelos/Combinação 5.png
- [R015] — Cabeça & Rosto/Narizes — Módulos e Combinações/Combinacao feminina rostos e narizes/Narizes 4, 5 e 6 - Rostos 4, 5 e 6 - Cabelos 6, 8 e 9.png
- [R016] — Cabeça & Rosto/Narizes — Módulos e Combinações/Combinacao feminina rostos e narizes/Narizes 4, 5 e 6.png
- [R019] — Cabeça & Rosto/Narizes — Módulos e Combinações/narizes/nariz 1.png
- [R023] — Cabeça & Rosto/Narizes — Módulos e Combinações/narizes/nariz 5.png
- [R033] — Cabeça & Rosto/Olhos/Padrões de Olhos Femininos — Rosto 1 e Corte 1/olho (1) - marrom.png
- [R038] — Cabeça & Rosto/Olhos/Padrões de Olhos Femininos — Rosto 1 e Corte 1/olho (6) - marrom.png
- [R039] — Cabeça & Rosto/Olhos/Padrões de Olhos Femininos — Rosto 1 e Corte 1/olho (7) - azul.png
- [R049] — Cabeça & Rosto/Rosto Geral/Rosto Geral Feminino.jpeg
- [R050] — Cabeça & Rosto/Rosto Geral/Rosto Geral Masculino.jpeg
- [R051] — Cabeça & Rosto/Tipo de Corte de cabelo/Padrao de mudanca de cabelo.jpeg
- [R052] — Cabeça & Rosto/Tipo de Corte de cabelo/Tipos cortes/Feminino/Corte feminino 1 - Corte 1.jpeg
- [R062] — Cabeça & Rosto/Tipo de Corte de cabelo/Tipos cortes/Feminino/Corte feminino 11 - Corte 11.jpeg
- [R067] — Cabeça & Rosto/Tipo de Corte de cabelo/Tipos cortes/Masculino/Corte masculino 4 - Careca.jpeg
- [R076] — Cabeça & Rosto/Tipo de rosto/base feminina/base 1 feminino.jpeg
- [R077] — Cabeça & Rosto/Tipo de rosto/base feminina/base 2 feminino.jpeg
- [R078] — Cabeça & Rosto/Tipo de rosto/base feminina/base 3 feminino.jpeg
- [R079] — Cabeça & Rosto/Tipo de rosto/base feminina/base 4 feminino.jpeg
- [R080] — Cabeça & Rosto/Tipo de rosto/base feminina/base 5 feminino.jpeg
- [R087] — Cabeça & Rosto/Tipo de rosto/Padrao de mudanca de Rosto.jpeg
- [R088] — Cabeça & Rosto/Tipo de rosto/rosto  + cabelo feminino 1/rosto 1 + cabelo 1.jpeg
- [R089] — Cabeça & Rosto/Tipo de rosto/rosto  + cabelo feminino 1/rosto 2 + cabelo 1.jpeg
- [R090] — Cabeça & Rosto/Tipo de rosto/rosto  + cabelo feminino 1/rosto 3 + cabelo 1.jpeg
- [R091] — Cabeça & Rosto/Tipo de rosto/rosto  + cabelo feminino 1/rosto 4 + cabelo 1.jpeg
- [R092] — Cabeça & Rosto/Tipo de rosto/rosto  + cabelo feminino 1/rosto 5 + cabelo 1.jpeg
- [R099] — Exemplo Geral/FemaleExemple.jpeg
- [R100] — Exemplo Geral/MaleExemple.jpeg

[R004]: <originais/R004.png>
[R006]: <originais/R006.png>
[R010]: <originais/R010.png>
[R013]: <originais/R013.png>
[R015]: <originais/R015.png>
[R016]: <originais/R016.png>
[R019]: <originais/R019.png>
[R023]: <originais/R023.png>
[R033]: <originais/R033.png>
[R038]: <originais/R038.png>
[R039]: <originais/R039.png>
[R049]: <originais/R049.jpeg>
[R050]: <originais/R050.jpeg>
[R051]: <originais/R051.jpeg>
[R052]: <originais/R052.jpeg>
[R062]: <originais/R062.jpeg>
[R067]: <originais/R067.jpeg>
[R076]: <originais/R076.jpeg>
[R077]: <originais/R077.jpeg>
[R078]: <originais/R078.jpeg>
[R079]: <originais/R079.jpeg>
[R080]: <originais/R080.jpeg>
[R087]: <originais/R087.jpeg>
[R088]: <originais/R088.jpeg>
[R089]: <originais/R089.jpeg>
[R090]: <originais/R090.jpeg>
[R091]: <originais/R091.jpeg>
[R092]: <originais/R092.jpeg>
[R099]: <originais/R099.jpeg>
[R100]: <originais/R100.jpeg>
