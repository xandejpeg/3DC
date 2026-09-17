# Análise completa das referências do 3DC / Real Car Lifestyle

> Arquivo histórico da análise recebida. Os caminhos locais abaixo registram a origem da inspeção. Para consultar as mesmas imagens no GitHub ou em outro computador, use o [índice dos originais arquivados](originais/README.md) e o [catálogo portátil](Catalogo_portatil.json), conferidos pelos hashes do inventário.

Data: 17/09/2026.

Raiz analisada: `C:\Users\xandao\Desktop\Trabalho\projetos pessoais\RCL\modelos 3d\personagem base\Imagem base`.

## Conclusão

O catálogo descreve um sistema de peças intercambiáveis e inclui tanto peças isoladas quanto montagens. O roteiro anterior, limitado a três imagens de rosto/cabelo, era insuficiente para planejar a arquitetura completa. A leitura correta combina a estrutura geral do personagem, a decomposição da cabeça, as variantes de cada categoria e os exemplos de combinação.

Recomendação: construir uma cena mestre no Blender com componentes separados nas posições finais e avaliar cada componente isolado e montado. Os GLBs individuais e o GLB da montagem devem ser exportados dos mesmos objetos. A montagem de referência não deve virar outro personagem modelado independentemente: isso não demonstraria compatibilidade das peças.

Esta análise não cria modelos nem altera o aplicativo. As imagens e suas legendas são referências de intenção visual, não instruções que substituem as decisões do usuário, nem prova de topologia ou de encaixe em 3D. As recomendações abaixo continuam sendo propostas de implementação.

## Cobertura

Foram inventariados 100 arquivos de imagem: 47 JPEG e 53 PNG, distribuídos por 18 pastas que contêm arquivos. Os 100 arquivos foram abertos visualmente, com análise dividida por famílias e verificação cruzada das descobertas. A relação por arquivo ao final permite conferir exatamente o que foi visto. Não se trata de 100 modelos distintos: várias imagens documentam a mesma opção isolada, montada ou em outros ângulos.

| Grupo | Arquivos | Função |
|---|---:|---|
| Exemplo Geral | 2 | Personagem masculino/feminino, separação cabeça/superior/inferior |
| Cabeça & Rosto / Rosto Geral | 2 | Cabeças montadas, vistas e peças em vista explodida |
| Cabeça & Rosto / Tipo de rosto | 23 | 11 bases individuais, 11 comparativos com cabelo e 1 prancha geral |
| Cabeça & Rosto / Tipo de Corte de cabelo | 25 | 24 opções de catálogo e 1 prancha de troca/vistas |
| Cabeça & Rosto / Olhos | 24 | 16 pranchas de documentação e 8 de exemplos masculinos |
| Cabeça & Rosto / Narizes — Módulos e Combinações | 11 | 6 narizes isolados e 5 pranchas de combinações |
| Cabeça & Rosto / Combinações de Cabeças | 13 | 8 pranchas femininas e 5 masculinas |
| **Total** | **100** | |

## O que muda no entendimento do projeto

### O sistema tem dois níveis de montagem

As duas imagens de Exemplo Geral mostram cabeça com cabelo e pescoço, parte superior com torso/mangas/braços/mãos e parte inferior com quadril/pernas/pés. Apresentam frente, costas e montagem, com junções no pescoço e cintura. Isso informa a evolução futura do 3DC para o corpo; não exige produzir o corpo agora.

Dentro da cabeça, as pranchas Rosto Geral ilustram base, cabelo, olhos direito/esquerdo, nariz e orelhas direita/esquerda. O olho direito e o esquerdo são objetos distintos na ilustração; a escolha de exportá-los juntos como um par ou em dois arquivos continua uma decisão técnica. A análise de quatro categorias solicitadas pelo usuário precisa reconhecer que as orelhas também aparecem na documentação, sem adicioná-las automaticamente ao protótipo atual.

### Existem vistas complementares que o roteiro inicial não considerou

Rosto Geral Masculino e Rosto Geral Feminino mostram frente, costas e ângulos laterais. A prancha de mudança de cabelo também mostra quatro vistas do corte masculino 2. Exemplo Geral inclui a cabeça vista por trás.

Portanto, a afirmação genérica de que não há perfil ou traseira estava incompleta. Entretanto, essas vistas não documentam individualmente todas as 11 bases e todos os cortes. Além disso, o quadro chamado perfil esquerdo na prancha feminina é visualmente um ângulo de três quartos. O que falta deve ser descrito por opção, sem ignorar as vistas que já existem e sem tratá-las como vistas ortográficas calibradas.

### A base desenhada não é uma cabeça completamente lisa

Há cavidades para olhos nas bases. As legendas gerais mantêm sobrancelhas e boca na base; no masculino, também barba. As imagens incluem pescoço. Algumas formas residuais de nariz e apoios laterais permanecem desenhados mesmo onde a legenda fala em componentes removidos.

Isso conflita com parte do roteiro anterior, que excluía cavidades e pescoço, além da interpretação que retirava todos os detalhes. O usuário havia limitado a fabricação inicial aos formatos de rosto e um cabelo, sem olhos/nariz e outros módulos. Essa limitação de fabricação não resolve por si só a geometria das interfaces futuras. Não devemos apagar as interfaces necessárias nem adicionar boca/sobrancelhas/barba apenas porque uma legenda as mantém. O conteúdo exato da base precisa ser registrado antes de gerar a malha.

### Os olhos incluem forma, pálpebras, pele ao redor e posição

As 16 pranchas de documentação mostram oito padrões em versões masculina/feminina. Incluem módulo isolado, frente, três quartos, perfil, detalhe no rosto e aplicação montada. Há mudanças de abertura, pálpebras, dobra epicântica, olheiras, cor e, em alguns padrões, espaçamento. Não é um catálogo de oito cores aplicadas à mesma esfera.

Os padrões 6 e 7 explicitam maior afastamento dos olhos e órbitas ajustadas. Isso é decisivo: não podemos prometer que basta trocar um GLB com órbitas e posições invariáveis. Uma proposta a testar é o módulo ocular incluir pálpebras e uma região de transição de pele com limite externo padronizado, permitindo variação interna. Se esse limite não comportar os formatos desejados, será necessário adaptar a região orbital da base ou rever o contrato dos módulos. Isso deve ser validado no Blender antes de virar código de produção.

### Cabelo e nariz exigem tipos de encaixe diferentes

O cabelo pode ser construído como um volume externo separado sobre uma região craniana compatível. Existem cortes longos, cacheados, afro, raspados, com desenhos, coque, moicano e espinhos. Os cortes rentes expõem transições com a pele; os longos antecipam colisões com o pescoço e futuros ombros. A compatibilidade de um corte volumoso não comprova a dos cortes rentes.

Há 12 opções masculinas, mas a opção 4, Careca, é explicitamente ausência de módulo. Somadas às 12 opções femininas, são 24 escolhas de catálogo, das quais 23 mostram cabelo físico. O aplicativo deve conseguir representar a escolha sem cabelo.

Os seis narizes isolados têm principalmente vista frontal ampliada. As pranchas de aplicação ajudam com proporção e relação com o rosto, mas não documentam todas as profundidades nem a superfície de junção. Para preservar nariz como GLB separado, recomenda-se projetar uma borda comum de conexão com a base e testar continuidade de posição, cor e sombreamento. Apenas sobrepor uma peça sobre uma cabeça fechada não demonstra continuidade da pele.

## Inconsistências e limites que precisam acompanhar os arquivos

- As bases femininas individuais disponíveis são 1 a 5. Há uma prancha de narizes/cabelos que cita rosto feminino 6; não existe arquivo individual feminino 6 neste inventário. A correspondência deve ser resolvida sem inventar uma sexta base por causa da legenda.
- A prancha masculina Combinação 5 repete o corte 12 em duas colunas. Isso não autoriza criar corte 13.
- Certas legendas dizem que componentes foram removidos, mas continuam aparecendo volumes nas bases; são ambiguidades visuais, não prova de como cortar a malha.
- Algumas pranchas dizem manter o mesmo rosto, enquanto há pequenas diferenças aparentes de nariz, sobrancelhas, abertura dos olhos e proporções. A comparação não deve assumir equivalência exata de pixels ou de câmera.
- As combinações apresentadas são amostras. Elas não cobrem todas as combinações possíveis entre bases, cabelos, olhos e narizes.
- Não há medidas físicas, topologia de bordas, espessuras internas, UVs, rigging ou pesos de deformação definidos pelas imagens. A escala de 0,24 m anteriormente proposta é uma convenção de trabalho, não uma medida extraída do catálogo.
- O estilo geral é estilizado e facetado. O contraste entre planos deve ser preservado sem confundir facetas pintadas/iluminadas da imagem com uma topologia já especificada.

## Fluxo recomendado para modelar e validar

1. **Definir o contrato da base e dos módulos.** Registrar o que pertence à cabeça, ao módulo ocular, ao nariz e ao cabelo; tratar pescoço, sobrancelhas, boca, barba e orelhas como decisões explícitas, à luz da instrução do usuário e do catálogo. Usar um sistema comum de coordenadas, origem e escala. Padronizar as bordas de contato necessárias, sem impor o mesmo volume ao rosto inteiro.
2. **Construir um conjunto piloto na mesma cena.** Uma base, um cabelo, um nariz e um par de olhos como objetos separados, caso o piloto ampliado seja adotado. A alternativa de começar apenas com base e cabelo continua possível, desde que se planejem previamente os encaixes futuros e não se feche a cabeça como uma superfície genérica incompatível com eles.
3. **Inspecionar isolado, montado e em vista explodida.** As três apresentações devem mostrar os mesmos objetos. Comparar frente, perfil, três quartos e costas usando todas as referências aplicáveis; registrar as regiões estimadas.
4. **Testar troca real.** Depois do primeiro conjunto, acrescentar outra base contrastante, outro nariz e outro padrão ocular; incluir um olho com abertura/espaçamento diferente no ensaio. Duas bases × dois narizes × dois padrões de olhos × um cabelo produzem oito combinações de teste. Esse é um teste proposto, não uma lista de produção já autorizada.
5. **Exportar e reabrir.** Cada peça deve conservar seu referencial. Exportar também a montagem formada por essas peças e reabrir os arquivos para conferir posição, materiais, nomes, continuidade e interpenetrações. Um GLB montado pode manter vários objetos; a união efetiva dos vértices é uma operação distinta.
6. **Integrar no 3DC.** O aplicativo atual tem slots base/cabelo. Testar olhos/narizes separadamente no Blender já ajuda a geometria, mas alterná-los no 3DC exigirá ampliar o aplicativo. Não apresentar essa capacidade como existente.
7. **Expandir somente após o teste de compatibilidade.** As famílias completas e a geração dos personagens/NPCs dependem dessa validação. O estudo das imagens do corpo orienta interfaces futuras sem iniciar corpo ou rigging nesta análise.

