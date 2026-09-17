# Piloto feminino 01 — resultado e problemas

17/09/2026 · Blender 5.2.1 LTS · somente base feminina 1 + Corte Feminino 1.

## Entrega

- [Cena mestre editável](piloto-feminino-01.blend)
- [Base feminina 1](base-feminina-01.glb)
- [Corte Feminino 1](corte-feminino-01.glb)
- [Montagem dos mesmos módulos](montagem-feminina-01.glb)
- [Quatro vistas dos GLBs reimportados](imagens/quatro_vistas.png)
- [Módulos isolados](imagens/modulos_separados.png)
- [Perfil oposto adicional](imagens/perfil_oposto.png)
- [Verificação numérica](verificacao/reimportacao.json)

As pranchas organizam renders sem retoque. A cena mestre contém dois objetos de malha: `Base_Feminina_01` e `Corte_Feminino_01`, sob `RCL_HEAD_ROOT`. Os três GLBs derivam desses mesmos objetos. Luzes e câmera não foram exportadas.

## Decisões implementadas

Pescoço incluído, escala em metros e altura de 0,24 m entre queixo e topo do crânio. A medida armazenada é 0,2400000095 m, por precisão de ponto flutuante. Queixo em z = 0,065 m; crânio em z = 0,305 m; origem no centro do corte inferior do pescoço, z = 0. Frente em -Y, +Z para cima.

Órbitas são cavidades provisórias, sem olhos. A região nasal é uma superfície receptora de baixo relevo, sem nariz. Grupos de vértices `INTERFACE_ORBITAL_L_PROVISORIA`, `INTERFACE_ORBITAL_R_PROVISORIA` e `INTERFACE_NASAL_PROVISORIA` permitem editar essas regiões. L/R seguem o personagem; L fica em +X.

Não foram fabricados sobrancelhas, boca, orelhas, barba ou corpo. O cabelo possui calota com espessura e 36 mechas facetadas, cada qual com grupo de vértices, reunidas em um objeto. Há sobreposição intencional entre mechas e calota; o módulo não é um sólido único soldado.

## Referências consultadas

Originais localizados pelo inventário JSON, abertos durante o trabalho e incorporados ao .blend:

- R076: `base 1 feminino.jpeg` — silhueta, crânio, mandíbula e pescoço.
- R052: `Corte feminino 1 - Corte 1.jpeg` — mechas largas, franja diagonal longa e pontas.
- R088: `rosto 1 + cabelo 1.jpeg` — relação entre os dois módulos.
- R049: `Rosto Geral Feminino.jpeg` — perfil, três quartos, costas e decomposição; reaberta na revisão da nuca.
- R099: `FemaleExemple.jpeg` — nuca e pescoço como parte da cabeça.

Os caminhos completos estão no [inventário](../../docs/referencias-rcl/Inventario_completo_referencias_RCL.json); os registros relevantes da análise foram relidos. As vistas não são ortográficas calibradas. O “perfil esquerdo” feminino é três quartos.

## Reimportação e encaixe

Os arquivos separados foram reimportados na cena `RCL_QA_GLB_SEPARADOS`; a montagem, em `RCL_QA_GLB_MONTAGEM`. Essas cenas são evidência de reimportação, não personagens modelados independentemente. A cena inicial do Blender foi preservada.

| Verificação | Base | Cabelo |
|---|---:|---:|
| Vértices na fonte | 2.961 | 2.962 |
| Triângulos na fonte e reimportados | 5.918 | 5.776 |
| Maior diferença entre posições de origem e reimportadas | 0 m | 0 m |
| Geometria dos triângulos, tolerância 1 µm | Igual | Igual |
| Cor base, rugosidade e metalicidade | Preservadas | Preservadas |
| Arestas abertas / não manifold na fonte | 0 / 0 | 0 / 0 |

Os resultados coincidem nos GLBs separados e no montado. A checagem BVH retornou **zero interseções entre triângulos da base e do cabelo** em ambos os conjuntos reimportados. Isso não certifica ausência de interseções internas entre as mechas.

O cabelo reimportado tem 13.120 vértices devido à separação de normais/materiais; posições e 5.776 triângulos foram preservados. Total da montagem: 11.694 triângulos. Hashes e resultados detalhados estão no JSON de verificação.

A inspeção visual incluiu frente, ambos os perfis, três quartos, costas e os módulos isolados. O aplicativo 3DC não foi alterado nem usado como evidência deste teste.

## Problemas encontrados

| Problema | Tratamento e situação |
|---|---|
| Órbitas iniciais quadradas | Remodeladas como depressões arredondadas; bordas ainda apresentam irregularidades de tesselação e precisam de refinamento |
| Transição dura entre queixo e pescoço | Curvatura ajustada e suavização localizada; permanece uma transição de sombreamento perceptível sob o queixo |
| Borda reta da calota e nuca descoberta | Contorno inferior variado e mechas posteriores prolongadas, com apoio na referência traseira |
| Raízes afastadas da calota | Reposicionadas sobre sua superfície; pontas livres e pequenas separações entre mechas permanecem no penteado |
| Interpenetração oculta da calota | 41 centroides internos penetravam até cerca de 0,526 mm; superfície interna afastada 3 mm. Checagem final cabelo/base: zero interseções |
| Fidelidade visual ainda parcial | Franja longa diagonal e mechas facetadas representadas; distribuição posterior mais vertical/regular que a referência e silhueta facial ainda aproximada |

## Limites e edição

Esta entrega é um protótipo de forma e montagem. O teste de reimportação passou; isso não equivale a aprovação de fidelidade visual final. As interfaces orbital e nasal são regiões editáveis, sem encaixe universal certificado ou bordas definitivas para outros módulos.

A base tem sombreamento mais suave que o cabelo. Planos faciais, transição do pescoço e distribuição das mechas ainda admitem refinamento. Materiais usam cores sólidas; não há UVs de produção, texturas ou rig. Superfícies internas e profundidades não documentadas são estimativas.

Não foram produzidas outras bases nem testados olhos, narizes, outros cabelos, corpo ou animação.

O .blend é a fonte editável. Os scripts em `scripts/` registram construção, correções, exportação e pranchas. Eles se destinam à construção em uma nova cena de piloto; não devem ser reexecutados indiscriminadamente sobre o arquivo final. Renders antigos com prefixo `revisao` são histórico, não as imagens finais.
