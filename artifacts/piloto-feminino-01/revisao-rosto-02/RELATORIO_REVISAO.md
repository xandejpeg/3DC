# Revisão limitada do rosto — piloto feminino 01 / R02

17/09/2026. Base feminina 1 com o mesmo Corte Feminino 1. Esta revisão trata o contorno inferior do rosto e a transição do pescoço. A próxima alteração depende da avaliação do usuário sobre esta comparação.

## Arquivos e comparação

- [Antes/depois: base isolada e montada](imagens/antes_depois_resumo.png).
- [Base isolada: frente, perfil, três quartos e costas](imagens/antes_depois_base.png).
- [Montagem: frente, perfil, três quartos e costas](imagens/antes_depois_montagem.png).
- [Blender revisado](piloto-feminino-01-rosto-r02.blend), com cenas `RCL_R02_ANTES`, `RCL_R02_DEPOIS` e duas cenas de reimportação.
- GLBs revisados: [base](base-feminina-01.glb), [cabelo](corte-feminino-01.glb), [montagem](montagem-feminina-01.glb).
- [Cópia binária do Blender anterior](anterior-preservado.blend). O .blend e os três GLBs da pasta superior continuam intactos, conferidos por SHA-256.
- [Parâmetros e preservação](verificacao/parametros_e_preservacao.json), [câmeras](verificacao/cameras_comparacao.json) e [reimportação](verificacao/reimportacao.json).

As pranchas usam renders das duas cenas nativas, sem retoque da geometria nas imagens. Os GLBs foram conferidos separadamente por reimportação. Em cada par antes/depois, câmera, projeção ortográfica, enquadramento, resolução, luzes, materiais e gestão de cor são iguais. Não houve recentralização ou ajuste automático de tamanho por versão. As posições das quatro câmeras e a escala ortográfica de 0,395 m repetem as vistas do primeiro piloto; ambos os estados desta comparação foram renderizados em 900 × 1000, 128 amostras. Os PNGs individuais estão em `imagens/`.

## Referências e leitura visual

Os arquivos originais foram localizados pelo [inventário JSON](../../../docs/referencias-rcl/Inventario_completo_referencias_RCL.json). Foram relidos os trechos sobre formas faciais, detalhes remanescentes nas bases e limites das vistas na [análise completa](../../../docs/referencias-rcl/Analise_completa_referencias_RCL.md).

| Referência reaberta | Uso nesta revisão |
|---|---|
| R076 — `Cabeça & Rosto/Tipo de rosto/base feminina/base 1 feminino.jpeg` | Queixo pequeno e arredondado, afunilamento moderado, continuidade entre mandíbula e pescoço. |
| R088 — `Cabeça & Rosto/Tipo de rosto/rosto  + cabelo feminino 1/rosto 1 + cabelo 1.jpeg` | Comparação da silhueta isolada e montada; referência de um rosto mais compacto abaixo das órbitas. Reaberta após os renders. |
| R049 — `Cabeça & Rosto/Rosto Geral/Rosto Geral Feminino.jpeg` | Relação mandíbula/pescoço no perfil e em três quartos, além da vista posterior. O painel chamado perfil esquerdo continua tratado como três quartos. |
| R052 — `Cabeça & Rosto/Tipo de Corte de cabelo/Tipos cortes/Feminino/Corte feminino 1 - Corte 1.jpeg` | Contexto do módulo preservado. Nenhuma mecha foi redesenhada nesta etapa. |

As referências orientam a forma, não fornecem medidas calibradas. Os valores abaixo são escolhas de modelagem deste ensaio; não foram extraídos como cotas das imagens. Olhos, nariz, boca, sobrancelhas e orelhas continuam fora da fabricação.

## Escolhas e parâmetros relacionados

A correção usa um campo contínuo de deslocamentos na malha existente. A largura em cada faixa se relaciona à largura anterior da mesma faixa, e a elevação do queixo ao intervalo vertical entre a linha orbital de trabalho e o queixo. Assim, a altura total de 24 cm não determina o formato desejado.

