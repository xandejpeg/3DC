# Cortes femininos 2–12 — 3DC Lab v1

Pedido: acrescentar onze cabelos independentes ao seletor, compatíveis com as cinco bases já entregues. Trocar rosto conserva cabelo; trocar cabelo conserva rosto, Olho 1, Nariz 1 e partes fixas. O fluxo de exportação do aplicativo ficou fora desta alteração.

## Referências e escolhas

Foram abertas as onze referências isoladas R053–R063 e as oito pranchas femininas R001–R008. As cópias do [catálogo portátil](../referencias-rcl/Catalogo_portatil.json) conservam os bytes dos originais indicados pelo usuário. O [registro de hashes desta etapa](../../artifacts/cabelos-femininos-v1/referencias-verificadas.json) relaciona os arquivos consultados.

| Corte | Referência isolada | Montagens consultadas | Característica modelada |
| --- | --- | --- | --- |
| 2 | R053 | R001/R005 | Comprimento longo, camadas e franja cheia |
| 3 | R054 | R001/R005 | Franja, mechas soltas e rabo baixo à direita da imagem frontal |
| 4 | R055 | R002/R006 | Bob arredondado, franja com término reto |
| 5 | R056 | R002/R006 | Risca central, dois rabos baixos e elásticos |
| 6 | R057 | R002/R006 | Comprimento médio, testa aberta e moldura lateral |
| 7 | R058 | R003/R007 | Cachos curtos distribuídos em volume arredondado |
| 8 | R059 | R003/R007 | Mechas com rotação em espiral e risca central |
| 9 | R060 | R003/R007 | Afro mais largo e comprido que o corte 7 |
| 10 | R061 | R004/R008 | Ondas à esquerda da imagem e lateral oposta raspada |
| 11 | R062 | R004/R008 | Topo crespo curto, curvas e cruzes na lateral raspada |
| 12 | R063 | R004/R008 | Ondas longas e amplas, repartidas ao centro |

O uso de outras variantes oculares nas pranchas é contexto visual; esta entrega mantém o Olho 1 e o Nariz 1 existentes. Nenhuma sexta base feminina foi inferida de legendas contraditórias.

## Implementação e parâmetros relacionados

O construtor [rcl-cabelos.py](../../scripts/rcl-cabelos.py) carrega somente a cena `RCL_Faciais_01` como biblioteca. Mantém as cinco bases, as partes fixas, os olhos, o nariz e o referencial. Não executa novamente os scripts de geração do rosto. O Corte 1 é removido apenas da nova cena de trabalho; seu arquivo de origem continua intacto.

Cada cabelo é um objeto com casca de apoio e mechas volumétricas fechadas. Grupos de vértices nomeados identificam calota, franja, mechas, cachos, rabos, elásticos e desenhos. As malhas podem ter ilhas sobrepostas: constituem um módulo de aparência, não um sólido único soldado para impressão. Espirais recebem um volume arredondado de apoio; ondas usam curvas com frequências distintas. As partes ocultas e a traseira são interpretações, pois as referências individuais não fornecem vistas calibradas dessas regiões.

- **Comprimento, largura e caimento posterior** variam juntos: os cabelos longos mantêm folga das orelhas e do pescoço enquanto as pontas voltam para dentro.
- **Altura da linha frontal, risca, largura das mechas e término da franja** definem juntos a abertura para o rosto. O corte 4 tem franja romba; 2/3 conservam pontas irregulares.
- **Raio, espaçamento e volume de cachos** acompanham o volume geral; 7 e 9 não são recolorações da mesma peça. 8 e 12 usam ritmos de curva distintos.
- **Raspado, limite da casca e desenhos** seguem a mesma superfície craniana. O degradê usa cores de vértices; os desenhos e elásticos pertencem ao GLB do cabelo.
- **Folga interna e curvatura das mechas** dependem do volume conjunto das cinco bases e das partes faciais. Isso evita correções de posição/escala no aplicativo.