Referência técnica sobre composição de objetos e transformações no glTF: [Khronos — Scenes and Nodes](https://github.khronos.org/glTF-Tutorials/gltfTutorial/gltfTutorial_004_ScenesNodes.html). Essa documentação sustenta a possibilidade de manter objetos separados no mesmo arquivo; não certifica que as peças deste projeto já se encaixam.

## Correção a transmitir ao Codex CLI

O roteiro de três imagens foi substituído por esta análise de catálogo. Antes de modelar, use todas as famílias relevantes: Exemplo Geral, Rosto Geral, padrões de rosto/cabelo, peças individuais, documentação de olhos/narizes e combinações. Não repita a conclusão de que não há perfis/traseiras, não transforme olho em simples troca de cor, não conclua que toda base deve ser lisa e fechada e não trate imagens contraditórias como medidas exatas.

Entregue primeiro um contrato de peças e interfaces baseado neste inventário, citando os arquivos que sustentam cada decisão. A montagem deverá reutilizar os próprios módulos, com uma única fonte de geometria. Este documento não aprova automaticamente todas as propostas: distingue as evidências visuais, a intenção do usuário e os pontos ainda não definidos.

## Observações por família

As seções seguintes registram a análise especializada dos grupos. Depois delas está o registro de cobertura por arquivo, com limitações individuais.



---

# Auditoria visual: formas de rosto e rostos gerais

Foram inventariados com `rg --files` e vistos diretamente com `view_image` **25 de 25 arquivos**: 23 em `Cabeça & Rosto/Tipo de rosto` e 2 em `Cabeça & Rosto/Rosto Geral`. Todos os originais foram tratados como somente leitura. Nenhum modelo foi criado ou alterado. O JSON acompanhante registra papel, observações e limitações de cada imagem com caminho relativo a `Imagem base`.

## Cobertura e organização observadas

| Grupo | Arquivos | Vistas efetivamente disponíveis |
|---|---:|---|
| Bases masculinas 1–6 | 6 | Uma vista em três quartos por base |
| Bases masculinas 1–6 + corte 1 | 6 | Cabeça montada frontal; base em três quartos |
| Bases femininas 1–5 | 5 | Uma vista em três quartos por base |
| Rostos femininos 1–5 + cabelo 1 | 5 | Cabeça montada frontal/quase frontal; base em três quartos |
| Padrão de mudança de rosto | 1 | Frente, dois perfis laterais e costas da cabeça masculina montada; decomposição e base em três quartos |
| Rosto geral masculino | 1 | Frente, dois perfis laterais e costas da cabeça montada; decomposição e base em três quartos |
| Rosto geral feminino | 1 | Frente, perfil à direita da imagem, costas e três quartos rotulado como perfil esquerdo; decomposição e base em três quartos |

Não se deve concluir que o catálogo não tem costas ou perfis. Eles existem para as cabeças montadas das pranchas gerais. Porém, essas vistas **não são fornecidas individualmente para cada uma das onze bases faciais**, nem para seus encaixes internos. A imagem geral feminina também não entrega dois perfis ortogonais: o quadro chamado “perfil esquerdo” deixa os dois olhos visíveis.

## Formas e correspondências

Os números das seis bases masculinas e cinco femininas correspondem aos números das respectivas montagens. A leitura visual reforça essas associações, sem provar que sejam projeções de um mesmo objeto 3D. A maior variação está nas bochechas, mandíbula e queixo; o cabelo, a expressão e a região superior do rosto mantêm linguagem semelhante.

| Forma | Diferença visível, sem atribuir categoria anatômica oficial |
|---|---|
| Masculina 1 | Mandíbula moderadamente afunilada e queixo intermediário |
| Masculina 2 | Terço inferior estreito e afunilado |
| Masculina 3 | Mandíbula ampla e queixo mais horizontal/retangular |
| Masculina 4 | Bochechas e mandíbula mais cheias/arredondadas |
| Masculina 5 | Face estreita e alongada, recuo abaixo das maçãs e queixo fino |
| Masculina 6 | Mandíbula robusta, queixo amplo e base inferior quase horizontal |
| Feminina 1 | Mandíbula suave e queixo pequeno, afunilamento moderado |
| Feminina 2 | Mandíbula mais reta/angular e relativamente larga |
| Feminina 3 | Bochechas cheias e queixo curto, face arredondada |
| Feminina 4 | Terço inferior mais longo, bochechas estreitas e queixo pontudo |
| Feminina 5 | Maçãs largas e queixo fino, contorno mais compacto que 4 |

São descrições qualitativas. Os arquivos não fornecem parâmetros ou cotas; algumas diferenças, especialmente entre masculinas 2/5 e 3/4/6, são graduais. Barba e sombreamento também alteram a leitura do contorno masculino.

O corte masculino 1 é castanho, curto e construído visualmente por mechas grandes e pontudas. O feminino 1 é castanho, assimétrico, com franja lateral longa à esquerda da imagem e nuca mais curta. As montagens mostram uma intenção clara de usar o mesmo estilo de cabelo em várias formas faciais. Elas não revelam se o cabelo foi reposicionado, escalado ou remodelado entre exemplos.

## O que permanece nas chamadas bases

Todas as onze bases mantêm **sobrancelhas, boca e pescoço**, além da forma do rosto e órbitas vazias. Todas as seis masculinas mantêm **barba**, bloco/placa na região nasal e saliência lateral achatada na região da orelha. Todas as cinco femininas mantêm **um pequeno nariz/relevo nasal**; nelas não há orelha externa evidente. Sobrancelhas e boca já impõem expressão de olhar cerrado/cantos baixos.

Por isso, “base sem componentes” não significa base neutra e sem detalhes. As próprias pranchas dizem manter sobrancelhas/boca e, no masculino, barba. O texto diz nariz/orelhas removidos, mas o masculino retém volumes nesses locais; o feminino conserva pequeno nariz. Pode haver intenção de representar apoios ou formas residuais para encaixe, mas **isso é hipótese**, não algo resolvido pelo desenho.

A barba ocupa a superfície e o contorno de mandíbula/bochechas masculinas. Não é possível decidir só com a referência se seria material, malha sobreposta ou parte esculpida da pele. O mesmo vale para a separação real das sobrancelhas. Facetas aparentes, inclusive as menores sobre a barba masculina 4, não são prova de conectividade, quantidade de polígonos ou topologia.

## Rótulos, ambiguidades e qualidade

- `Padrao de mudanca de Rosto.jpeg` contém uma prancha masculina explodida, e não uma comparação dos onze rostos. Sua composição é quase a mesma de `Rosto Geral Masculino.jpeg`, mas o contorno mandibular é visivelmente mais largo; não tratar automaticamente como duplicata exata.
- A base masculina 1 é visualmente compatível com a base da prancha geral masculina. A feminina 1 se aproxima da prancha geral feminina. As demais bases têm correspondência numerada nas montagens, mas não pranchas próprias com quatro vistas.
- Os exemplos masculinos 3 e 6 contêm rodapés que mencionam “três rostos” e “mesmo encaixe”, apesar de cada arquivo conter um único par montado/base. Isso provavelmente reflete um recorte de prancha maior, hipótese apoiada também por bordas de painéis; o texto não é comprovação de encaixe.
- O “perfil esquerdo” feminino é três quartos. Não converter o rótulo em certeza de orientação ortogonal.
- Os recortes masculinos 1–3 medem somente 252–265 × 336 pixels. A base masculina 1 mede 267 × 328 e a feminina 1 somente 354 × 190. Eles servem para silhueta/identidade visual geral, com pouca definição para junções finas.
- As bases masculinas 2–6 têm aproximadamente 1620 × 970 pixels e tornam os volumes mais legíveis. As demais bases femininas têm aproximadamente 570–590 × 370 e são relativamente suaves. Maior resolução não transforma a ilustração em prova de modelo 3D.

## Consequência para a leitura modular, antes de qualquer decisão de modelagem

O grupo demonstra a intenção visual de **onze formas faciais, dois estilos de cabelo usados em exemplos e montagem com olhos/nariz/orelhas**. Demonstra também a aparência final esperada: rosto, olhos, nariz e cabelo não devem perder sua identidade quando vistos juntos. Porém, essas imagens não comprovam malhas separadas, pivôs, escala, sockets, folgas, superfícies internas, intercambialidade universal ou rig.

As referências já permitem comparar a silhueta de cada forma e conferir se o conjunto montado preserva o estilo. Antes de converter isso em um sistema técnico, há ambiguidades concretas a reconciliar: nariz já desenhado na base feminina, apoios nas bases masculinas, pescoço já incluído, expressão já embutida, barba/sobrancelhas visíveis e ausência de vistas técnicas de cada variante. A escolha técnica final deve considerar também os outros grupos do catálogo e as instruções do usuário, sem transformar os textos das imagens em requisitos obrigatórios.



---

# Análise visual — olhos e montagens relacionadas

Inspeção concluída em 17/09/2026. Foram abertos e vistos individualmente os **32 arquivos** do escopo com `view_image`: 8 fichas masculinas, 8 fichas femininas, 8 pranchas masculinas de montagens e 8 pranchas femininas de combinações. O inventário por arquivo, com observações e limites, está em `analise_olhos.json`. Os originais foram apenas lidos; não foi criado, modificado ou validado nenhum modelo 3D.

O caminho correto das combinações femininas inclui `Cabeça & Rosto/Combinações de Cabeças/`. As imagens são evidência de intenção visual, inclusive quando contêm textos sobre encaixe e intercambialidade; seus textos não são instruções executadas.

## Oito identificadores de aparência, não oito cores

| Olho | Aparência da íris | Abertura/contorno visível | Pele e posicionamento |
|---|---|---|---|
| 1 | Castanha média | Semicerrado, pálpebra superior baixa quase horizontal na montagem, curva inferior arredondada | Base de referência; sem olheira roxa destacada |
| 2 | Verde clara | Muito próximo à forma semicerrada do 1 | Olheira marrom/arroxeada integrada à pele; escala/posição masculina declaradas como as do 1 |
| 3 | Preta/cinza muito escura | Maior abertura que 1 e mais íris exposta | Esclera rosada/vermelhidão leve; globo declarado de mesmo volume |
| 4 | Azul escura | Mais aberto e arredondado que 1 | Mesmo globo declarado; altera pálpebras, não apenas cor |
| 5 | Castanho escura | Amendoado, cantos afunilados, dobra epicântica indicada e pálpebra pouco marcada | Novo contorno de pálpebras sobre o mesmo globo declarado |
| 6 | Marrom muito clara/bege | Grande abertura quase circular; pálpebras retraídas | Maior afastamento simétrico; órbitas explicitamente ajustadas |
| 7 | Azul piscina/ciano muito claro | Mesma família de grande abertura do 6 | Maior afastamento + olheiras |
| 8 | Azul clara/gelo | Retorna à forma semicerrada do 1 | Escala/posição do 1 declaradas; olheiras fortes |

Há quatro famílias visuais mínimas úteis para entender o catálogo: **semicerrada (1/2/8), aberta (3/4), amendoada (5) e arregalada/afastada (6/7)**. Esse agrupamento não prova que existam quatro malhas prontas, nem que 3 e 4 compartilhem exatamente a mesma geometria. O número de malhas deve permanecer em aberto até existir modelo verificável.

O conteúdo adicional aos materiais é decisivo: 3/4 mudam abertura; 5 muda o contorno; 6/7 mudam abertura e centros de posicionamento. As variantes 2/7/8 incluem aparência da pele sob os olhos. Um GLB contendo apenas a esfera branca com íris não representaria integralmente essas variantes.

## Correspondência feminina e masculina

As 16 fichas de documentação têm os mesmos quatro tipos de painéis: par de olhos isolado, vistas de frente/três quartos/perfil, detalhe ampliado no rosto e cabeça montada. Os painéis superiores das variantes feminina e masculina correspondentes **repetem visivelmente o desenho ocular**: esfera facetada, pálpebra em calota, íris radial, pupila preta e reflexo branco. É forte evidência de um catálogo de olhos comum às duas linhas.

As aplicações femininas mudam o enquadramento facial, sobrancelhas e, em vários casos, o prolongamento externo do contorno superior/cílios. Esse prolongamento não está descrito no módulo isolado. A expressão séria também depende das sobrancelhas e da boca; não deve ser atribuída apenas ao olho.

Nas fichas femininas, todas as aplicações se chamam rosto 1/corte 1, mas nariz, inclinação das sobrancelhas, contorno facial e pose sofrem pequenas derivas entre desenhos. Essas diferenças não demonstram novos IDs de rosto. Também não é possível afirmar, pelas imagens, que as montagens tenham sido renderizadas de uma única malha com materiais trocados.

## Montagens masculinas

Cada uma das 8 pranchas usa o **rosto masculino 1** com três cortes, totalizando **24 exemplos**:

- Corte 1, Bagunçado 1: mechas pontiagudas com direção lateral.
- Corte 2, Bagunçado 2: mechas mais radiais e franja pontiaguda.
- Corte 3, Hi Fade: topo baixo e curto, superfície facetada, laterais curtas.

A linha superior mostra os cabelos isolados; a intermediária mostra a montagem frontal; a inferior repete a base em três quartos, sem cabelo nem olhos, com sobrancelhas/barba e região nasal simplificada em bloco. A relação cabelo separado + cabeça receptora é clara como intenção visual.

Nos exemplos dos olhos **6 e 7**, a linha da base recebe a legenda de encaixe específico do olho. Isso concorda com as fichas que pedem órbitas ajustadas ao maior afastamento. Uma decisão futura de sockets únicos fixos para os oito olhos precisaria resolver esse requisito, e não ignorá-lo.

Essas folhas não demonstram todas as cabeças masculinas, nem todos os cabelos do catálogo. São 24 combinações sobre uma única família facial.

## Montagens femininas e correspondências exatas

Cada célula abaixo registra **rosto + corte** da esquerda para a direita; a variante ocular é a indicada na primeira coluna.

| Olho | Coluna 1 | Coluna 2 | Coluna 3 |
|---|---|---|---|
| 1 | Rosto 1 + corte 1 | Rosto 2 + corte 2 | Rosto 3 + corte 3 |
| 2 | Rosto 4 + corte 4 | Rosto 5 + corte 5 | Rosto 3 + corte 6 |
| 3 | Rosto 1 + corte 7 | Rosto 2 + corte 8 | Rosto 3 + corte 9 |
| 4 | Rosto 4 + corte 10 | Rosto 5 + corte 11 | Rosto 3 + corte 12 |
| 5 | Rosto 4 + corte 1 | Rosto 5 + corte 2 | Rosto 3 + corte 3 |
| 6 | Rosto 1 + corte 4 | Rosto 2 + corte 5 | Rosto 3 + corte 6 |
| 7 | Rosto 4 + corte 7 | Rosto 5 + corte 8 | Rosto 3 + corte 9 |
| 8 | Rosto 1 + corte 10 | Rosto 2 + corte 11 | Rosto 3 + corte 12 |

São **24 exemplos escolhidos**, cobrindo cinco rostos e doze cortes. Não é uma tabela de todas as combinações possíveis. O número de “cabeça feminina” acompanha o rosto, enquanto o corte mantém sua numeração própria.

Os cortes vistos nessas folhas são: 1 curto assimétrico pontiagudo; 2 longo em camadas com franja; 3 rabo lateral baixo com franja; 4 bob reto com franja; 5 dois rabos baixos; 6 médio dividido ao centro; 7 cacheado curto; 8 cachos/ondas em espiral de comprimento médio; 9 afro volumoso arredondado; 10 longo ondulado assimétrico com uma lateral raspada; 11 topo curto cacheado com desenhos claros na lateral raspada; 12 longo ondulado dividido próximo ao centro. São descrições visuais, sem inventar nomes oficiais.

Os rostos 4 e 5 têm queixos mais pontudos, com 4 especialmente alongado; 3 tem maior largura e arredondamento. Os rostos 1/2 apresentam diferenças mais moderadas de contorno oval/mandíbula. A base feminina inferior mantém um nariz pequeno visualmente integrado, ao contrário do bloco nasal ilustrativo nos exemplos masculinos. Portanto, a separação do nariz como asset não está documentada de forma igual nestas duas séries.

Nas combinações de olhos 1–5 e 8 aparece olhar lateral ou para cima em parte dos exemplos; 6/7 aparecem mais arregalados e predominantemente frontais. Direção do olhar é pose do globo/pupila e não novo ID de olho. Nenhuma animação é mostrada.

## Cobertura de vistas e pontos ainda não comprovados

As fichas oculares oferecem frente, três quartos e **um perfil ilustrativo**, além de detalhe frontal e aplicação. Isso informa forma geral e cobertura palpebral. Não há vistas superior/inferior, anatomia posterior, perspectiva calibrada, cotas ou garantia de que cada desenho corresponda à mesma projeção de uma malha.

Nas pranchas de combinação, cabelos isolados aparecem predominantemente de frente ou em leve três quartos. As bases aparecem em três quartos; montagens são principalmente frontais. Não há cobertura posterior suficiente para fechar volumes de cabelo ou crânio somente com este conjunto.

Os limites mais importantes são:

1. **Intercambialidade é intenção.** Não foram vistos pivôs, escalas, eixos, unidades, soquetes, glTF/GLB, topologia ou montagem real.
2. **Olho e pele se cruzam.** Pálpebras, olheiras e cílios ultrapassam o globo; a futura divisão de componentes deve declarar a quem pertencem.
3. **6/7 exigem posicionamento especial.** O próprio catálogo diz afastamento maior e órbitas ajustadas, sem fornecer medidas.
4. **Contornos mudam.** Um recorte facial fixo idêntico para semicerrado, amendoado e arregalado não está demonstrado.
5. **As legendas têm limites.** A ficha feminina do olho 2 diz mesma escala/posição “do Olho 2”, referência circular. Essa legenda não equivale a uma dimensão.
6. **Derivas de desenho impedem metrologia.** Proporções faciais, nariz, sobrancelhas, direção de olhar e pequenos detalhes de cabelo variam mesmo quando rótulos se repetem.
7. **Não há prova de operação no RCL/3DC.** Compatibilidade de importação, materiais, orientação, montagem, deformação e animação permanece fora do que essas imagens podem demonstrar.

Este relatório completa a leitura dos 32 arquivos atribuídos; não encerra a análise do restante do catálogo nem fixa a arquitetura final de modelagem.




---

# Análise visual de narizes e combinações masculinas

Data: 2026-09-17. Foram abertos e vistos individualmente com `view_image` **16 arquivos**: seis narizes isolados, três pranchas femininas de narizes, duas pranchas masculinas de narizes e cinco pranchas masculinas de olhos/rostos/cabelos. O inventário individual está em `analise_narizes_combinacoes.json`, com caminhos relativos a `Imagem base`. Nenhum original foi modificado e nenhuma modelagem foi feita.

## Seis variantes de nariz

| ID | Forma efetivamente visível | Intenção adicional do rótulo |
|---|---|---|
| 1 | Ponte intermediária, ponta arredondada e asas moderadas | Original |
| 2 | Ponta globosa muito larga e asas arredondadas maiores | Gordinho e protuberante |
| 3 | Forma compacta com ponta e asas menores | Curto e fino |
| 4 | Ponte muito longa/estreita, ponta angular pequena e narinas visíveis | Fino, comprido e empinado |
| 5 | Ponte longa com alteração central de largura/facetas e ponta alongada | Longo, fino e com calombo |
| 6 | Ponte larga, ponta grande alongada e asas largas | Grande, largo e alongado |

A família usa pele alaranjada e acabamento facetado comuns. As variantes são diferenças de forma, não seis cores. Todas as vistas isoladas são frontais; **protuberância, empinamento e calombo dorsal são intenções escritas que ainda precisam de perfil para definição fiel**. A grade é gráfica e não oferece unidade física comprovada. Não há traseira dos módulos, espessura de pele, interface de união ou origem/escala documentada.

## Correspondências efetivamente apresentadas

- Feminino, narizes1/2/3: rosto1+nariz1+corte1; rosto2+nariz2+corte1; rosto3+nariz3+corte1.
- Feminino, narizes4/5/6 com corte1: rosto4+nariz4; rosto5+nariz5; **rosto3+nariz6**.
- Feminino, cortes6/8/9: rosto4+nariz4+corte6; rosto5+nariz5+corte8; **rosto6+nariz6+corte9**.
- Masculino, narizes1/2/3: rostos1/2/3 e respectivos narizes, todos com corte1.
- Masculino, narizes4/5/6: rostos4/5/6 e respectivos narizes, todos com corte1.
- Combinação masculina1: olho1 + cabelo1/2/3 + rosto1/2/3.
- Combinação masculina2: olho1 + cabelo3/4/5 + rosto3/4/5.
- Combinação masculina3: olho2 + cabelo6/7/8 + rosto1/2/3.
- Combinação masculina4: olho7 + cabelo8/9/10 + rosto4/5/6.
- Combinação masculina5: olho5 + cabelo11/12/12 + rosto1/2/3.

As pranchas oferecem exemplos selecionados. Não representam todas as combinações cruzadas e não comprovam que os objetos3D têm transformações iguais.

## Conflitos e decisões de catálogo

1. **Rosto feminino3 versus6:** a prancha de narizes4/5/6 com corte1 chama a terceira base de3; a prancha com cortes6/8/9 chama uma base visualmente muito semelhante, arredondada, de6. Confirmar se é renumeração/erro da prancha ou uma variante planejada. Não inventar uma sexta base por inferência de rótulo.
2. **Rostos masculinos incluem6.** O catálogo feminino não deve ser deduzido desse total.
3. **Cabelo masculino4 é ausência de módulo.** A própria prancha diz “SEM CABELO / NENHUM MÓDULO”.
4. **Combinação5 repete cabelo12.** O terceiro exemplo testa o mesmo corte em outro rosto; não é cabelo13.
5. **Moicano5:** a referência isolada inclui uma casca escura nas laterais; a montagem mostra laterais do couro cabeludo expostas. Definir na modelagem quais partes pertencem ao cabelo.
6. **Olho7:** bases são rotuladas “ENCAIXE OLHO7”. Isso sinaliza a necessidade de verificar compatibilidade; não estabelece por si só um encaixe universal ou exclusivo.

## Geometria, cor e fronteiras de módulos

- Olhos1 e2 têm abertura semicerrada e expressão cansada; olho2 acrescenta íris verde-clara e olheiras. Olho7 tem abertura grande/arredondada e íris azul-clara; olho5 tem contorno amendoado e íris escura. Há variações de **forma e aparência**, não apenas troca de cor. Os módulos de olhos isolados não estão entre estes16arquivos.
- Nos cabelos, mechas/pontas/cachos/coque definem volumes diferentes. Íris, pontas claras do corte12, desenhos raspados, olheiras e cor da pele são candidatos a controles de material ou superfície; as imagens não determinam a implementação.
- Bases inferiores não são cabeças lisas: mostram cavidades oculares, sobrancelhas, boca, pescoço e, nas masculinas, orelhas/barba e bloco nasal claro. Isso é referência visual de montagem, não instrução para incluir automaticamente todos esses componentes no primeiro escopo.
- Renders mostram continuidade visual entre nariz e face, mas não mostram como a união foi obtida. Um nariz independente exige decisão sobre contorno de contato, transição da pele e correspondência de materiais/normais; não basta exportar separado.
- Olhos precisam de uma fronteira definida entre globo, pálpebras, órbitas e pele ao redor. Uma face fechada e totalmente lisa não corresponde às bases com cavidades documentadas.

## Consequência para o fluxo de trabalho

Usar as referências isoladas para forma e as montadas para relação entre partes. Construir uma montagem mestre com módulos distintos e validar a montagem usando exatamente os módulos exportados. Uma segunda cabeça inteira esculpida separadamente não comprovaria encaixe.

Antes de fabricar todas as variantes, resolver o conflito feminino3/6 e definir interfaces de nariz/olhos/cabelo. Um protótipo cruzando duas bases de rosto contrastantes, dois narizes, dois tipos de olho e um cabelo testaria oito montagens. Isso é proposta de validação, não autorização presumida para começar a modelagem.

Não há vistas completas de perfil/traseira nem medidas nestes16arquivos. Partes ocultas continuam estimadas e devem ser identificadas como tal.




---

## Registro de cobertura — 100 arquivos

Todos os caminhos abaixo são relativos à raiz Imagem base informada no início. O inventário CSV/JSON ao lado deste documento inclui caminhos absolutos e hashes SHA-256.


### 001. Cabeça & Rosto/Combinações de Cabeças/Combinações de Cabeças Femininas — Olhos, Rostos e Cabelos/olho (1) - exemplos femininos.png

**Papel:** Três combinações femininas com olho 1, rostos e cabelos selecionados

**Observado:** Íris castanha, pupila preta circular e reflexo branco; esclera creme. Pálpebra superior grande cobre a parte alta da íris; abertura inferior arredondada e olhar semicerrado. Da esquerda para a direita: rosto 1 + corte 1 + olho 1; rosto 2 + corte 2 + olho 1; rosto 3 + corte 3 + olho 1. Corte 1: curto assimétrico com grandes mechas pontiagudas laterais; 2: longo em camadas com franja; 3: rabo lateral baixo com franja e mechas junto ao rosto. Estrutura de três linhas: cabelo isolado frontal/levemente em três quartos, cabeça montada predominantemente frontal, padrão de rosto sem cabelo/olhos em três quartos. Rosto 1 é mais estreito/oval e de queixo menor; 2 tem contorno de mandíbula mais amplo; 3 é mais arredondado e largo. As bases femininas inferiores preservam um nariz pequeno integrado visualmente; ao contrário das bases masculinas dos exemplos, não mostram o mesmo bloco retangular de indicação nasal. O olhar é deslocado lateralmente ou para cima em parte das montagens; é pose visual, não evidência de outra variante de globo.

**Limites:** São três combinações selecionadas, não uma matriz exaustiva de todos os rostos, cabelos e olhos. O corte tem seu próprio número; 'cabeça feminina N' nesta prancha acompanha o rosto N, não necessariamente o corte N. Sem vistas posteriores, cortes internos, espessura de cabelo, soquetes, medidas ou rig; compatibilidade 3D permanece não testada. Cores/aberturas e proporções sofrem pequenas variações de renderização; não extrair medidas exatas nem presumir identidade de malha a partir do rótulo.


### 002. Cabeça & Rosto/Combinações de Cabeças/Combinações de Cabeças Femininas — Olhos, Rostos e Cabelos/olho (2) - exemplos femininos.png

**Papel:** Três combinações femininas com olho 2, rostos e cabelos selecionados

**Observado:** Íris verde clara com aro escuro e pupila preta; abertura semicerrada visualmente próxima ao olho 1. Mancha marrom/arroxeada ampla sob o olho. Da esquerda para a direita: rosto 4 + corte 4 + olho 2; rosto 5 + corte 5 + olho 2; rosto 3 + corte 6 + olho 2. Corte 4: bob reto curto com franja reta; 5: dois rabos baixos e divisão central; 6: médio solto com divisão central e sem franja reta. Estrutura de três linhas: cabelo isolado frontal/levemente em três quartos, cabeça montada predominantemente frontal, padrão de rosto sem cabelo/olhos em três quartos. Rosto 4 é estreito e comprido com queixo muito pontudo; 5 tem contorno triangular mais moderado; 3 é largo/arredondado. As bases femininas inferiores preservam um nariz pequeno integrado visualmente; ao contrário das bases masculinas dos exemplos, não mostram o mesmo bloco retangular de indicação nasal. O olhar é deslocado lateralmente ou para cima em parte das montagens; é pose visual, não evidência de outra variante de globo.

**Limites:** São três combinações selecionadas, não uma matriz exaustiva de todos os rostos, cabelos e olhos. O corte tem seu próprio número; 'cabeça feminina N' nesta prancha acompanha o rosto N, não necessariamente o corte N. Sem vistas posteriores, cortes internos, espessura de cabelo, soquetes, medidas ou rig; compatibilidade 3D permanece não testada. Cores/aberturas e proporções sofrem pequenas variações de renderização; não extrair medidas exatas nem presumir identidade de malha a partir do rótulo.


### 003. Cabeça & Rosto/Combinações de Cabeças/Combinações de Cabeças Femininas — Olhos, Rostos e Cabelos/olho (3) - exemplos femininos.png

**Papel:** Três combinações femininas com olho 3, rostos e cabelos selecionados

**Observado:** Íris quase preta com aro cinza muito escuro, pupila preta e reflexo branco; esclera mais rosada nas laterais. Mais íris exposta que no olho 1. Da esquerda para a direita: rosto 1 + corte 7 + olho 3; rosto 2 + corte 8 + olho 3; rosto 3 + corte 9 + olho 3. Corte 7: cacheado curto em pequenos cachos volumosos; 8: médio com cachos/ondas em espiral; 9: afro grande arredondado. Estrutura de três linhas: cabelo isolado frontal/levemente em três quartos, cabeça montada predominantemente frontal, padrão de rosto sem cabelo/olhos em três quartos. Rosto 1 é mais estreito/oval e de queixo menor; 2 tem contorno de mandíbula mais amplo; 3 é mais arredondado e largo. As bases femininas inferiores preservam um nariz pequeno integrado visualmente; ao contrário das bases masculinas dos exemplos, não mostram o mesmo bloco retangular de indicação nasal. O olhar é deslocado lateralmente ou para cima em parte das montagens; é pose visual, não evidência de outra variante de globo.

**Limites:** São três combinações selecionadas, não uma matriz exaustiva de todos os rostos, cabelos e olhos. O corte tem seu próprio número; 'cabeça feminina N' nesta prancha acompanha o rosto N, não necessariamente o corte N. Sem vistas posteriores, cortes internos, espessura de cabelo, soquetes, medidas ou rig; compatibilidade 3D permanece não testada. Cores/aberturas e proporções sofrem pequenas variações de renderização; não extrair medidas exatas nem presumir identidade de malha a partir do rótulo.


### 004. Cabeça & Rosto/Combinações de Cabeças/Combinações de Cabeças Femininas — Olhos, Rostos e Cabelos/olho (4) - exemplos femininos.png

**Papel:** Três combinações femininas com olho 4, rostos e cabelos selecionados

**Observado:** Íris azul escura, pupila preta e aro externo escuro; abertura maior e mais arredondada que no olho 1, ainda parcialmente coberta acima. Da esquerda para a direita: rosto 4 + corte 10 + olho 4; rosto 5 + corte 11 + olho 4; rosto 3 + corte 12 + olho 4. Corte 10: longo ondulado de um lado e lateral raspada; 11: curto com topo de cachos e desenhos claros na lateral raspada; 12: longo ondulado, dividido próximo ao centro. Estrutura de três linhas: cabelo isolado frontal/levemente em três quartos, cabeça montada predominantemente frontal, padrão de rosto sem cabelo/olhos em três quartos. Rosto 4 é estreito e comprido com queixo muito pontudo; 5 tem contorno triangular mais moderado; 3 é largo/arredondado. As bases femininas inferiores preservam um nariz pequeno integrado visualmente; ao contrário das bases masculinas dos exemplos, não mostram o mesmo bloco retangular de indicação nasal. O olhar é deslocado lateralmente ou para cima em parte das montagens; é pose visual, não evidência de outra variante de globo.

**Limites:** São três combinações selecionadas, não uma matriz exaustiva de todos os rostos, cabelos e olhos. O corte tem seu próprio número; 'cabeça feminina N' nesta prancha acompanha o rosto N, não necessariamente o corte N. Sem vistas posteriores, cortes internos, espessura de cabelo, soquetes, medidas ou rig; compatibilidade 3D permanece não testada. Cores/aberturas e proporções sofrem pequenas variações de renderização; não extrair medidas exatas nem presumir identidade de malha a partir do rótulo.


### 005. Cabeça & Rosto/Combinações de Cabeças/Combinações de Cabeças Femininas — Olhos, Rostos e Cabelos/olho (5) - exemplos femininos.png

**Papel:** Três combinações femininas com olho 5, rostos e cabelos selecionados

**Observado:** Íris castanho escura, abertura amendoada com cantos afunilados, borda inferior de pele fina contornando o globo e cobertura superior arqueada. Da esquerda para a direita: rosto 4 + corte 1 + olho 5; rosto 5 + corte 2 + olho 5; rosto 3 + corte 3 + olho 5. Retoma cortes 1/2/3: curto assimétrico, longo em camadas com franja e rabo lateral; muda os rostos 1/2 usados no olho 1 para 4/5. Estrutura de três linhas: cabelo isolado frontal/levemente em três quartos, cabeça montada predominantemente frontal, padrão de rosto sem cabelo/olhos em três quartos. Rosto 4 é estreito e comprido com queixo muito pontudo; 5 tem contorno triangular mais moderado; 3 é largo/arredondado. As bases femininas inferiores preservam um nariz pequeno integrado visualmente; ao contrário das bases masculinas dos exemplos, não mostram o mesmo bloco retangular de indicação nasal. O olhar é deslocado lateralmente ou para cima em parte das montagens; é pose visual, não evidência de outra variante de globo.

**Limites:** São três combinações selecionadas, não uma matriz exaustiva de todos os rostos, cabelos e olhos. O corte tem seu próprio número; 'cabeça feminina N' nesta prancha acompanha o rosto N, não necessariamente o corte N. Sem vistas posteriores, cortes internos, espessura de cabelo, soquetes, medidas ou rig; compatibilidade 3D permanece não testada. Cores/aberturas e proporções sofrem pequenas variações de renderização; não extrair medidas exatas nem presumir identidade de malha a partir do rótulo.


### 006. Cabeça & Rosto/Combinações de Cabeças/Combinações de Cabeças Femininas — Olhos, Rostos e Cabelos/olho (6) - exemplos femininos.png

**Papel:** Três combinações femininas com olho 6, rostos e cabelos selecionados

**Observado:** Íris bege/marrom muito clara, maior abertura quase circular; pálpebras retraídas expõem praticamente toda a íris, com esclera clara ao redor. Da esquerda para a direita: rosto 1 + corte 4 + olho 6; rosto 2 + corte 5 + olho 6; rosto 3 + corte 6 + olho 6. Retoma cortes 4/5/6: bob com franja, dois rabos baixos e médio dividido ao centro; usa rostos 1/2/3, distintos de 4/5/3 do olho 2. Estrutura de três linhas: cabelo isolado frontal/levemente em três quartos, cabeça montada predominantemente frontal, padrão de rosto sem cabelo/olhos em três quartos. Rosto 1 é mais estreito/oval e de queixo menor; 2 tem contorno de mandíbula mais amplo; 3 é mais arredondado e largo. As bases femininas inferiores preservam um nariz pequeno integrado visualmente; ao contrário das bases masculinas dos exemplos, não mostram o mesmo bloco retangular de indicação nasal. Olhos grandes/arregalados aparecem nas três montagens; as bases inferiores não trazem medidas nem marcação de encaixe especial equivalente à série masculina.

**Limites:** São três combinações selecionadas, não uma matriz exaustiva de todos os rostos, cabelos e olhos. O corte tem seu próprio número; 'cabeça feminina N' nesta prancha acompanha o rosto N, não necessariamente o corte N. Sem vistas posteriores, cortes internos, espessura de cabelo, soquetes, medidas ou rig; compatibilidade 3D permanece não testada. Cores/aberturas e proporções sofrem pequenas variações de renderização; não extrair medidas exatas nem presumir identidade de malha a partir do rótulo.


### 007. Cabeça & Rosto/Combinações de Cabeças/Combinações de Cabeças Femininas — Olhos, Rostos e Cabelos/olho (7) - exemplos femininos.png

**Papel:** Três combinações femininas com olho 7, rostos e cabelos selecionados

**Observado:** Íris azul piscina/ciano muito clara e pupila preta; abertura grande quase circular como no 6, com olheira arroxeada sob o olho. Da esquerda para a direita: rosto 4 + corte 7 + olho 7; rosto 5 + corte 8 + olho 7; rosto 3 + corte 9 + olho 7. Retoma cortes 7/8/9: cacheado curto, cachos em espiral médios e afro grande; usa rostos 4/5/3, distintos de 1/2/3 do olho 3. Estrutura de três linhas: cabelo isolado frontal/levemente em três quartos, cabeça montada predominantemente frontal, padrão de rosto sem cabelo/olhos em três quartos. Rosto 4 é estreito e comprido com queixo muito pontudo; 5 tem contorno triangular mais moderado; 3 é largo/arredondado. As bases femininas inferiores preservam um nariz pequeno integrado visualmente; ao contrário das bases masculinas dos exemplos, não mostram o mesmo bloco retangular de indicação nasal. Olhos grandes/arregalados aparecem nas três montagens; as bases inferiores não trazem medidas nem marcação de encaixe especial equivalente à série masculina.

**Limites:** São três combinações selecionadas, não uma matriz exaustiva de todos os rostos, cabelos e olhos. O corte tem seu próprio número; 'cabeça feminina N' nesta prancha acompanha o rosto N, não necessariamente o corte N. Sem vistas posteriores, cortes internos, espessura de cabelo, soquetes, medidas ou rig; compatibilidade 3D permanece não testada. Cores/aberturas e proporções sofrem pequenas variações de renderização; não extrair medidas exatas nem presumir identidade de malha a partir do rótulo.


### 008. Cabeça & Rosto/Combinações de Cabeças/Combinações de Cabeças Femininas — Olhos, Rostos e Cabelos/olho (8) - exemplos femininos.png

**Papel:** Três combinações femininas com olho 8, rostos e cabelos selecionados

**Observado:** Íris azul clara/gelo com aro azul acinzentado; pálpebra superior baixa e abertura semicerrada como no 1. Olheiras roxas escuras e acentuadas. Da esquerda para a direita: rosto 1 + corte 10 + olho 8; rosto 2 + corte 11 + olho 8; rosto 3 + corte 12 + olho 8. Retoma cortes 10/11/12: lateral raspada com longo assimétrico, curto com desenhos laterais e longo ondulado; usa rostos 1/2/3, distintos de 4/5/3 do olho 4. Estrutura de três linhas: cabelo isolado frontal/levemente em três quartos, cabeça montada predominantemente frontal, padrão de rosto sem cabelo/olhos em três quartos. Rosto 1 é mais estreito/oval e de queixo menor; 2 tem contorno de mandíbula mais amplo; 3 é mais arredondado e largo. As bases femininas inferiores preservam um nariz pequeno integrado visualmente; ao contrário das bases masculinas dos exemplos, não mostram o mesmo bloco retangular de indicação nasal. O olhar é deslocado lateralmente ou para cima em parte das montagens; é pose visual, não evidência de outra variante de globo.

**Limites:** São três combinações selecionadas, não uma matriz exaustiva de todos os rostos, cabelos e olhos. O corte tem seu próprio número; 'cabeça feminina N' nesta prancha acompanha o rosto N, não necessariamente o corte N. Sem vistas posteriores, cortes internos, espessura de cabelo, soquetes, medidas ou rig; compatibilidade 3D permanece não testada. Cores/aberturas e proporções sofrem pequenas variações de renderização; não extrair medidas exatas nem presumir identidade de malha a partir do rótulo.


### 009. Cabeça & Rosto/Combinações de Cabeças/Combinações de Cabeças Masculinas Olhos,Rostos e Cabelos/Combinação 1.png

**Papel:** Prancha masculina olho1 com cabelos1/2/3 e rostos1/2/3

**Observado:** Correspondências: olho1+cabelo1+rosto1; olho1+cabelo2+rosto2; olho1+cabelo3+rosto3. Cabelo1 BAGUNÇADO1: mechas largas assimétricas inclinadas lateralmente; cabelo2 BAGUNÇADO2: mechas mais radiais e franja serrilhada; cabelo3 HI FADE: topo curto texturizado e laterais baixas em degradê. Olho1 tem abertura semicerrada, íris castanha e aspecto cansado/desconfiado; sobrancelhas grossas anguladas aparecem separadas acima. Módulos superiores são cascas de cabelo com região interna inferior escura; bases inferiores exibem órbitas vazias e bloco nasal claro. Geometria de cabelos muda claramente, cor permanece castanha.

**Limites:** Olho1 não está isolado nesta prancha; não define fronteira entre globo/pálpebras/sobrancelhas/pele. Base e montagem têm vistas diferentes. As cascas não mostram traseira/perfil completo nem interior mensurável. Não comprova cabelo imóvel ao trocar bases.


### 010. Cabeça & Rosto/Combinações de Cabeças/Combinações de Cabeças Masculinas Olhos,Rostos e Cabelos/Combinação 2.png

**Papel:** Prancha masculina olho1 com cabelos3/4/5 e rostos3/4/5

**Observado:** Correspondências: olho1+cabelo3+rosto3; olho1+cabelo4+rosto4; olho1+cabelo5+rosto5. Cabelo3 HI FADE reaparece; cabelo4 CARECA é explicitamente descrito SEM CABELO / NENHUM MÓDULO. Cabelo5 MOICANO: faixa central de pontas altas; imagem isolada mostra também casca lateral escura, enquanto montagem mostra laterais de pele aparente. É preciso decidir o que integra o módulo final. Olhos1 semicerrados/castanhos permanecem; bases rotuladas3/4/5 mudam contorno inferior. Barba, boca, orelhas e pescoço são contexto presente.

**Limites:** Careca deve poder ser ausência de cabelo no catálogo, não exigir geometria fictícia. Diferença visual entre casca isolada do moicano e lateral exposta na montagem precisa ser resolvida ao construir. Sem vista traseira/perfil, medidas ou encaixe comprovado.


### 011. Cabeça & Rosto/Combinações de Cabeças/Combinações de Cabeças Masculinas Olhos,Rostos e Cabelos/Combinação 3.png

**Papel:** Prancha masculina olho2 com cabelos6/7/8 e rostos1/2/3

**Observado:** Correspondências: olho2+cabelo6+rosto1; olho2+cabelo7+rosto2; olho2+cabelo8+rosto3. Olho2 é rotulado íris verde-clara e olheiras; abertura semicerrada semelhante à família olho1, com pigmentação/sombra periocular mais evidente. Cabelo6 PUNK ESPETADO: vários espigões grandes ao redor do topo; cabelo7 RAZOR PART: topo penteado lateralmente e linha clara de risca raspada; cabelo8 COQUE SAMURAI: cabelo puxado para trás e coque alto com elástico escuro. Mudanças de cabelos envolvem geometria; verde da íris, olheiras e linha de couro cabeludo podem exigir material/parametrização próprios, sem obrigar novo volume para cada cor.

**Limites:** Não há olho2 isolado ou vista de perfil para separar volume de olheira de pigmentação. A risca raspada deve preservar correspondência de cor com a pele; imagem não define se é recorte, decal ou malha. Cascas e cabeça montada são renders, não demonstram interface de encaixe nem comprimentos físicos.


### 012. Cabeça & Rosto/Combinações de Cabeças/Combinações de Cabeças Masculinas Olhos,Rostos e Cabelos/Combinação 4.png

**Papel:** Prancha masculina olho7 com cabelos8/9/10 e rostos4/5/6

**Observado:** Correspondências: olho7+cabelo8+rosto4; olho7+cabelo9+rosto5; olho7+cabelo10+rosto6. Olho7 é visivelmente mais aberto e arredondado que olhos1/2, íris azul-clara/azul-piscina e olheiras arroxeadas marcadas; existe mudança de forma, não somente cor. Cabelo8 coque samurai reaparece; cabelo9 BLACK POWER tem massa arredondada de cachos em volumes facetados; cabelo10 CHAVOSO tem topo curto crespo, laterais baixas e desenhos raspados claros. Bases inferiores são rotuladas ENCAIXE OLHO7, mas mostram órbitas vazias parecidas com outras pranchas; rosto6 aparece amplo/quadrangular. Desenhos raspados/pigmentação de íris/olheiras são aspectos de material ou superfície a separar da definição de forma.

**Limites:** Rótulo ENCAIXE OLHO7 não comprova que um encaixe exclusivo seja necessário nem que seja universal; precisa testar olho7 nos mesmos sockets dos outros. Sem vistas internas, perfil ou medida de volume de globo/pálpebra. Não prometer todos os olhos em todas as bases sem protótipo.


### 013. Cabeça & Rosto/Combinações de Cabeças/Combinações de Cabeças Masculinas Olhos,Rostos e Cabelos/Combinação 5.png

**Papel:** Prancha masculina olho5 com cabelo11/12/12 e rostos1/2/3

**Observado:** Título e colunas repetem cabelos11,12e12. Correspondências: olho5+cabelo11+rosto1; olho5+cabelo12+rosto2; olho5+cabelo12+rosto3. Não existe cabelo13 nesta prancha. Olho5 é rotulado amendoado, com abertura alongada lateralmente e íris muito escura/grande; forma difere dos redondos olho7. Cabelo11 DE RAUL: topo penteado para trás com mechas largas e linha frontal detalhada; cabelo12 REFLEXO DE CRIA: topo de cachos curtos com pontas claras/loiras contrastando com base escura e laterais baixas. A repetição do cabelo12 mostra intenção explícita de reutilizar o mesmo corte sobre dois rostos. Coloração clara nas pontas é material/cor; cachos e silhueta são geometria.

**Limites:** Reutilização é intenção visual; não comprova mesmo tamanho/transform na geometria3D. Nenhum módulo de olho isolado; limite do módulo ocular continua indefinido. Sem traseira/perfil dos cortes; detalhes de pigmentação não devem ser confundidos automaticamente com novas peças geométricas.


### 014. Cabeça & Rosto/Narizes — Módulos e Combinações/Combinacao feminina rostos e narizes/Narizes 1, 2 e 3.png

**Papel:** Prancha feminina de correspondência: narizes1/2/3, rostos1/2/3, cabelo1

**Observado:** Três colunas: nariz1→cabeça feminina1→padrão rosto1; nariz2→cabeça feminina2→padrão rosto2; nariz3→cabeça feminina3→padrão rosto3. Todas montagens indicam corte1. Linha superior mostra módulos isolados frontais; central apresenta montagem frontal com cabelo curto castanho assimétrico, olhos, sobrancelhas, nariz, boca, orelhas e pescoço. Bases inferiores em três quartos possuem cavidades oculares, sobrancelhas, pequeno relevo nasal, boca e pescoço; não são bases faciais lisas. Rosto1 afunila até queixo pequeno; rosto2 tem região inferior mais ampla/angular; rosto3 tem bochechas e contorno inferior arredondados. Nariz2 se destaca pela ponta gorda.

**Limites:** A prancha demonstra três associações, não todas9combinações possíveis de três rostos e três narizes. Montagens são imagens; não comprovam reutilização da mesma malha/mesmo transform, fusão, espessura ou compatibilidade automática. Nose isolado é frontal e base é três quartos; não há perfil/traseira para verificar profundidade. Aparência de cor/material é comum, variações relevantes são formas.


### 015. Cabeça & Rosto/Narizes — Módulos e Combinações/Combinacao feminina rostos e narizes/Narizes 4, 5 e 6 - Rostos 4, 5 e 6 - Cabelos 6, 8 e 9.png

**Papel:** Prancha feminina: narizes4/5/6 com cabelos6/8/9 e rostos rotulados4/5/6

**Observado:** Coluna1: rosto4+nariz4+corte6; cabelo liso castanho médio, risca central e pontas perto do pescoço. Coluna2: rosto5+nariz5+corte8; cabelo castanho cacheado/ondulado de cachos largos, risca central e volume lateral. Coluna3: rosto6+nariz6+corte9; cabelo castanho crespo muito volumoso/arredondado, composto de pequenos cachos. A base inferior chamada rosto6 parece reutilizar o contorno arredondado apresentado como rosto3 na prancha feminina equivalente com corte1. Sem confirmação suficiente para declarar nova base6 distinta. Narizes superiores repetem as mesmas seis-variantes correspondentes4/5/6; diferença de cabelos é geométrica, sem paleta nova.

**Limites:** Conflito de identificação rosto3/rosto6 exige decisão de catálogo; não gerar uma sexta base apenas porque este rótulo existe. Sem módulos de cabelo isolados nesta prancha, perfil, traseira, vista interna de encaixe ou medidas. Presença de olhos/boca/orelhas/pescoço é contexto de montagem, não autorização automática de escopo.


### 016. Cabeça & Rosto/Narizes — Módulos e Combinações/Combinacao feminina rostos e narizes/Narizes 4, 5 e 6.png

**Papel:** Prancha feminina de correspondência: narizes4/5/6 com cabelo1

**Observado:** Rótulos correspondem a nariz4+cabeça/rosto feminino4+corte1; nariz5+cabeça/rosto feminino5+corte1; nariz6+cabeça/rosto feminino3+corte1. Rosto4 é longo e estreito, queixo pontudo; rosto5 tem bochechas relativamente largas e queixo estreito; terceira base é mais arredondada. Montagens frontais mostram nasal4 longo estreito; nasal5 de ponta mais baixa; nasal6 largo e muito saliente visualmente. Cabelo castanho assimétrico permanece a referência de corte1. Bases inferiores têm cavidades oculares, sobrancelhas, boca, pescoço e algum relevo nasal; não fornecem interface modular vazia.

**Limites:** Terceira coluna é ROSTO3, não rosto6. Conflita com numeração de outra prancha feminina de narizes4/5/6 com cabelos6/8/9. Somente três associações; proporções e continuidade de pele devem ser validadas no3D. Sem perfil/traseira ou métricas.


### 017. Cabeça & Rosto/Narizes — Módulos e Combinações/Combinacao masculina rostos e narizes/Narizes 1, 2 e 3.png

**Papel:** Prancha masculina: narizes1/2/3, rostos1/2/3, cabelo1

**Observado:** Colunas: rosto masculino1+nariz1+corte1; rosto2+nariz2+corte1; rosto3+nariz3+corte1. Cabeças montadas frontais, bases em três quartos. Cabelo1 castanho curto bagunçado, mechas grandes facetadas; barba/bigode escuros, sobrancelhas, orelhas, boca e pescoço aparecem. Nariz2 tem ponta e asas mais largas; nariz3 é mais compacto. Rosto2 inferior mais estreito; rosto3 aparenta maior largura mandibular e bochechas. Bases inferiores têm órbitas vazias e bloco nasal claro/truncado: a posição do nariz é indicada visualmente, mas não há especificação técnica da borda.

**Limites:** Três correspondências específicas, sem prova de aplicação cruzada a todos os rostos. Seis narizes são apresentados como mesmos módulos usados no feminino, mas imagem não comprova escala/transform idênticos entre bases masculinas e femininas. Barba/sombras fazem parte da aparência; não é possível classificar definitivamente textura versus geometria a partir do render.


### 018. Cabeça & Rosto/Narizes — Módulos e Combinações/Combinacao masculina rostos e narizes/Narizes 4, 5 e 6.png

**Papel:** Prancha masculina: narizes4/5/6, rostos4/5/6, cabelo1

**Observado:** Colunas: rosto masculino4+nariz4+corte1; rosto5+nariz5+corte1; rosto6+nariz6+corte1. Rótulos masculinos incluem explicitamente rosto6. Rosto4 tem região inferior larga/arredondada; rosto5 estreita até queixo; rosto6 é amplo e mais quadrangular. Nariz6 cobre grande região central da face. O mesmo tipo de corte1, barba e olhos semicerrados é exibido; nariz4 fino longo, nariz5 ponta alongada, nariz6 muito largo. Bases inferiores repetem órbitas vazias e bloco claro nasal, com sobrancelhas/barba/orelhas/boca/pescoço presentes.

**Limites:** Diferenças de narizes são geométricas pretendidas; escala comum e relação nariz/face não têm medidas. Sem perfil/traseira ou borda de encaixe; a barba pode esconder partes da transição mandíbula/pele e não deve ser incorporada automaticamente ao escopo.


### 019. Cabeça & Rosto/Narizes — Módulos e Combinações/narizes/nariz 1.png

**Papel:** Referência isolada de nariz 1

**Observado:** Rótulo ORIGINAL; nariz alaranjado com facetas, ponte de largura intermediária, raiz superior plana/quadrangular e ponta arredondada. Asas laterais moderadas; região inferior e narinas aparecem escuras. Diferença de desenho principalmente geométrica, sem variante de cor demonstrada.

**Limites:** Somente vista frontal renderizada, sem medidas, perfil, traseira do módulo ou geometria da interface com o rosto; grade de fundo não fornece escala comprovada. Não comprova posição de encaixe nem profundidade/projeção da ponta.


### 020. Cabeça & Rosto/Narizes — Módulos e Combinações/narizes/nariz 2.png

**Papel:** Referência isolada de nariz 2

**Observado:** Rótulo GORDINHO E PROTUBERANTE; ponta grande e globosa, asas largas e arredondadas, volume inferior muito mais largo que a ponte. Superfície alaranjada facetada como nariz1; a mudança visível é de silhueta e volume aparente, não de paleta.

**Limites:** Somente vista frontal renderizada, sem medidas, perfil, traseira do módulo ou geometria da interface com o rosto; grade de fundo não fornece escala comprovada. Protuberância é uma intenção escrita; sua medida em profundidade não é determinada pela vista frontal.


### 021. Cabeça & Rosto/Narizes — Módulos e Combinações/narizes/nariz 3.png

**Papel:** Referência isolada de nariz 3

**Observado:** Rótulo CURTO E FINO; ponta pequena arredondada, asas menores e silhueta global compacta. Mesma linguagem alaranjada facetada; aparenta ter menor altura e largura no quadro que nariz1.

**Limites:** Somente vista frontal renderizada, sem medidas, perfil, traseira do módulo ou geometria da interface com o rosto; grade de fundo não fornece escala comprovada. Enquadramentos independentes impedem converter diferença em pixels em medida física.


### 022. Cabeça & Rosto/Narizes — Módulos e Combinações/narizes/nariz 4.png

**Papel:** Referência isolada de nariz 4

**Observado:** Rótulo FINO, COMPRIDO E EMPINADO; ponte muito longa e estreita com expansão próxima às asas. Ponta pequena/angular e duas aberturas de narinas nitidamente visíveis na região inferior; material alaranjado comum.

**Limites:** Somente vista frontal renderizada, sem medidas, perfil, traseira do módulo ou geometria da interface com o rosto; grade de fundo não fornece escala comprovada. Empinamento e ângulo da ponta exigem perfil; não deduzir curva lateral somente pelo rótulo.


### 023. Cabeça & Rosto/Narizes — Módulos e Combinações/narizes/nariz 5.png

**Papel:** Referência isolada de nariz 5

**Observado:** Rótulo LONGO, FINO E COM CALOMBO; ponte longa com mudança visível de largura/facetas no trecho médio. Ponta inferior alongada/angular; asas discretas comparadas ao nariz6. Mesma cor de pele das demais referências.

**Limites:** Somente vista frontal renderizada, sem medidas, perfil, traseira do módulo ou geometria da interface com o rosto; grade de fundo não fornece escala comprovada. Calombo dorsal em perfil não é confirmado dimensionalmente pela projeção frontal; estimar como intenção, não como medida observada.


### 024. Cabeça & Rosto/Narizes — Módulos e Combinações/narizes/nariz 6.png

**Papel:** Referência isolada de nariz 6

**Observado:** Rótulo GRANDE, LARGO E ALONGADO; ponte larga, corpo longo e ponta volumosa alongada para baixo. Asas bem abertas e narinas escuras grandes; referência alaranjada facetada. Contorno inferior chega muito próximo da borda da imagem.

**Limites:** Somente vista frontal renderizada, sem medidas, perfil, traseira do módulo ou geometria da interface com o rosto; grade de fundo não fornece escala comprovada. Perfil e profundidade do módulo mais volumoso não documentados.


### 025. Cabeça & Rosto/Olhos/exemplos masculinos de olhos em diferentes cabelos/olho (1) - exemplos.png

**Papel:** Comparação de montagem masculina: olho 1, rosto 1 e três cabelos

**Observado:** Íris castanha, pupila preta circular e reflexo branco; esclera creme. Pálpebra superior grande cobre a parte alta da íris; abertura inferior arredondada e olhar semicerrado. Três colunas constantes: corte 1 Bagunçado 1, corte 2 Bagunçado 2 e corte 3 Hi Fade. Cada coluna mostra cabelo isolado no alto, cabeça montada frontal no meio e base sem cabelo/olhos em três quartos abaixo. Corte 1 tem mechas pontiagudas de direção lateral; 2 tem mechas radiais mais uniformes/franja; 3 tem topo curto facetado e transição lateral curta. As três montagens mantêm o rosto masculino 1 com barba e sobrancelhas espessas, aplicando a mesma variante ocular; são exemplos de troca de cabelo sobre uma base. A linha inferior repete a base 1 com cavidades oculares vazias e uma região frontal retangular no lugar de um nariz completo. Montagens mantêm as cores e abertura da variante documentada, sem novas peças oculares identificadas.

**Limites:** Somente três montagens no rosto 1; não demonstra o olho combinado a todos os rostos masculinos ou cabelos do catálogo. Cabelo isolado e base em três quartos não têm vistas traseiras/laterais completas, medidas ou pivôs. Cavidades e nariz simplificado ilustram separação de módulos; não são especificação de soquetes geométricos nem prova de ausência de interpenetração. A repetição aparente da base não prova que malhas/cavidades sejam idênticas.


### 026. Cabeça & Rosto/Olhos/exemplos masculinos de olhos em diferentes cabelos/olho (2) - exemplos.png

**Papel:** Comparação de montagem masculina: olho 2, rosto 1 e três cabelos

**Observado:** Íris verde clara com aro escuro e pupila preta; abertura semicerrada visualmente próxima ao olho 1. Mancha marrom/arroxeada ampla sob o olho. Três colunas constantes: corte 1 Bagunçado 1, corte 2 Bagunçado 2 e corte 3 Hi Fade. Cada coluna mostra cabelo isolado no alto, cabeça montada frontal no meio e base sem cabelo/olhos em três quartos abaixo. Corte 1 tem mechas pontiagudas de direção lateral; 2 tem mechas radiais mais uniformes/franja; 3 tem topo curto facetado e transição lateral curta. As três montagens mantêm o rosto masculino 1 com barba e sobrancelhas espessas, aplicando a mesma variante ocular; são exemplos de troca de cabelo sobre uma base. A linha inferior repete a base 1 com cavidades oculares vazias e uma região frontal retangular no lugar de um nariz completo. A olheira está presente nas cabeças montadas e não acompanha claramente a base vazia inferior; estado de material da pele deve fazer parte da montagem.

**Limites:** Somente três montagens no rosto 1; não demonstra o olho combinado a todos os rostos masculinos ou cabelos do catálogo. Cabelo isolado e base em três quartos não têm vistas traseiras/laterais completas, medidas ou pivôs. Cavidades e nariz simplificado ilustram separação de módulos; não são especificação de soquetes geométricos nem prova de ausência de interpenetração. A repetição aparente da base não prova que malhas/cavidades sejam idênticas.


### 027. Cabeça & Rosto/Olhos/exemplos masculinos de olhos em diferentes cabelos/olho (3) - exemplos.png

**Papel:** Comparação de montagem masculina: olho 3, rosto 1 e três cabelos

**Observado:** Íris quase preta com aro cinza muito escuro, pupila preta e reflexo branco; esclera mais rosada nas laterais. Mais íris exposta que no olho 1. Três colunas constantes: corte 1 Bagunçado 1, corte 2 Bagunçado 2 e corte 3 Hi Fade. Cada coluna mostra cabelo isolado no alto, cabeça montada frontal no meio e base sem cabelo/olhos em três quartos abaixo. Corte 1 tem mechas pontiagudas de direção lateral; 2 tem mechas radiais mais uniformes/franja; 3 tem topo curto facetado e transição lateral curta. As três montagens mantêm o rosto masculino 1 com barba e sobrancelhas espessas, aplicando a mesma variante ocular; são exemplos de troca de cabelo sobre uma base. A linha inferior repete a base 1 com cavidades oculares vazias e uma região frontal retangular no lugar de um nariz completo. Montagens mantêm as cores e abertura da variante documentada, sem novas peças oculares identificadas.

**Limites:** Somente três montagens no rosto 1; não demonstra o olho combinado a todos os rostos masculinos ou cabelos do catálogo. Cabelo isolado e base em três quartos não têm vistas traseiras/laterais completas, medidas ou pivôs. Cavidades e nariz simplificado ilustram separação de módulos; não são especificação de soquetes geométricos nem prova de ausência de interpenetração. A repetição aparente da base não prova que malhas/cavidades sejam idênticas.


### 028. Cabeça & Rosto/Olhos/exemplos masculinos de olhos em diferentes cabelos/olho (4) - exemplos.png

**Papel:** Comparação de montagem masculina: olho 4, rosto 1 e três cabelos

**Observado:** Íris azul escura, pupila preta e aro externo escuro; abertura maior e mais arredondada que no olho 1, ainda parcialmente coberta acima. Três colunas constantes: corte 1 Bagunçado 1, corte 2 Bagunçado 2 e corte 3 Hi Fade. Cada coluna mostra cabelo isolado no alto, cabeça montada frontal no meio e base sem cabelo/olhos em três quartos abaixo. Corte 1 tem mechas pontiagudas de direção lateral; 2 tem mechas radiais mais uniformes/franja; 3 tem topo curto facetado e transição lateral curta. As três montagens mantêm o rosto masculino 1 com barba e sobrancelhas espessas, aplicando a mesma variante ocular; são exemplos de troca de cabelo sobre uma base. A linha inferior repete a base 1 com cavidades oculares vazias e uma região frontal retangular no lugar de um nariz completo. Montagens mantêm as cores e abertura da variante documentada, sem novas peças oculares identificadas.

**Limites:** Somente três montagens no rosto 1; não demonstra o olho combinado a todos os rostos masculinos ou cabelos do catálogo. Cabelo isolado e base em três quartos não têm vistas traseiras/laterais completas, medidas ou pivôs. Cavidades e nariz simplificado ilustram separação de módulos; não são especificação de soquetes geométricos nem prova de ausência de interpenetração. A repetição aparente da base não prova que malhas/cavidades sejam idênticas.


### 029. Cabeça & Rosto/Olhos/exemplos masculinos de olhos em diferentes cabelos/olho (5) - exemplos.png

**Papel:** Comparação de montagem masculina: olho 5, rosto 1 e três cabelos

**Observado:** Íris castanho escura, abertura amendoada com cantos afunilados, borda inferior de pele fina contornando o globo e cobertura superior arqueada. Três colunas constantes: corte 1 Bagunçado 1, corte 2 Bagunçado 2 e corte 3 Hi Fade. Cada coluna mostra cabelo isolado no alto, cabeça montada frontal no meio e base sem cabelo/olhos em três quartos abaixo. Corte 1 tem mechas pontiagudas de direção lateral; 2 tem mechas radiais mais uniformes/franja; 3 tem topo curto facetado e transição lateral curta. As três montagens mantêm o rosto masculino 1 com barba e sobrancelhas espessas, aplicando a mesma variante ocular; são exemplos de troca de cabelo sobre uma base. A linha inferior repete a base 1 com cavidades oculares vazias e uma região frontal retangular no lugar de um nariz completo. Montagens mantêm as cores e abertura da variante documentada, sem novas peças oculares identificadas.

**Limites:** Somente três montagens no rosto 1; não demonstra o olho combinado a todos os rostos masculinos ou cabelos do catálogo. Cabelo isolado e base em três quartos não têm vistas traseiras/laterais completas, medidas ou pivôs. Cavidades e nariz simplificado ilustram separação de módulos; não são especificação de soquetes geométricos nem prova de ausência de interpenetração. A repetição aparente da base não prova que malhas/cavidades sejam idênticas.


### 030. Cabeça & Rosto/Olhos/exemplos masculinos de olhos em diferentes cabelos/olho (6) - exemplos.png

**Papel:** Comparação de montagem masculina: olho 6, rosto 1 e três cabelos

**Observado:** Íris bege/marrom muito clara, maior abertura quase circular; pálpebras retraídas expõem praticamente toda a íris, com esclera clara ao redor. Três colunas constantes: corte 1 Bagunçado 1, corte 2 Bagunçado 2 e corte 3 Hi Fade. Cada coluna mostra cabelo isolado no alto, cabeça montada frontal no meio e base sem cabelo/olhos em três quartos abaixo. Corte 1 tem mechas pontiagudas de direção lateral; 2 tem mechas radiais mais uniformes/franja; 3 tem topo curto facetado e transição lateral curta. As três montagens mantêm o rosto masculino 1 com barba e sobrancelhas espessas, aplicando a mesma variante ocular; são exemplos de troca de cabelo sobre uma base. A linha inferior recebe legenda ENCAIXE OLHO 6, coerente com necessidade de órbitas/afastamento próprios descrita na folha ocular. Montagens mantêm as cores e abertura da variante documentada, sem novas peças oculares identificadas.

**Limites:** Somente três montagens no rosto 1; não demonstra o olho combinado a todos os rostos masculinos ou cabelos do catálogo. Cabelo isolado e base em três quartos não têm vistas traseiras/laterais completas, medidas ou pivôs. Cavidades e nariz simplificado ilustram separação de módulos; não são especificação de soquetes geométricos nem prova de ausência de interpenetração. A base rotulada com encaixe especial não oferece medidas para reproduzir a mudança de afastamento.


### 031. Cabeça & Rosto/Olhos/exemplos masculinos de olhos em diferentes cabelos/olho (7) - exemplos.png

**Papel:** Comparação de montagem masculina: olho 7, rosto 1 e três cabelos

**Observado:** Íris azul piscina/ciano muito clara e pupila preta; abertura grande quase circular como no 6, com olheira arroxeada sob o olho. Três colunas constantes: corte 1 Bagunçado 1, corte 2 Bagunçado 2 e corte 3 Hi Fade. Cada coluna mostra cabelo isolado no alto, cabeça montada frontal no meio e base sem cabelo/olhos em três quartos abaixo. Corte 1 tem mechas pontiagudas de direção lateral; 2 tem mechas radiais mais uniformes/franja; 3 tem topo curto facetado e transição lateral curta. As três montagens mantêm o rosto masculino 1 com barba e sobrancelhas espessas, aplicando a mesma variante ocular; são exemplos de troca de cabelo sobre uma base. A linha inferior recebe legenda ENCAIXE OLHO 7, coerente com necessidade de órbitas/afastamento próprios descrita na folha ocular. A olheira está presente nas cabeças montadas e não acompanha claramente a base vazia inferior; estado de material da pele deve fazer parte da montagem.

**Limites:** Somente três montagens no rosto 1; não demonstra o olho combinado a todos os rostos masculinos ou cabelos do catálogo. Cabelo isolado e base em três quartos não têm vistas traseiras/laterais completas, medidas ou pivôs. Cavidades e nariz simplificado ilustram separação de módulos; não são especificação de soquetes geométricos nem prova de ausência de interpenetração. A base rotulada com encaixe especial não oferece medidas para reproduzir a mudança de afastamento.


### 032. Cabeça & Rosto/Olhos/exemplos masculinos de olhos em diferentes cabelos/olho (8) - exemplos.png

**Papel:** Comparação de montagem masculina: olho 8, rosto 1 e três cabelos

**Observado:** Íris azul clara/gelo com aro azul acinzentado; pálpebra superior baixa e abertura semicerrada como no 1. Olheiras roxas escuras e acentuadas. Três colunas constantes: corte 1 Bagunçado 1, corte 2 Bagunçado 2 e corte 3 Hi Fade. Cada coluna mostra cabelo isolado no alto, cabeça montada frontal no meio e base sem cabelo/olhos em três quartos abaixo. Corte 1 tem mechas pontiagudas de direção lateral; 2 tem mechas radiais mais uniformes/franja; 3 tem topo curto facetado e transição lateral curta. As três montagens mantêm o rosto masculino 1 com barba e sobrancelhas espessas, aplicando a mesma variante ocular; são exemplos de troca de cabelo sobre uma base. A linha inferior repete a base 1 com cavidades oculares vazias e uma região frontal retangular no lugar de um nariz completo. A olheira está presente nas cabeças montadas e não acompanha claramente a base vazia inferior; estado de material da pele deve fazer parte da montagem.

**Limites:** Somente três montagens no rosto 1; não demonstra o olho combinado a todos os rostos masculinos ou cabelos do catálogo. Cabelo isolado e base em três quartos não têm vistas traseiras/laterais completas, medidas ou pivôs. Cavidades e nariz simplificado ilustram separação de módulos; não são especificação de soquetes geométricos nem prova de ausência de interpenetração. A repetição aparente da base não prova que malhas/cavidades sejam idênticas.


### 033. Cabeça & Rosto/Olhos/Padrões de Olhos Femininos — Rosto 1 e Corte 1/olho (1) - marrom.png

**Papel:** Documentação do módulo ocular 1, aplicação feminina no rosto 1/corte 1

**Observado:** Íris castanha, pupila preta circular e reflexo branco; esclera creme. Pálpebra superior grande cobre a parte alta da íris; abertura inferior arredondada e olhar semicerrado. Forma de referência, contorno superior quase horizontal na montagem, curva inferior ampla; sem olheira roxa destacada. Prancha de quatro painéis: par ocular isolado; olho em frente, três quartos e perfil; detalhe ampliado dos olhos no rosto; cabeça frontal montada. Aplicação no rosto feminino 1 com corte assimétrico 1, sobrancelhas menos volumosas e ponta externa do contorno superior alongada. Os diagramas do módulo isolado e das três vistas repetem visualmente o desenho da variante masculina correspondente; isso evidencia intenção de catálogo ocular comum, não prova de identidade de arquivos 3D.

**Limites:** Referência raster ilustrativa, sem unidades, dimensões, profundidade do encaixe, pivô, topologia, UV, animação ou arquivo 3D verificável. Frente, três quartos e um perfil são desenhos sem calibração ortográfica; não garantem concordância geométrica exata entre vistas. Texto de intercambialidade descreve intenção visual; GLBs montáveis e compatibilidade com RCL/3DC precisam de validação própria. O rosto rotulado 1 varia levemente em nariz, sobrancelhas e proporções entre pranchas; os diagramas isolados não documentam os cílios/contornos alongados presentes na aplicação.


### 034. Cabeça & Rosto/Olhos/Padrões de Olhos Femininos — Rosto 1 e Corte 1/olho (2) - verde.png

**Papel:** Documentação do módulo ocular 2, aplicação feminina no rosto 1/corte 1

**Observado:** Íris verde clara com aro escuro e pupila preta; abertura semicerrada visualmente próxima ao olho 1. Mancha marrom/arroxeada ampla sob o olho. Variação majoritariamente de cor da íris e região periorbital sobre a forma base 1; as olheiras aparecem na pele, não no globo isolado. Prancha de quatro painéis: par ocular isolado; olho em frente, três quartos e perfil; detalhe ampliado dos olhos no rosto; cabeça frontal montada. A legenda feminina diz 'Mesma escala e posição do Olho 2', referência circular que não define medidas; a intenção de repetição da forma continua visualmente clara. Os diagramas do módulo isolado e das três vistas repetem visualmente o desenho da variante masculina correspondente; isso evidencia intenção de catálogo ocular comum, não prova de identidade de arquivos 3D.

**Limites:** Referência raster ilustrativa, sem unidades, dimensões, profundidade do encaixe, pivô, topologia, UV, animação ou arquivo 3D verificável. Frente, três quartos e um perfil são desenhos sem calibração ortográfica; não garantem concordância geométrica exata entre vistas. Texto de intercambialidade descreve intenção visual; GLBs montáveis e compatibilidade com RCL/3DC precisam de validação própria. O rosto rotulado 1 varia levemente em nariz, sobrancelhas e proporções entre pranchas; os diagramas isolados não documentam os cílios/contornos alongados presentes na aplicação. A olheira pertence visualmente à região de pele ao redor do olho; exportar só o globo como GLB não reproduz a variante completa.


### 035. Cabeça & Rosto/Olhos/Padrões de Olhos Femininos — Rosto 1 e Corte 1/olho (3) - preto.png

**Papel:** Documentação do módulo ocular 3, aplicação feminina no rosto 1/corte 1

**Observado:** Íris quase preta com aro cinza muito escuro, pupila preta e reflexo branco; esclera mais rosada nas laterais. Mais íris exposta que no olho 1. Abertura palpebral maior, globo declarado de mesmo volume; altera a configuração de pálpebras e a cor da esclera além da íris. Prancha de quatro painéis: par ocular isolado; olho em frente, três quartos e perfil; detalhe ampliado dos olhos no rosto; cabeça frontal montada. Rosto feminino 1 com íris grande escura; a aplicação muda levemente a direção do olhar, portanto direção da pupila não deve ser confundida com nova variante anatômica. Os diagramas do módulo isolado e das três vistas repetem visualmente o desenho da variante masculina correspondente; isso evidencia intenção de catálogo ocular comum, não prova de identidade de arquivos 3D.

**Limites:** Referência raster ilustrativa, sem unidades, dimensões, profundidade do encaixe, pivô, topologia, UV, animação ou arquivo 3D verificável. Frente, três quartos e um perfil são desenhos sem calibração ortográfica; não garantem concordância geométrica exata entre vistas. Texto de intercambialidade descreve intenção visual; GLBs montáveis e compatibilidade com RCL/3DC precisam de validação própria. O rosto rotulado 1 varia levemente em nariz, sobrancelhas e proporções entre pranchas; os diagramas isolados não documentam os cílios/contornos alongados presentes na aplicação.


### 036. Cabeça & Rosto/Olhos/Padrões de Olhos Femininos — Rosto 1 e Corte 1/olho (4) - azul.png

**Papel:** Documentação do módulo ocular 4, aplicação feminina no rosto 1/corte 1

**Observado:** Íris azul escura, pupila preta e aro externo escuro; abertura maior e mais arredondada que no olho 1, ainda parcialmente coberta acima. Variação de abertura palpebral e cor, não apenas material; família visual de olhos mais abertos próxima ao 3, sem comprovação de malha idêntica. Prancha de quatro painéis: par ocular isolado; olho em frente, três quartos e perfil; detalhe ampliado dos olhos no rosto; cabeça frontal montada. A vista feminina conserva os diagramas oculares do padrão masculino; aplicação tem contorno superior/cílios mais alongados lateralmente. Os diagramas do módulo isolado e das três vistas repetem visualmente o desenho da variante masculina correspondente; isso evidencia intenção de catálogo ocular comum, não prova de identidade de arquivos 3D.

**Limites:** Referência raster ilustrativa, sem unidades, dimensões, profundidade do encaixe, pivô, topologia, UV, animação ou arquivo 3D verificável. Frente, três quartos e um perfil são desenhos sem calibração ortográfica; não garantem concordância geométrica exata entre vistas. Texto de intercambialidade descreve intenção visual; GLBs montáveis e compatibilidade com RCL/3DC precisam de validação própria. O rosto rotulado 1 varia levemente em nariz, sobrancelhas e proporções entre pranchas; os diagramas isolados não documentam os cílios/contornos alongados presentes na aplicação.


### 037. Cabeça & Rosto/Olhos/Padrões de Olhos Femininos — Rosto 1 e Corte 1/olho (5) - marrom.png

**Papel:** Documentação do módulo ocular 5, aplicação feminina no rosto 1/corte 1

**Observado:** Íris castanho escura, abertura amendoada com cantos afunilados, borda inferior de pele fina contornando o globo e cobertura superior arqueada. Contorno palpebral novo, dobra epicântica indicada no canto interno e pálpebra pouco marcada; não é substituição de cor do olho 1. Prancha de quatro painéis: par ocular isolado; olho em frente, três quartos e perfil; detalhe ampliado dos olhos no rosto; cabeça frontal montada. A forma amendoada reaparece no rosto feminino; não há desenho exclusivo de globo feminino. Detalhe exibe canto interno pronunciado. Os diagramas do módulo isolado e das três vistas repetem visualmente o desenho da variante masculina correspondente; isso evidencia intenção de catálogo ocular comum, não prova de identidade de arquivos 3D.

**Limites:** Referência raster ilustrativa, sem unidades, dimensões, profundidade do encaixe, pivô, topologia, UV, animação ou arquivo 3D verificável. Frente, três quartos e um perfil são desenhos sem calibração ortográfica; não garantem concordância geométrica exata entre vistas. Texto de intercambialidade descreve intenção visual; GLBs montáveis e compatibilidade com RCL/3DC precisam de validação própria. O rosto rotulado 1 varia levemente em nariz, sobrancelhas e proporções entre pranchas; os diagramas isolados não documentam os cílios/contornos alongados presentes na aplicação.


### 038. Cabeça & Rosto/Olhos/Padrões de Olhos Femininos — Rosto 1 e Corte 1/olho (6) - marrom.png

**Papel:** Documentação do módulo ocular 6, aplicação feminina no rosto 1/corte 1

**Observado:** Íris bege/marrom muito clara, maior abertura quase circular; pálpebras retraídas expõem praticamente toda a íris, com esclera clara ao redor. Além da abertura, o par fica mais afastado. A folha indica afastamento simétrico e órbitas ajustadas; isso muda posicionamento e interface com o rosto. Prancha de quatro painéis: par ocular isolado; olho em frente, três quartos e perfil; detalhe ampliado dos olhos no rosto; cabeça frontal montada. Aplicação feminina tem contornos externos/cílios salientes, ausentes do diagrama isolado compartilhado. Afastamento e grande abertura constam da folha. Os diagramas do módulo isolado e das três vistas repetem visualmente o desenho da variante masculina correspondente; isso evidencia intenção de catálogo ocular comum, não prova de identidade de arquivos 3D.

**Limites:** Referência raster ilustrativa, sem unidades, dimensões, profundidade do encaixe, pivô, topologia, UV, animação ou arquivo 3D verificável. Frente, três quartos e um perfil são desenhos sem calibração ortográfica; não garantem concordância geométrica exata entre vistas. Texto de intercambialidade descreve intenção visual; GLBs montáveis e compatibilidade com RCL/3DC precisam de validação própria. O rosto rotulado 1 varia levemente em nariz, sobrancelhas e proporções entre pranchas; os diagramas isolados não documentam os cílios/contornos alongados presentes na aplicação. O maior afastamento e as órbitas ajustadas contradizem a suposição de que basta um encaixe fixo invariável para todas as oito variantes.


### 039. Cabeça & Rosto/Olhos/Padrões de Olhos Femininos — Rosto 1 e Corte 1/olho (7) - azul.png

**Papel:** Documentação do módulo ocular 7, aplicação feminina no rosto 1/corte 1

**Observado:** Íris azul piscina/ciano muito clara e pupila preta; abertura grande quase circular como no 6, com olheira arroxeada sob o olho. Combina a geometria visual e afastamento do 6 com nova íris e olheiras; exige material da pele e posicionamento, além do globo. Prancha de quatro painéis: par ocular isolado; olho em frente, três quartos e perfil; detalhe ampliado dos olhos no rosto; cabeça frontal montada. Grande abertura e olheira reaparecem no rosto feminino 1; ciano distingue esta variante do azul claro do 8, que é semicerrado. Os diagramas do módulo isolado e das três vistas repetem visualmente o desenho da variante masculina correspondente; isso evidencia intenção de catálogo ocular comum, não prova de identidade de arquivos 3D.

**Limites:** Referência raster ilustrativa, sem unidades, dimensões, profundidade do encaixe, pivô, topologia, UV, animação ou arquivo 3D verificável. Frente, três quartos e um perfil são desenhos sem calibração ortográfica; não garantem concordância geométrica exata entre vistas. Texto de intercambialidade descreve intenção visual; GLBs montáveis e compatibilidade com RCL/3DC precisam de validação própria. O rosto rotulado 1 varia levemente em nariz, sobrancelhas e proporções entre pranchas; os diagramas isolados não documentam os cílios/contornos alongados presentes na aplicação. A olheira pertence visualmente à região de pele ao redor do olho; exportar só o globo como GLB não reproduz a variante completa. O maior afastamento e as órbitas ajustadas contradizem a suposição de que basta um encaixe fixo invariável para todas as oito variantes.


### 040. Cabeça & Rosto/Olhos/Padrões de Olhos Femininos — Rosto 1 e Corte 1/olho (8) - azul.png

**Papel:** Documentação do módulo ocular 8, aplicação feminina no rosto 1/corte 1

**Observado:** Íris azul clara/gelo com aro azul acinzentado; pálpebra superior baixa e abertura semicerrada como no 1. Olheiras roxas escuras e acentuadas. Retorna explicitamente à escala/posição do 1 e à família semicerrada; diferenças principais são íris e mancha periorbital mais intensa. Prancha de quatro painéis: par ocular isolado; olho em frente, três quartos e perfil; detalhe ampliado dos olhos no rosto; cabeça frontal montada. Aplicação feminina transmite cansaço pelas olheiras e pálpebras; olhar azul claro difere da abertura grande/ciano do 7. Os diagramas do módulo isolado e das três vistas repetem visualmente o desenho da variante masculina correspondente; isso evidencia intenção de catálogo ocular comum, não prova de identidade de arquivos 3D.

**Limites:** Referência raster ilustrativa, sem unidades, dimensões, profundidade do encaixe, pivô, topologia, UV, animação ou arquivo 3D verificável. Frente, três quartos e um perfil são desenhos sem calibração ortográfica; não garantem concordância geométrica exata entre vistas. Texto de intercambialidade descreve intenção visual; GLBs montáveis e compatibilidade com RCL/3DC precisam de validação própria. O rosto rotulado 1 varia levemente em nariz, sobrancelhas e proporções entre pranchas; os diagramas isolados não documentam os cílios/contornos alongados presentes na aplicação. A olheira pertence visualmente à região de pele ao redor do olho; exportar só o globo como GLB não reproduz a variante completa.


### 041. Cabeça & Rosto/Olhos/Padrões de Olhos Masculino — Rosto 1 e Corte 1/olho (1) - marrom.png

**Papel:** Documentação do módulo ocular 1, aplicação masculina no rosto 1/corte 1

**Observado:** Íris castanha, pupila preta circular e reflexo branco; esclera creme. Pálpebra superior grande cobre a parte alta da íris; abertura inferior arredondada e olhar semicerrado. Forma de referência, contorno superior quase horizontal na montagem, curva inferior ampla; sem olheira roxa destacada. Prancha de quatro painéis: par ocular isolado; olho em frente, três quartos e perfil; detalhe ampliado dos olhos no rosto; cabeça frontal montada. A montagem frontal masculina mantém sobrancelhas espessas angulares, nariz largo e barba; a expressão de severidade também depende dessas peças. Estilo faceteado de baixa contagem visual de polígonos, com íris radial facetada, pupila circular preta e brilho branco.

**Limites:** Referência raster ilustrativa, sem unidades, dimensões, profundidade do encaixe, pivô, topologia, UV, animação ou arquivo 3D verificável. Frente, três quartos e um perfil são desenhos sem calibração ortográfica; não garantem concordância geométrica exata entre vistas. Texto de intercambialidade descreve intenção visual; GLBs montáveis e compatibilidade com RCL/3DC precisam de validação própria.


### 042. Cabeça & Rosto/Olhos/Padrões de Olhos Masculino — Rosto 1 e Corte 1/olho (2) - verde.png

**Papel:** Documentação do módulo ocular 2, aplicação masculina no rosto 1/corte 1

**Observado:** Íris verde clara com aro escuro e pupila preta; abertura semicerrada visualmente próxima ao olho 1. Mancha marrom/arroxeada ampla sob o olho. Variação majoritariamente de cor da íris e região periorbital sobre a forma base 1; as olheiras aparecem na pele, não no globo isolado. Prancha de quatro painéis: par ocular isolado; olho em frente, três quartos e perfil; detalhe ampliado dos olhos no rosto; cabeça frontal montada. A folha diz mesma escala e posição do Olho 1; o módulo isolado e as três vistas não incluem a olheira que aparece no rosto. Estilo faceteado de baixa contagem visual de polígonos, com íris radial facetada, pupila circular preta e brilho branco.

**Limites:** Referência raster ilustrativa, sem unidades, dimensões, profundidade do encaixe, pivô, topologia, UV, animação ou arquivo 3D verificável. Frente, três quartos e um perfil são desenhos sem calibração ortográfica; não garantem concordância geométrica exata entre vistas. Texto de intercambialidade descreve intenção visual; GLBs montáveis e compatibilidade com RCL/3DC precisam de validação própria. A olheira pertence visualmente à região de pele ao redor do olho; exportar só o globo como GLB não reproduz a variante completa.


### 043. Cabeça & Rosto/Olhos/Padrões de Olhos Masculino — Rosto 1 e Corte 1/olho (3) - preto.png

**Papel:** Documentação do módulo ocular 3, aplicação masculina no rosto 1/corte 1

**Observado:** Íris quase preta com aro cinza muito escuro, pupila preta e reflexo branco; esclera mais rosada nas laterais. Mais íris exposta que no olho 1. Abertura palpebral maior, globo declarado de mesmo volume; altera a configuração de pálpebras e a cor da esclera além da íris. Prancha de quatro painéis: par ocular isolado; olho em frente, três quartos e perfil; detalhe ampliado dos olhos no rosto; cabeça frontal montada. Detalhe frontal evidencia esclera levemente avermelhada e elevação da borda superior; montagem conserva a cabeça masculina 1. Estilo faceteado de baixa contagem visual de polígonos, com íris radial facetada, pupila circular preta e brilho branco.

**Limites:** Referência raster ilustrativa, sem unidades, dimensões, profundidade do encaixe, pivô, topologia, UV, animação ou arquivo 3D verificável. Frente, três quartos e um perfil são desenhos sem calibração ortográfica; não garantem concordância geométrica exata entre vistas. Texto de intercambialidade descreve intenção visual; GLBs montáveis e compatibilidade com RCL/3DC precisam de validação própria.


### 044. Cabeça & Rosto/Olhos/Padrões de Olhos Masculino — Rosto 1 e Corte 1/olho (4) - azul.png

**Papel:** Documentação do módulo ocular 4, aplicação masculina no rosto 1/corte 1

**Observado:** Íris azul escura, pupila preta e aro externo escuro; abertura maior e mais arredondada que no olho 1, ainda parcialmente coberta acima. Variação de abertura palpebral e cor, não apenas material; família visual de olhos mais abertos próxima ao 3, sem comprovação de malha idêntica. Prancha de quatro painéis: par ocular isolado; olho em frente, três quartos e perfil; detalhe ampliado dos olhos no rosto; cabeça frontal montada. Legenda indica mesmo globo ocular e pálpebras mais abertas; detalhe e montagem mostram ampla esclera sob a íris. Estilo faceteado de baixa contagem visual de polígonos, com íris radial facetada, pupila circular preta e brilho branco.

**Limites:** Referência raster ilustrativa, sem unidades, dimensões, profundidade do encaixe, pivô, topologia, UV, animação ou arquivo 3D verificável. Frente, três quartos e um perfil são desenhos sem calibração ortográfica; não garantem concordância geométrica exata entre vistas. Texto de intercambialidade descreve intenção visual; GLBs montáveis e compatibilidade com RCL/3DC precisam de validação própria.


### 045. Cabeça & Rosto/Olhos/Padrões de Olhos Masculino — Rosto 1 e Corte 1/olho (5) - marrom.png

**Papel:** Documentação do módulo ocular 5, aplicação masculina no rosto 1/corte 1

**Observado:** Íris castanho escura, abertura amendoada com cantos afunilados, borda inferior de pele fina contornando o globo e cobertura superior arqueada. Contorno palpebral novo, dobra epicântica indicada no canto interno e pálpebra pouco marcada; não é substituição de cor do olho 1. Prancha de quatro painéis: par ocular isolado; olho em frente, três quartos e perfil; detalhe ampliado dos olhos no rosto; cabeça frontal montada. A forma amendoada aparece tanto no módulo isolado como na montagem masculina; a folha declara conservar o globo ocular. Estilo faceteado de baixa contagem visual de polígonos, com íris radial facetada, pupila circular preta e brilho branco.

**Limites:** Referência raster ilustrativa, sem unidades, dimensões, profundidade do encaixe, pivô, topologia, UV, animação ou arquivo 3D verificável. Frente, três quartos e um perfil são desenhos sem calibração ortográfica; não garantem concordância geométrica exata entre vistas. Texto de intercambialidade descreve intenção visual; GLBs montáveis e compatibilidade com RCL/3DC precisam de validação própria.


### 046. Cabeça & Rosto/Olhos/Padrões de Olhos Masculino — Rosto 1 e Corte 1/olho (6) - marrom.png

**Papel:** Documentação do módulo ocular 6, aplicação masculina no rosto 1/corte 1

**Observado:** Íris bege/marrom muito clara, maior abertura quase circular; pálpebras retraídas expõem praticamente toda a íris, com esclera clara ao redor. Além da abertura, o par fica mais afastado. A folha indica afastamento simétrico e órbitas ajustadas; isso muda posicionamento e interface com o rosto. Prancha de quatro painéis: par ocular isolado; olho em frente, três quartos e perfil; detalhe ampliado dos olhos no rosto; cabeça frontal montada. Módulo isolado tem menos cobertura superior e aro inferior fino; cabeça frontal parece mais arregalada. Legenda de perfil mostra grande exposição anterior da íris. Estilo faceteado de baixa contagem visual de polígonos, com íris radial facetada, pupila circular preta e brilho branco.

**Limites:** Referência raster ilustrativa, sem unidades, dimensões, profundidade do encaixe, pivô, topologia, UV, animação ou arquivo 3D verificável. Frente, três quartos e um perfil são desenhos sem calibração ortográfica; não garantem concordância geométrica exata entre vistas. Texto de intercambialidade descreve intenção visual; GLBs montáveis e compatibilidade com RCL/3DC precisam de validação própria. O maior afastamento e as órbitas ajustadas contradizem a suposição de que basta um encaixe fixo invariável para todas as oito variantes.


### 047. Cabeça & Rosto/Olhos/Padrões de Olhos Masculino — Rosto 1 e Corte 1/olho (7) - azul.png

**Papel:** Documentação do módulo ocular 7, aplicação masculina no rosto 1/corte 1

**Observado:** Íris azul piscina/ciano muito clara e pupila preta; abertura grande quase circular como no 6, com olheira arroxeada sob o olho. Combina a geometria visual e afastamento do 6 com nova íris e olheiras; exige material da pele e posicionamento, além do globo. Prancha de quatro painéis: par ocular isolado; olho em frente, três quartos e perfil; detalhe ampliado dos olhos no rosto; cabeça frontal montada. Setas apontam olhos mais afastados e olheira integrada à pele; a legenda da aplicação declara órbitas ajustadas ao novo afastamento. Estilo faceteado de baixa contagem visual de polígonos, com íris radial facetada, pupila circular preta e brilho branco.

**Limites:** Referência raster ilustrativa, sem unidades, dimensões, profundidade do encaixe, pivô, topologia, UV, animação ou arquivo 3D verificável. Frente, três quartos e um perfil são desenhos sem calibração ortográfica; não garantem concordância geométrica exata entre vistas. Texto de intercambialidade descreve intenção visual; GLBs montáveis e compatibilidade com RCL/3DC precisam de validação própria. A olheira pertence visualmente à região de pele ao redor do olho; exportar só o globo como GLB não reproduz a variante completa. O maior afastamento e as órbitas ajustadas contradizem a suposição de que basta um encaixe fixo invariável para todas as oito variantes.


### 048. Cabeça & Rosto/Olhos/Padrões de Olhos Masculino — Rosto 1 e Corte 1/olho (8) - azul.png

**Papel:** Documentação do módulo ocular 8, aplicação masculina no rosto 1/corte 1

**Observado:** Íris azul clara/gelo com aro azul acinzentado; pálpebra superior baixa e abertura semicerrada como no 1. Olheiras roxas escuras e acentuadas. Retorna explicitamente à escala/posição do 1 e à família semicerrada; diferenças principais são íris e mancha periorbital mais intensa. Prancha de quatro painéis: par ocular isolado; olho em frente, três quartos e perfil; detalhe ampliado dos olhos no rosto; cabeça frontal montada. As olheiras escuras ocupam região sob a borda inferior, com transição para a pele; não estão presentes no módulo isolado. Estilo faceteado de baixa contagem visual de polígonos, com íris radial facetada, pupila circular preta e brilho branco.

**Limites:** Referência raster ilustrativa, sem unidades, dimensões, profundidade do encaixe, pivô, topologia, UV, animação ou arquivo 3D verificável. Frente, três quartos e um perfil são desenhos sem calibração ortográfica; não garantem concordância geométrica exata entre vistas. Texto de intercambialidade descreve intenção visual; GLBs montáveis e compatibilidade com RCL/3DC precisam de validação própria. A olheira pertence visualmente à região de pele ao redor do olho; exportar só o globo como GLB não reproduz a variante completa.


### 049. Cabeça & Rosto/Rosto Geral/Rosto Geral Feminino.jpeg

**Papel:** Referência geral feminina montada e explodida

**Observado:** Inspeção direta: 1536 × 1024. Cabeça com cabelo castanho assimétrico em mechas largas, franja longa à esquerda da imagem e nuca curta; rosto afunila suavemente até o queixo, olhos semicerrados e boca de cantos baixos. Mostra frente, perfil voltado à direita da imagem, costas e uma vista em três quartos rotulada 'perfil esquerdo'. Embaixo, cabelo, dois olhos, nariz e duas orelhas são desenhados afastados da base. A base mantém sobrancelhas, boca, pescoço, órbitas vazias e um pequeno relevo nasal. Não há apêndice auricular evidente nessa base. É visualmente compatível com a família feminina 1.

**Limites:** O painel 'perfil esquerdo' não é um perfil estritamente lateral: ambos os olhos continuam visíveis. O conjunto não fornece dois perfis ortogonais femininos confiáveis. A legenda diz nariz removido, mas há nariz/relevo nasal visível na base; a peça nasal explodida também parece proporcionalmente maior que o pequeno nariz da montagem. É uma ambiguidade visual, sem medida para resolver. A base não é neutra: sobrancelhas inclinadas e boca desenham expressão. Nenhuma vista mostra superfície interna do cabelo, recortes de encaixe ou base por trás.


### 050. Cabeça & Rosto/Rosto Geral/Rosto Geral Masculino.jpeg

**Papel:** Referência geral masculina montada e explodida

**Observado:** Inspeção direta: 1536 × 1024. Frente, dois perfis laterais e costas da cabeça montada; decomposição e base em três quartos. O nariz, a orelha e a projeção do queixo são legíveis nos perfis. Cabelo castanho curto em mechas pontudas, olhos semicerrados com sobrancelhas grossas, barba e pescoço. A mandíbula é relativamente mais estreita/afunilada do que na prancha Padrao de mudanca de Rosto. A base em três quartos é visualmente compatível com a pequena referência base masculina 1. Permanecem sobrancelhas, boca, barba e pescoço; há bloco nasal e uma saliência lateral achatada.

**Limites:** A numeração e as setas descrevem uma intenção de separação; não demonstram arquivos de malha separados ou compatibilidade dos encaixes. O título 'base sem componentes' é relativo: a legenda explicitamente mantém sobrancelhas, boca e barba, e o desenho ainda contém formas no local do nariz e da orelha. As quatro vistas são da cabeça já montada, não de cada base facial 2–6; não devem ser atribuídas automaticamente a todas as variantes.


### 051. Cabeça & Rosto/Tipo de Corte de cabelo/Padrao de mudanca de cabelo.jpeg

**Papel:** Regra visual de troca e vistas complementares

**Observado:** Prancha de troca de cabelo masculina: cabeça montada com Corte2 em frente, perfil direito, costas e perfil esquerdo; Corte1 e Corte2 isolados em vista explodida. Diferencia topete assimétrico1 de franja radial2. Texto mantém olhos/nariz/orelhas/barba na cabeça neste experimento; isso descreve teste de troca, não prova que essas regiões devam ser uma única malha final.

**Limites:** Quatro vistas aplicam-se à cabeça e corte2 ilustrados; não comprovam todas as outras bases ou cortes. Desenho2D não garante equivalência geométrica entre vistas.


### 052. Cabeça & Rosto/Tipo de Corte de cabelo/Tipos cortes/Feminino/Corte feminino 1 - Corte 1.jpeg

**Papel:** Referência de módulo de cabelo isolado

**Observado:** Corte feminino1: cabelo castanho curto, assimétrico, volumoso, franja diagonal longa e grandes mechas pontudas; abertura inferior demonstra peça independente.

**Limites:** Arquivo isolado oferece predominantemente uma vista em três quartos/frontal, sem medidas físicas ou superfície interna definida. Requer cruzamento com montagens e checagem3D; fundo e grade não são textura do modelo.


### 053. Cabeça & Rosto/Tipo de Corte de cabelo/Tipos cortes/Feminino/Corte feminino 2 - Corte 2.jpeg

**Papel:** Referência de módulo de cabelo isolado

**Observado:** Corte feminino2: longo castanho em camadas com franja frontal densa e pontas alongadas nas laterais; extensão inferior já pede considerar pescoço/ombros futuros.

**Limites:** Arquivo isolado oferece predominantemente uma vista em três quartos/frontal, sem medidas físicas ou superfície interna definida. Requer cruzamento com montagens e checagem3D; fundo e grade não são textura do modelo.


### 054. Cabeça & Rosto/Tipo de Corte de cabelo/Tipos cortes/Feminino/Corte feminino 3 - Corte 3.jpeg

**Papel:** Referência de módulo de cabelo isolado

**Observado:** Corte feminino3: franja e fios compridos na frente, cabelo preso em rabo baixo lateral à direita da imagem; assimetria precisa ser preservada no espaço3D.

**Limites:** Arquivo isolado oferece predominantemente uma vista em três quartos/frontal, sem medidas físicas ou superfície interna definida. Requer cruzamento com montagens e checagem3D; fundo e grade não são textura do modelo.


### 055. Cabeça & Rosto/Tipo de Corte de cabelo/Tipos cortes/Feminino/Corte feminino 4 - Corte 4.jpeg

**Papel:** Referência de módulo de cabelo isolado

**Observado:** Corte feminino4: chanel curto arredondado, franja reta quase horizontal, pontas das laterais em direção ao queixo.

**Limites:** Arquivo isolado oferece predominantemente uma vista em três quartos/frontal, sem medidas físicas ou superfície interna definida. Requer cruzamento com montagens e checagem3D; fundo e grade não são textura do modelo.


### 056. Cabeça & Rosto/Tipo de Corte de cabelo/Tipos cortes/Feminino/Corte feminino 5 - Corte 5.jpeg

**Papel:** Referência de módulo de cabelo isolado

**Observado:** Corte feminino5: dois rabos laterais presos com elásticos escuros, divisão central e mechas frontais; três conjuntos visuais (calota, rabo esquerdo, direito) podem compor um só módulo.

**Limites:** Arquivo isolado oferece predominantemente uma vista em três quartos/frontal, sem medidas físicas ou superfície interna definida. Requer cruzamento com montagens e checagem3D; fundo e grade não são textura do modelo.


### 057. Cabeça & Rosto/Tipo de Corte de cabelo/Tipos cortes/Feminino/Corte feminino 6 - Corte 6.jpeg

**Papel:** Referência de módulo de cabelo isolado

**Observado:** Corte feminino6: médio, liso com mechas largas, repartido ao centro, testa relativamente aberta; pontas laterais abaixo do queixo.

**Limites:** Arquivo isolado oferece predominantemente uma vista em três quartos/frontal, sem medidas físicas ou superfície interna definida. Requer cruzamento com montagens e checagem3D; fundo e grade não são textura do modelo.


### 058. Cabeça & Rosto/Tipo de Corte de cabelo/Tipos cortes/Feminino/Corte feminino 7 - Corte 7.jpeg

**Papel:** Referência de módulo de cabelo isolado

**Observado:** Corte feminino7: crespo curto arredondado em cachos/grumos, pouco alongamento nas laterais; arco frontal amplo.

**Limites:** Arquivo isolado oferece predominantemente uma vista em três quartos/frontal, sem medidas físicas ou superfície interna definida. Requer cruzamento com montagens e checagem3D; fundo e grade não são textura do modelo.


### 059. Cabeça & Rosto/Tipo de Corte de cabelo/Tipos cortes/Feminino/Corte feminino 8 - Corte 8.jpeg

**Papel:** Referência de módulo de cabelo isolado

**Observado:** Corte feminino8: cachos espirais grandes, repartição central, comprimento médio/longo; o desenho depende das silhuetas dos cachos.

**Limites:** Arquivo isolado oferece predominantemente uma vista em três quartos/frontal, sem medidas físicas ou superfície interna definida. Requer cruzamento com montagens e checagem3D; fundo e grade não são textura do modelo.


### 060. Cabeça & Rosto/Tipo de Corte de cabelo/Tipos cortes/Feminino/Corte feminino 9 - Corte 9.jpeg

**Papel:** Referência de módulo de cabelo isolado

**Observado:** Corte feminino9: afro/cachos densos e volumosos, grande largura e laterais mais longas que7; conferir colisão com cabeça e futuros ombros.

**Limites:** Arquivo isolado oferece predominantemente uma vista em três quartos/frontal, sem medidas físicas ou superfície interna definida. Requer cruzamento com montagens e checagem3D; fundo e grade não são textura do modelo.


### 061. Cabeça & Rosto/Tipo de Corte de cabelo/Tipos cortes/Feminino/Corte feminino 10 - Corte 10.jpeg

**Papel:** Referência de módulo de cabelo isolado

**Observado:** Corte feminino10: muito assimétrico, mechas longas onduladas de um lado e lateral raspada do outro; região raspada expõe sensibilidade à forma do crânio.

**Limites:** Arquivo isolado oferece predominantemente uma vista em três quartos/frontal, sem medidas físicas ou superfície interna definida. Requer cruzamento com montagens e checagem3D; fundo e grade não são textura do modelo.


### 062. Cabeça & Rosto/Tipo de Corte de cabelo/Tipos cortes/Feminino/Corte feminino 11 - Corte 11.jpeg

**Papel:** Referência de módulo de cabelo isolado

**Observado:** Corte feminino11: cabelo curto texturizado com lateral raspada e desenho claro de curvas/cruzes; visualmente aparentado ao masculino10, sem comprovação de malha compartilhada.

**Limites:** Arquivo isolado oferece predominantemente uma vista em três quartos/frontal, sem medidas físicas ou superfície interna definida. Requer cruzamento com montagens e checagem3D; fundo e grade não são textura do modelo.


### 063. Cabeça & Rosto/Tipo de Corte de cabelo/Tipos cortes/Feminino/Corte feminino 12 - Corte 12.jpeg

**Papel:** Referência de módulo de cabelo isolado

**Observado:** Corte feminino12: cabelo longo ondulado, ondas largas e repartição central; silhueta alongada e larga, com região frontal aberta.

**Limites:** Arquivo isolado oferece predominantemente uma vista em três quartos/frontal, sem medidas físicas ou superfície interna definida. Requer cruzamento com montagens e checagem3D; fundo e grade não são textura do modelo.


### 064. Cabeça & Rosto/Tipo de Corte de cabelo/Tipos cortes/Masculino/Corte masculino 1 - Bagunçado 1.jpeg

**Papel:** Referência de módulo de cabelo isolado

**Observado:** Corte masculino1: castanho escuro, feixes grandes facetados, topete e franja assimétricos inclinados, volume concentrado no topo; arco inferior aberto visível.

**Limites:** Arquivo isolado oferece predominantemente uma vista em três quartos/frontal, sem medidas físicas ou superfície interna definida. Requer cruzamento com montagens e checagem3D; fundo e grade não são textura do modelo.


### 065. Cabeça & Rosto/Tipo de Corte de cabelo/Tipos cortes/Masculino/Corte masculino 2 - Bagunçado 2.jpeg

**Papel:** Referência de módulo de cabelo isolado

**Observado:** Corte masculino2: castanho escuro, franja de pontas irregulares voltadas para frente/baixo, distribuição mais radial e arredondada que1; corte curto com massa lateral/posterior.

**Limites:** Arquivo isolado oferece predominantemente uma vista em três quartos/frontal, sem medidas físicas ou superfície interna definida. Requer cruzamento com montagens e checagem3D; fundo e grade não são textura do modelo.


### 066. Cabeça & Rosto/Tipo de Corte de cabelo/Tipos cortes/Masculino/Corte masculino 3 - Hi Fade.jpeg

**Papel:** Referência de módulo de cabelo isolado

**Observado:** Corte masculino3: topo curto com pequenos cachos/blocos, laterais em degradê escuro para tom de pele; cabelo bem rente. O degradê exige estudar material e transição com a pele, além de geometria.

**Limites:** Arquivo isolado oferece predominantemente uma vista em três quartos/frontal, sem medidas físicas ou superfície interna definida. Requer cruzamento com montagens e checagem3D; fundo e grade não são textura do modelo.


### 067. Cabeça & Rosto/Tipo de Corte de cabelo/Tipos cortes/Masculino/Corte masculino 4 - Careca.jpeg

**Papel:** Opção sem módulo de cabelo

**Observado:** Corte masculino4: painel contém apenas 'SEM CABELO / NENHUM MÓDULO'. É uma opção de catálogo sem peça de cabelo; não corresponde a uma24ª malha obrigatória.

**Limites:** Ausência de módulo precisa ser representada pelo aplicativo; não inventar uma malha vazia como condição obrigatória.


### 068. Cabeça & Rosto/Tipo de Corte de cabelo/Tipos cortes/Masculino/Corte masculino 5 - Moicano.jpeg

**Papel:** Referência de módulo de cabelo isolado

**Observado:** Corte masculino5: crista central de mechas rígidas triangulares formando moicano, laterais muito curtas/rentes; volume estreito e alto no topo.

**Limites:** Arquivo isolado oferece predominantemente uma vista em três quartos/frontal, sem medidas físicas ou superfície interna definida. Requer cruzamento com montagens e checagem3D; fundo e grade não são textura do modelo.


### 069. Cabeça & Rosto/Tipo de Corte de cabelo/Tipos cortes/Masculino/Corte masculino 6 - Punk Espetado.jpeg

**Papel:** Referência de módulo de cabelo isolado

**Observado:** Corte masculino6: muitos espinhos longos, grandes e triangulares irradiando para cima e lados; aumenta significativamente o envelope externo.

**Limites:** Arquivo isolado oferece predominantemente uma vista em três quartos/frontal, sem medidas físicas ou superfície interna definida. Requer cruzamento com montagens e checagem3D; fundo e grade não são textura do modelo.


### 070. Cabeça & Rosto/Tipo de Corte de cabelo/Tipos cortes/Masculino/Corte masculino 7 - Razor Part.jpeg

**Papel:** Referência de módulo de cabelo isolado

**Observado:** Corte masculino7: topo penteado lateralmente em grandes faixas, lateral curta, linha raspada clara separando regiões (razor part).

**Limites:** Arquivo isolado oferece predominantemente uma vista em três quartos/frontal, sem medidas físicas ou superfície interna definida. Requer cruzamento com montagens e checagem3D; fundo e grade não são textura do modelo.


### 071. Cabeça & Rosto/Tipo de Corte de cabelo/Tipos cortes/Masculino/Corte masculino 8 - Coque Samurai.jpeg

**Papel:** Referência de módulo de cabelo isolado

**Observado:** Corte masculino8: cabelo penteado para trás até pequeno coque superior/traseiro, com laterais curtas; necessita definir geometria posterior do coque.

**Limites:** Arquivo isolado oferece predominantemente uma vista em três quartos/frontal, sem medidas físicas ou superfície interna definida. Requer cruzamento com montagens e checagem3D; fundo e grade não são textura do modelo.


### 072. Cabeça & Rosto/Tipo de Corte de cabelo/Tipos cortes/Masculino/Corte masculino 9 - Black Power.jpeg

**Papel:** Referência de módulo de cabelo isolado

**Observado:** Corte masculino9: afro arredondado amplo composto de cachos volumosos em grumos facetados; envelope muito maior que cortes rentes.

**Limites:** Arquivo isolado oferece predominantemente uma vista em três quartos/frontal, sem medidas físicas ou superfície interna definida. Requer cruzamento com montagens e checagem3D; fundo e grade não são textura do modelo.


### 073. Cabeça & Rosto/Tipo de Corte de cabelo/Tipos cortes/Masculino/Corte masculino 10 - Chavoso.jpeg

**Papel:** Referência de módulo de cabelo isolado

**Observado:** Corte masculino10: cabelo bem curto texturizado, lateral em degradê e desenhos raspados claros com curvas/cruzes; detalhe de superfície é parte da identidade.

**Limites:** Arquivo isolado oferece predominantemente uma vista em três quartos/frontal, sem medidas físicas ou superfície interna definida. Requer cruzamento com montagens e checagem3D; fundo e grade não são textura do modelo.


### 074. Cabeça & Rosto/Tipo de Corte de cabelo/Tipos cortes/Masculino/Corte masculino 11 - De Raul.jpeg

**Papel:** Referência de módulo de cabelo isolado

**Observado:** Corte masculino11: topo penteado para trás em camadas, linha frontal marcada e laterais em degradê; massa compacta.

**Limites:** Arquivo isolado oferece predominantemente uma vista em três quartos/frontal, sem medidas físicas ou superfície interna definida. Requer cruzamento com montagens e checagem3D; fundo e grade não são textura do modelo.


### 075. Cabeça & Rosto/Tipo de Corte de cabelo/Tipos cortes/Masculino/Corte masculino 12 - Reflexo de Cria.jpeg

**Papel:** Referência de módulo de cabelo isolado

**Observado:** Corte masculino12: crespo curto com grumos e pontas claras sobre base escura, laterais rentes; forma e distribuição de cores participam da identidade.

**Limites:** Arquivo isolado oferece predominantemente uma vista em três quartos/frontal, sem medidas físicas ou superfície interna definida. Requer cruzamento com montagens e checagem3D; fundo e grade não são textura do modelo.


### 076. Cabeça & Rosto/Tipo de rosto/base feminina/base 1 feminino.jpeg

**Papel:** Forma facial feminina 1 sem cabelo e olhos

**Observado:** Inspeção direta: 354 × 190. Vista em três quartos, crânio arredondado, mandíbula suave afunilando até queixo pequeno; pescoço incluído. Órbitas vazias e ausência de cabelo/orelhas visíveis, mas sobrancelhas espessas inclinadas, boca de cantos baixos e pequeno nariz continuam desenhados. Forma visualmente compatível com rosto 1 + cabelo 1 e a base de Rosto Geral Feminino.

**Limites:** É uma das menores referências do grupo; não permite detalhe do nariz, pálpebra, linha de encaixe ou superfície. A base tem expressão própria e nariz remanescente; não equivale a crânio/face neutros sem componentes. Sem frente, perfil ou posterior isolados dessa base.


### 077. Cabeça & Rosto/Tipo de rosto/base feminina/base 2 feminino.jpeg

**Papel:** Forma facial feminina 2, variação mais angular na mandíbula

**Observado:** Inspeção direta: 588 × 370. Três quartos; contorno da mandíbula mais reto/angular e queixo relativamente largo quando comparado à família 1/4/5. Crânio arredondado, órbitas vazias, sobrancelhas grossas, nariz pequeno, boca inclinada para baixo e pescoço; sem cabelo nem orelhas evidentes. Rótulo padrão rosto 2 e silhueta correspondem visualmente ao painel inferior de rosto 2 + cabelo 1.

**Limites:** A categorização angular descreve a imagem, não é nome técnico estabelecido pelo catálogo. Uma única vista e imagem um pouco suave/comprimida não definem cotas, profundidade nem recortes de encaixe. Nariz e expressão continuam presentes; não há evidencia visual de separação topológica desses detalhes.


### 078. Cabeça & Rosto/Tipo de rosto/base feminina/base 3 feminino.jpeg

**Papel:** Forma facial feminina 3, variação arredondada

**Observado:** Inspeção direta: 577 × 373. Vista em três quartos com bochechas cheias, mandíbula arredondada e queixo curto, criando face mais redonda que 2/4/5. Mantém sobrancelhas, boca, pequeno nariz, órbitas vazias e pescoço; não mostra cabelo ou orelhas externas. A montagem rosto 3 + cabelo 1 também apresenta bochechas cheias e contorno inferior arredondado.

**Limites:** Sem frente/perfil/posterior próprios da base. O volume de bochecha é leitura de contorno e iluminação, sem medida. Nenhuma borda indica onde terminaria uma peça nasal independente; o nariz já se encontra representado na base. Sobrancelhas e boca trazem expressão, o que deve ser considerado separado de uma escolha futura de forma facial.


### 079. Cabeça & Rosto/Tipo de rosto/base feminina/base 4 feminino.jpeg

**Papel:** Forma facial feminina 4, variação alongada e afunilada

**Observado:** Inspeção direta: 589 × 369. Três quartos; maçãs do rosto altas visualmente, bochechas estreitas e terço inferior longo convergindo para queixo estreito/pontudo. Preserva órbitas vazias, sobrancelhas, nariz pequeno, boca e pescoço; não mostra orelhas/cabelo. O alongamento e a ponta do queixo também são legíveis na montagem rosto 4 + cabelo 1.

**Limites:** Não há perfil isolado para confirmar projeção anterior do queixo ou comprimento do nariz. A referência não fornece parâmetros que diferenciem numericamente essa forma da 5. A base continua contendo nariz e expressão; o arquivo não demonstra modularidade técnica.


### 080. Cabeça & Rosto/Tipo de rosto/base feminina/base 5 feminino.jpeg

**Papel:** Forma facial feminina 5, variação de maçãs largas e queixo fino

**Observado:** Inspeção direta: 568 × 375. Três quartos; região superior e maçãs do rosto largas, estreitamento nítido para queixo pequeno, com contorno mais compacto que a forma 4. Crânio sem cabelo e órbitas vazias; sobrancelhas grossas, pequeno nariz, boca de cantos baixos e pescoço permanecem. O painel de montagem rosto 5 + cabelo 1 confirma visualmente a oposição entre largura das maçãs e ponta do queixo.

**Limites:** Rótulo só fornece número; termos como compacto/afunilado são descrições, não categorias oficiais. Sem frente/perfil/posterior isolados, medidas de crânio ou encaixe de pescoço. O nariz integrado visualmente precisa ser reconciliado com a intenção de nariz modular mostrada na prancha geral.


### 081. Cabeça & Rosto/Tipo de rosto/bases masculina/base masculina 1.jpeg

**Papel:** Forma facial masculina 1 isolada do cabelo e olhos

**Observado:** Inspeção direta: 267 × 328, vista única em três quartos. Cabeça alongada moderadamente, maçãs do rosto marcadas e mandíbula que afunila para queixo arredondado/anguloso. Retém sobrancelhas grossas, boca, barba, pescoço, bloco nasal claro e saliência lateral achatada; órbitas vazias e crânio sem cabelo. A composição e a forma correspondem visualmente à base da prancha Rosto Geral Masculino e à metade inferior de base 1 + corte 1.

**Limites:** Resolução muito pequena e apenas três quartos; não define perfil exato, vista posterior ou detalhes de união. Texto afirma olhos/nariz/orelhas/cabelo removidos, porém as saliências lateral e nasal permanecem. Não é uma superfície facial lisa nem sem características. A correspondência é visual; não houve comparação de malhas nem prova de recorte idêntico.


### 082. Cabeça & Rosto/Tipo de rosto/bases masculina/base masculina 2.png

**Papel:** Forma facial masculina 2, variação de mandíbula afunilada

**Observado:** Inspeção direta: 1619 × 971, três quartos. Crânio superior largo, faces laterais marcadas, terço inferior afunilando para queixo relativamente estreito e longo. Crânio sem cabelo e órbitas vazias, mas sobrancelhas, boca, barba, pescoço, placa/bloco nasal e saliência lateral permanecem. A montagem base 2 + corte 1 apresenta o mesmo tema de rosto mais estreito no terço inferior; esta imagem detalha melhor a base.

**Limites:** Uma única perspectiva não demonstra simetria, largura frontal real ou profundidade lateral; não há traseira da base. A diferença para a base 5 é graduada, não uma categoria geométrica nomeada pelo catálogo. A classificação como afunilada é descritiva. Facetas visíveis não provam contagem de polígonos, conectividade ou separação de barba/sobrancelhas.


### 083. Cabeça & Rosto/Tipo de rosto/bases masculina/base masculina 3.png

**Papel:** Forma facial masculina 3, variação de mandíbula larga e mais reta

**Observado:** Inspeção direta: 1628 × 966, três quartos. Terço inferior mais largo e horizontal que na base 2; queixo amplo e contorno mandibular com tendência retangular. Mantém a linguagem comum de crânio arredondado facetado, sobrancelhas grossas, órbitas vazias, bloco nasal, barba, boca de cantos baixos, saliência auricular e pescoço. Corresponde tematicamente ao rosto largo/baixo da montagem base 3 + corte 1.

**Limites:** Sem frente nem perfil isolado dessa base; não é possível extrair cotas ou assegurar o mesmo crânio de outra variante. Barba ocupa o contorno inteiro da mandíbula e oculta a forma exata da pele sob ela. Aparência facetada e sombreamento não indicam a estrutura real de uma malha exportável.


### 084. Cabeça & Rosto/Tipo de rosto/bases masculina/base masculina 4.png

**Papel:** Forma facial masculina 4, variação mais cheia/arredondada

**Observado:** Inspeção direta: 1629 × 965, três quartos. Bochechas e mandíbula formam contorno cheio; queixo amplo e arredondado, sem o estreitamento pronunciado de 2/5. Conserva sobrancelhas, órbitas vazias, placa nasal, saliência lateral, boca, barba e pescoço. A barba exibe pequenas facetas/linhas muito mais densas que o crânio. A montagem base 4 + corte 1 confirma visualmente a intenção de face mais redonda e larga.

**Limites:** Há só três quartos da base. O preenchimento da bochecha/barba é aparente e não mede volume ou espessura. A densidade de triângulos aparente na barba pode pertencer à imagem/material e não à malha; não usar como prova topológica. Nenhum desenho mostra como o cabelo 1 acompanha a variação do topo ou como olhos e nariz se ajustam.


### 085. Cabeça & Rosto/Tipo de rosto/bases masculina/base masculina 5.png

**Papel:** Forma facial masculina 5, variação estreita e alongada

**Observado:** Inspeção direta: 1619 × 971, três quartos. Maçã do rosto saliente, recuo visível abaixo dela e mandíbula convergente para queixo mais estreito/alongado. A parte superior arredondada se mantém semelhante à família; base tem sobrancelhas, barba, boca, órbitas, pescoço, bloco nasal e saliência lateral. A montagem base 5 + corte 1 enfatiza de frente o alongamento e a face estreita; relação visual coerente entre os dois arquivos.

**Limites:** A distinção quantitativa em relação a 2 não é fornecida. Não há perfil/posterior específico nem escala comum certificada. Barba e sombra contribuem para a percepção de bochecha cavada, portanto não se pode inferir toda a anatomia subjacente. Os encaixes de cabelo, órbitas e nariz são apenas sugeridos pelo desenho.


### 086. Cabeça & Rosto/Tipo de rosto/bases masculina/base masculina 6.png

**Papel:** Forma facial masculina 6, variação de mandíbula robusta

**Observado:** Inspeção direta: 1639 × 959, três quartos. Terço inferior largo e robusto, queixo amplo e base mandibular quase horizontal; laterais menos afuniladas que 2/5. Retém as mesmas famílias de detalhes: barba, sobrancelhas, boca, pescoço, órbitas vazias, bloco nasal e peça/saliência auricular achatada. A montagem base 6 + corte 1 mostra frente de mandíbula pesada/larga, compatível com a leitura desta base.

**Limites:** Diferenças para 3/4 concentram-se no contorno inferior e não têm nomes ou parâmetros explícitos; chamar de robusta é descrição visual. Vista única em três quartos, sem traseira, planta ou lateral isolada. Pescoço já incluído, sem linha de separação cabeça-pescoço demonstrada. Não prova intercâmbio sem ajuste com outros olhos/narizes/cabelos.


### 087. Cabeça & Rosto/Tipo de rosto/Padrao de mudanca de Rosto.jpeg

**Papel:** Prancha conceitual masculina de vistas e decomposição modular

**Observado:** Inspeção direta: 1536 × 1024. Faixa superior mostra frente, lateral voltada à direita da imagem, costas e lateral voltada à esquerda; faixa inferior mostra cabeça em três quartos, cabelo/olhos/nariz/orelhas afastados e uma base em três quartos. Cabeça masculina de cabelo castanho curto em mechas pontudas, sobrancelhas escuras grossas, olhos semicerrados, barba e mandíbula larga/quadrada. A parte inferior do rosto é mais larga do que em Rosto Geral Masculino, apesar de a composição ser quase igual. A prancha nomeia base, cabelo, dois olhos, nariz e duas orelhas. A base representada retém sobrancelhas, boca, barba, pescoço, depressões orbitais, bloco nasal claro e saliências laterais achatadas na região das orelhas.

**Limites:** O nome do arquivo sugere padrão de mudança de rosto, mas o conteúdo não é uma matriz de formas faciais: é uma única cabeça com componentes explodidos. O texto diz que orelhas e nariz foram removidos, mas ainda há formas nas respectivas regiões; podem ser suportes/zonas de encaixe, hipótese que a imagem não resolve. Não prova peças reais, topologia, espessura, escala, pivôs, identidade exata entre vistas nem encaixe universal. A própria legenda pede validar encaixes na malha 3D.


### 088. Cabeça & Rosto/Tipo de rosto/rosto  + cabelo feminino 1/rosto 1 + cabelo 1.jpeg

**Papel:** Exemplo montado feminino 1 com corte 1

**Observado:** Inspeção direta: 358 × 457. Painel superior quase frontal, inferior da base em três quartos. Cabelo castanho assimétrico, mechas facetadas grossas e franja comprida à esquerda da imagem. Rosto de mandíbula suave e queixo pequeno, olhos semicerrados, sobrancelhas inclinadas, boca de cantos baixos; orelha visível à direita da imagem e outra região coberta pelo cabelo. A base inferior retém nariz, sobrancelhas, boca e pescoço e corresponde visualmente à base feminina 1.

**Limites:** Franja oculta parte importante da lateral do crânio, testa e uma orelha; não é possível inspecionar todos os encontros do cabelo com a cabeça. Vistas diferentes entre montagem e base, sem perfil/posterior específico deste par. Pequena resolução limita detalhes; igualdade do corte entre as cinco montagens é uma intenção visual, não prova de um mesmo objeto 3D.


### 089. Cabeça & Rosto/Tipo de rosto/rosto  + cabelo feminino 1/rosto 2 + cabelo 1.jpeg

**Papel:** Exemplo montado feminino 2 com corte 1

**Observado:** Inspeção direta: 349 × 439. Montagem quase frontal com mandíbula mais reta/larga que 1/4/5, cabelo assimétrico longo de um lado e base em três quartos abaixo. A franja cruza parte da testa; sobrancelhas, olhos semicerrados, nariz, boca e uma orelha estão legíveis. Base inferior contém nariz/sobrancelhas/boca/pescoço. Rótulos cabeça feminina 2, corte feminino 1 e padrão rosto 2 são internamente coerentes com base feminina 2.

**Limites:** Não há lateral ou posterior dessa variante; cabelo oculta parte do perímetro facial e do crânio. A expressão mantém-se semelhante entre variantes, mas não há neutralização que isole estritamente só a forma. Não demonstra como reajustar cabelo, nariz e olhos ao trocar a base.


### 090. Cabeça & Rosto/Tipo de rosto/rosto  + cabelo feminino 1/rosto 3 + cabelo 1.jpeg

**Papel:** Exemplo montado feminino 3 com corte 1

**Observado:** Inspeção direta: 342 × 435. Face mais cheia/redonda, bochechas amplas e queixo curto; montagem frontal/quase frontal sobre base em três quartos. O cabelo repete franja longa lateral e mechas castanhas; olhos semicerrados e boca de cantos baixos seguem a família. Base inferior preserva nariz, boca, sobrancelhas e pescoço. O contorno corresponde ao padrão de base feminina 3.

**Limites:** A frontalidade aproximada não fornece vista ortogonal calibrada; não se podem derivar proporções métricas por simples medição de pixels. Sem perfis/posterior e sem cabelo isolado nesta imagem. A aparência redonda não informa rig, deformação de expressão nem topologia de bochechas.


### 091. Cabeça & Rosto/Tipo de rosto/rosto  + cabelo feminino 1/rosto 4 + cabelo 1.jpeg

**Papel:** Exemplo montado feminino 4 com corte 1

**Observado:** Inspeção direta: 369 × 444. Montagem quase frontal com terço inferior alongado, bochechas estreitas e queixo fino/pontudo; base em três quartos abaixo. Mesma família de cabelo assimétrico em mechas grandes, uma orelha exposta e expressão de olhos semicerrados/boca inclinada para baixo. Base inferior retém nariz, sobrancelhas, boca e pescoço; forma alinhada visualmente à base feminina 4.

**Limites:** Sem perfil/posterior específicos. Franja cobre partes do lado oposto e impede inspeção completa do cabelo em torno das orelhas. Rostos 4/5 têm queixo fino, mas a imagem não define limites ou valores para tornar essas famílias tecnicamente distintas. Restos de bordas de painel adjacente não constituem uma vista adicional utilizável.


### 092. Cabeça & Rosto/Tipo de rosto/rosto  + cabelo feminino 1/rosto 5 + cabelo 1.jpeg

**Papel:** Exemplo montado feminino 5 com corte 1

**Observado:** Inspeção direta: 343 × 441. Rosto de maçãs relativamente largas que converge para queixo fino/curto; desenho mais compacto que a montagem 4. Montagem quase frontal com cabelo lateral castanho, franja extensa, olhos semicerrados e uma orelha exposta; base em três quartos abaixo. A base inferior tem órbitas vazias mas mantém nariz, sobrancelhas, boca e pescoço, coerente visualmente com base feminina 5.

**Limites:** Não mostra perfil ou posterior próprios; topo/lateral do crânio ficam ocultos na montagem. Não estabelece dimensões nem comportamento de encaixe do corte 1 sobre a forma mais afunilada. O catálogo mostra uma combinação por forma facial neste subgrupo, não todas as combinações entre olhos, nariz, cabelos e bases.


### 093. Cabeça & Rosto/Tipo de rosto/rosto  + cabelo masculino 1/base 1 + corte 1.jpeg

**Papel:** Exemplo montado masculino 1 com corte 1 e base correspondente

**Observado:** Inspeção direta: 262 × 336. Painel superior frontal com cabelo curto castanho em mechas pontudas, orelhas, olhos semicerrados, nariz e barba; inferior mostra base sem cabelo/olhos em três quartos. Forma facial equilibrada, queixo moderadamente afunilado. O cabelo e expressão acompanham a família dos seis exemplos masculinos. Os rótulos ligam cabeça masculina 1/corte masculino 1 ao padrão rosto 1, e a base inferior é visualmente compatível com base masculina 1.

**Limites:** Arquivo muito pequeno: cada cabeça ocupa apenas parte dos 336 pixels de altura; não permite detalhes de união ou ajuste. Vistas são diferentes entre base e montagem, portanto não constituem antes/depois no mesmo ângulo. Não há perfis nem posterior dessa combinação no arquivo; usar pranchas gerais somente como apoio visual da família, sem provar identidade de malha.


### 094. Cabeça & Rosto/Tipo de rosto/rosto  + cabelo masculino 1/base 2 + corte 1.jpeg

**Papel:** Exemplo montado masculino 2 com corte 1

**Observado:** Inspeção direta: 252 × 336. Montagem frontal e base em três quartos. Face relativamente estreita com queixo afunilado, comparada a 3/4/6. Repete o cabelo curto pontudo do corte 1, sobrancelhas fortes, olhos semicerrados, barba e orelhas visíveis; a base inferior mantém sobrancelhas/barba/boca e blocos nasal/lateral. Rótulos e silhueta associam esta montagem à base masculina 2.

**Limites:** Resolução muito reduzida e ângulos distintos entre painéis; não mede a mudança de crânio, distância dos olhos ou escala do cabelo. Não mostra interior do cabelo nem união nariz/rosto; repetição do estilo do corte não prova geometria idêntica. Sem perfis e posterior específicos.


### 095. Cabeça & Rosto/Tipo de rosto/rosto  + cabelo masculino 1/base 3 + corte 1.jpeg

**Papel:** Exemplo montado masculino 3 com corte 1

**Observado:** Inspeção direta: 265 × 336. Cabeça frontal com mandíbula larga e inferior mais horizontal; embaixo, base em três quartos com olhos/cabelo ausentes. Cabelo castanho curto em pontas e expressão acompanham as demais montagens; base inferior combina visualmente com base masculina 3. Rodapé legível afirma 'Um corte. Três rostos. Mesmo encaixe.', mas o próprio arquivo mostra um único par de cabeça e base.

**Limites:** Rodapé pode ter vindo de uma prancha maior; não demonstra três rostos dentro desta imagem e não prova encaixe geométrico. Baixa resolução e perspectiva diferente dos dois painéis impedem aferição de correspondência exata. Não apresenta perfis/posterior da variante 3.


### 096. Cabeça & Rosto/Tipo de rosto/rosto  + cabelo masculino 1/base 4 + corte 1.jpeg

**Papel:** Exemplo montado masculino 4 com corte 1

**Observado:** Inspeção direta: 506 × 690. Painel frontal mostra face mais cheia/arredondada, bochechas amplas e queixo largo curvo; painel inferior traz base em três quartos. Cabelo curto pontudo, olhos semicerrados, nariz, orelhas e barba acompanham a família masculina 1. O contorno mais arredondado corresponde à base masculina 4. Na base inferior continuam sobrancelhas, barba, boca, pescoço, placa nasal e volume lateral auricular.

**Limites:** Sem perfil/posterior próprios e sem vista do cabelo separado. A base inferior continua expressiva e não é neutra. O cabelo parece da mesma família, mas a prancha não permite provar que foi usado o mesmo objeto com dimensões preservadas. Bordas recortadas na parte superior sugerem extração de catálogo; não se dispõe da prancha completa neste arquivo.


### 097. Cabeça & Rosto/Tipo de rosto/rosto  + cabelo masculino 1/base 5 + corte 1.jpeg

**Papel:** Exemplo montado masculino 5 com corte 1

**Observado:** Inspeção direta: 531 × 708. Frente alongada, bochechas mais estreitas sob as maçãs do rosto e queixo estreito; base correspondente em três quartos abaixo. Cabelo em mechas pontudas mantém a linguagem do corte 1; barba acentua a silhueta estreita. Rótulos e contorno correspondem à base masculina 5. As duas imagens incluem pescoço; a base inferior retém os detalhes comuns de boca/barba/sobrancelhas e blocos nasal/lateral.

**Limites:** Cabelo e rosto foram apresentados montados sem descrever adaptações. Não é demonstração de montagem automatizada sem ajustes. Não há perfis ou posterior da variante. A extensão da barba pode afetar leitura do queixo. Restos de divisórias de outros painéis aparecem nas bordas e não são referências adicionais completas.


### 098. Cabeça & Rosto/Tipo de rosto/rosto  + cabelo masculino 1/base 6 + corte 1.jpeg

**Papel:** Exemplo montado masculino 6 com corte 1

**Observado:** Inspeção direta: 522 × 695. Cabeça frontal com mandíbula robusta/quadrada, queixo amplo e pescoço largo; base em três quartos embaixo. Mantém corte curto pontudo, olhos semicerrados, sobrancelhas grossas e barba; base inferior é visualmente compatível com base masculina 6. Rodapé afirma 'Um corte. Três rostos bem distintos. Mesmo encaixe.', embora esta imagem contenha apenas a variante 6.

**Limites:** A afirmação de mesmo encaixe é texto da referência, não validação de uma interface 3D. Sem perfis/posterior próprios. Os dois painéis têm ângulos diferentes, impossibilitando sobreposição direta. A variedade do terço inferior é clara, mas o topo do crânio fica oculto na montagem e não permite concluir que seja invariável.


### 099. Exemplo Geral/FemaleExemple.jpeg

**Papel:** Contexto de personagem e módulos do corpo

**Observado:** Prancha feminina completa: três módulos grandes — cabeça com cabelo e pescoço; superior com torso, mangas, braços e mãos; inferior com quadril, pernas e pés. Mostra separação frontal, traseira e montagem em três quartos. Estilo estilizado facetado, cabeça grande e roupas de mecânica. Junções indicadas no pescoço e cintura; é contexto para a evolução ao corpo.

**Limites:** Prancha de intenção visual: não define medidas, bordas3D, rigging nem topologia. Oferece traseira da cabeça, mas não decompõe todos os componentes faciais. Corpo pertence a etapa futura.


### 100. Exemplo Geral/MaleExemple.jpeg

**Papel:** Contexto de personagem e módulos do corpo

**Observado:** Prancha masculina completa: cabeça com cabelo e pescoço; superior com torso, mangas, braços e mãos; inferior com quadril, pernas e pés. Frente/traseira separadas e montagem em três quartos. Barba e sobrancelhas definem expressão; luva em uma mão e tatuagens pertencem ao conjunto superior ilustrado. Pescoço/cintura são fronteiras propostas.

**Limites:** Prancha de intenção visual: não define medidas, bordas3D, rigging nem topologia. Oferece traseira da cabeça, mas não decompõe todos os componentes faciais. Corpo pertence a etapa futura.
