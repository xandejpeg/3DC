# GLBs do 3DC Lab v1 para o jogo 3D

Destino: projeto do jogo **Real Car Lifestyle**. Este conjunto serve ao estudo e à integração inicial de personagens; contém cabeças estáticas, não personagens completos prontos para animação. A importação e o comportamento na engine ainda não foram testados.

## Arquivos de entrada e de saída

| Uso | Arquivos |
| --- | --- |
| Fonte de modelagem atual | [Cena Blender da revisão 2](../artifacts/conjunto-feminino-v2/conjunto-feminino-v2.blend) |
| Fontes dos cortes 2–12 | [Uma cena e um GLB por corte](../artifacts/cabelos-femininos-v1/README.md) |
| Biblioteca modular do seletor | [public/models/rcl-feminino-v2](../public/models/rcl-feminino-v2/) |
| IDs, slots e arquivos | [manifest.json](../public/models/rcl-feminino-v2/manifest.json) |
| Exemplos de montagem do Blender | [montagens/cabeca-feminina-01…05.glb](../artifacts/conjunto-feminino-v2/montagens/) |
| Saídas do teste com exportador do aplicativo | [exportacoes-app](../artifacts/conjunto-feminino-v2/exportacoes-app/) |
| Nova combinação escolhida pelo usuário | Botão **Exportar montagem GLB** no seletor; download `personagem-<data>.glb` |

Os nomes históricos `base-N-corte-1.glb` em `exportacoes-app/` também contêm Olho 1, Nariz 1 e as partes fixas nesta revisão. São evidências do exportador, não uma categoria adicional de personagem.

## Contrato que o jogo deve preservar

- Unidades de trabalho em metros. No Blender: Z para cima, frente em −Y. A exportação converte para glTF com Y para cima e frente em +Z. Conferir a conversão aplicada pelo importador da engine; não reaplicar uma correção já feita por ele.
- Usar uma raiz comum para montar os módulos. Não centralizar, ajustar escala ou alinhar pelo centro da caixa de cada peça individualmente: as posições já carregam o referencial compartilhado.
- Cinco bases, Cortes 1–12, um Olho 1 em par e um Nariz 1. Sobrancelhas, boca e orelhas estão dentro do GLB da base e mudam com ela. São 60 combinações estáticas verificadas no montador.
- GLB montado pode conter diversos nós/malhas e materiais. Exportar tudo num arquivo não solda as superfícies nem cria um rig.
- IDs `module_id`, `base_id`, revisão e dados do catálogo ajudam a rastrear a origem. Importadores podem tratar metadados extras de formas diferentes; manter o manifesto junto dos arquivos na integração.
- O catálogo atual foi testado como conjunto. Um GLB externo aceito pelo seletor não ganha compatibilidade geométrica automaticamente.

Materiais, geometrias e recursos usados pelo conjunto estão dentro dos GLBs. Não há texturas externas obrigatórias nesses assets. A imagem de referência, seu fundo e sua grade não viraram texturas do personagem.

Os cortes 10/11 usam `COLOR_0` para o degradê do raspado: preservar cores de vértices e a multiplicação pelo material no importador. Os cabelos 7/9/11 são os mais densos (aproximadamente 122/141/162 mil triângulos); precisam de orçamento e LOD antes de serem multiplicados em uma população do jogo. A prioridade desta etapa foi a forma e o encaixe; ela não certifica desempenho. O [registro dos cabelos](registros/2026-09-17-cabelos-femininos.md) detalha os limites visuais.

## O que ainda precisa ser decidido/testado no jogo

| Área | Estado no laboratório / próximo teste |
| --- | --- |
| Importação real | Conferir eixos, escala, nomes, materiais, orientação de faces e limites de cena na engine escolhida |
| Aparência | Repetir frente, perfil, três quartos e costas com a iluminação do jogo; comparar junções e silhuetas |
| Movimento | Sem rig, pesos, piscar, expressões ou rotação do olhar; o segmento ocular atual é estático |
| Corpo | Pescoço existe; conexão com tronco/corpo ainda não foi produzida nem validada |
| Desempenho | Orçamentos de triângulos, materiais, chamadas de desenho, LOD e memória precisam vir da plataforma e cena do jogo; não foram fixados aqui |
| Colisão | Não há colisores de gameplay; interseção geométrica base/cabelo é um teste distinto |
| População | Sem randomizador, regras de combinação ou geração em lote dos 50 personagens/200 NPCs |

Para incorporar um personagem no jogo, registrar no projeto de destino: commit de origem do 3DC, revisão do catálogo, IDs selecionados, caminho/nome do GLB, hash do arquivo, versão/configuração do importador e resultado do teste visual. Assim, uma correção no laboratório pode ser aplicada de forma rastreável.

As limitações visuais atuais estão na [entrega](../artifacts/conjunto-feminino-v2/ENTREGA.md). O laboratório permanecer na v1 não elimina essas etapas de validação; também não impede que os assets sejam usados agora em cenas de protótipo.