| Controle | Escolha aplicada | Relação que deve ser preservada |
|---|---|---|
| Altura inferior do rosto | Queixo elevado 14 mm, equivalente a 12,7% do intervalo orbital–queixo anterior de 110 mm. Efeito diminui progressivamente até z = 0,150 m. | Encurtamento, largura mandibular e arredondamento do queixo devem variar juntos; mover só o queixo acentuaria uma ponta ou um degrau. |
| Largura inferior | Fatores nominais: 1,24 na faixa do queixo, 1,18 na mandíbula baixa, 1,10 na mandíbula intermediária, 1,055 na bochecha inferior, decrescendo até 1 no alto. | As larguras formam uma curva contínua. São intensidades máximas antes das máscaras de proteção, não aumentos uniformes da largura total. |
| Pescoço | Fator nominal de largura até 1,19 na transição; preenchimento anterior até 4 mm. Corte inferior permanece em z = 0. | Largura e profundidade do pescoço acompanham a nova mandíbula. O corte inferior e a origem comuns ficam fixos. O pescoço não foi encurtado por escala independente. |
| Profundidade do queixo | Componente de recuo de até 2 mm, combinado com o preenchimento do pescoço. | Perfil do queixo e superfície sob a mandíbula precisam ser avaliados juntos. O deslocamento líquido do marco central em Y é aproximadamente −0,87 mm, pois os dois campos se sobrepõem. |
| Fronteiras editadas | Transição suave de influência em 10 mm junto aos vértices protegidos. Congelamento a até 6 mm do cabelo, liberando gradualmente até 18 mm. | Deslocamentos faciais ficam subordinados à preservação do contato craniano; esses números são máscaras de edição, não novas folgas de encaixe. |
| Escala | Metros; sem transformação global. Altura queixo–crânio resultante: **0,226 m**. | Os 0,24 m anteriores são referência provisória. Não compensar o encurtamento local escalando a cabeça ou reposicionando o cabelo. |

Crânio superior, grupo de couro cabeludo, interfaces orbital/nasal e corte inferior do pescoço foram protegidos. O vértice do topo continua em z = 0,305 m; o marco do queixo passou de z = 0,065 para 0,079 m. A malha continua editável, com um novo grupo que registra a influência da revisão.

## Conferência e resultado

- 689 vértices deslocados; 2.012 vértices protegidos com deslocamento exatamente zero.
- Cabelo com posições de vértices, topologia, atribuição de materiais e transformação iguais às da versão anterior. Seus materiais foram reutilizados sem edição.
- Base continua com zero arestas abertas e zero arestas não manifold.
- Zero interseções entre triângulos da base e do cabelo, tanto na fonte quanto nos GLBs reimportados.
- GLBs individuais e montagem reimportados com as mesmas posições, triângulos e materiais; a montagem contém exatamente os dois módulos. A fonte continua única para a versão revisada.
- Versão anterior preservada no arquivo original, na cópia binária e na cena de comparação. Os arquivos originais foram conferidos por hash após a exportação.

Visualmente, o queixo está menos pontudo e o trecho inferior mais compacto; mandíbula e pescoço têm maior largura. O resultado aparece mais claramente na base isolada e na frente. O cabelo preservado continua ocultando parte da mudança nas vistas montadas.

## Problemas que permanecem

O perfil ainda mostra uma dobra/sombra marcada sob o queixo e a transição lateral da mandíbula pode ganhar continuidade. A nova posição do queixo aumenta o trecho de pescoço exposto; o ganho de largura reduz o aspecto estreito, mas a relação visual deve ser julgada na comparação. A superfície facial continua lisa e as órbitas mantêm as irregularidades anteriores, pois esta revisão não alterou essas regiões. O volume e o desenho das mechas continuam divergentes das referências e não foram corrigidos nesta etapa.

Na primeira tentativa de exportação desta revisão, a seleção de outras cenas incluiu objetos de comparação. A validação falhou; a exportação foi restringida à cena ativa e passou a exigir exatamente dois módulos após a reimportação. Os GLBs entregues são os arquivos corrigidos.

Não houve aplicação desta revisão ao código do 3DC, novas bases, novos componentes faciais ou segunda alteração de cabelo. Esta entrega encerra a revisão limitada para avaliação conjunta.