Os parâmetros executados e referências ficam em `corte-NN/progresso.json`; a cena é salva antes das prévias para resistir a interrupções. As medidas são controles de implementação no referencial existente, sem normalização estética aos 24 cm.

## Problemas encontrados e correções

1. A transição abrupta entre crânio e cabelo longo criava um degrau. A interpolação do caimento foi suavizada.
2. Projetar mechas contra normais de superfícies faciais abertas criava pontas junto aos olhos. Essas superfícies deixaram de participar dessa projeção local.
3. Mechas curvas dos cortes 5/6/8/12 e regiões de 7/10 ainda atravessavam têmporas ou orelhas entre vértices. Foi usado um envelope radial comum, obtido da união das cinco bases e peças faciais, com folga conservadora. O corte 12 precisou de folga adicional junto à orelha direita. Somente o cabelo foi corrigido.
4. O primeiro raspado apresentava faixas de material visíveis. Foi substituído por degradê contínuo em `COLOR_0`. A reimportação alterou a estrutura de nós do material; a verificação passou a comparar o fator de cor efetivo e as cores de vértices, em vez do valor desconectado de um socket. A diferença máxima registrada nas cores foi cerca de 0,0032, abaixo da tolerância de quantização de 8 bits de 0,005.
5. A conferência de perfil revelou uma faixa descoberta entre cachos do corte 11. A distribuição passou de incrementos de ângulo para distâncias ao longo do contorno, reduzindo a lacuna lateral. Somente esse corte foi reconstruído e novamente validado após a revisão final de vistas.

## Entrega e verificação

- [Checkpoints por corte](../../artifacts/cabelos-femininos-v1/README.md): onze `.blend`, onze GLBs, frente, perfil, três quartos, costas e cabelo isolado.
- [Comparação visual](../../artifacts/cabelos-femininos-v1/comparacao-referencias.jpg) e [catálogo com hashes](../../artifacts/cabelos-femininos-v1/catalogo.json).
- Onze GLBs reimportados no Blender: triângulos/posições e fatores de materiais preservados. Cores de vértices conferidas nos cortes 10/11.
- 55 combinações dos cabelos novos com as cinco bases: nenhum cruzamento de triângulos detectado entre cabelo e base, partes fixas, olhos ou nariz. Este teste não avalia interseções internas entre as próprias mechas.
- [Teste do seletor](../../artifacts/cabelos-femininos-v1/teste-seletor.json): `SceneManager` real, 60 trocas de rosto e 60 de cabelo, preservando instâncias dos outros slots, geometria, materiais e partes fixas. Sem navegador/WebGL.
- [Khronos Validator](../../artifacts/cabelos-femininos-v1/khronos.txt): 11 arquivos, zero erros, avisos, informações ou dependências externas.
- `npm run build` aprovado, com o aviso já existente de bundle JavaScript maior que 500 kB. Servidor local respondeu HTTP 200.

O manifesto ganhou onze entradas; os textos do catálogo passaram a informar 12 cortes. IDs existentes, arquivos das cinco bases, Corte 1, Olho 1, Nariz 1 e exportador do aplicativo permaneceram inalterados. O navegador não estava disponível na ferramenta desta sessão, portanto não houve conferência por cliques nem medição de WebGL.

## Limites visuais e de uso

Esta é a primeira versão desses cabelos. Algumas mechas são mais regulares/espessas que os desenhos; cachos 7/9/11 ainda têm distribuição e detalhe simplificados, e o corte 10 tem menos volume no topo que a referência. A transição de pele dos raspados e seus desenhos merecem revisão com a iluminação do jogo. Não declarar reprodução exata.

Os cabelos 7/9/11 têm aproximadamente 122/141/162 mil triângulos, respectivamente. Não há LOD, rig, física de cabelo ou teste com corpo/ombros. O contraste dos rostos continua o da entrega anterior; esta etapa não corrige boca, nariz, pálpebras ou proporções faciais. A próxima decisão de produto é quais cortes terão prioridade numa segunda revisão visual e qual orçamento de geometria o jogo precisa. Esses limites não impedem testar agora as 60 combinações estáticas no laboratório.
