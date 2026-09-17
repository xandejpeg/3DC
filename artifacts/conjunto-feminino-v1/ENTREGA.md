# Conjunto feminino v1 — 17/09/2026

Cinco bases separadas + um único Corte Feminino 1, disponíveis automaticamente no seletor. [Comparação](comparacao.png) · [Blender](conjunto-feminino-v1.blend) · [GLBs incluídos](../../public/models/rcl-feminino-v1/).

Referências consultadas: bases R076–R080 e montagens R088–R092 do inventário. Identidades procuradas: 1 suave, 2 mandíbula mais angular/larga, 3 arredondada/curta, 4 alongada/estreita, 5 maçãs largas e queixo fino. Reutilizada a cena R02; órbitas provisórias e pescoço receberam suavização comum. Nenhum componente facial foi acrescentado.

Largura inferior, comprimento do queixo e profundidade das bochechas variam por campos suaves na malha. Crânio de contato comum e cabelo permanecem fixos; a influência das alterações diminui perto do cabelo. Não se impôs altura de 24 cm. Parâmetros finais em `parametros.json`; scripts de geração e entrega em `scripts/rcl-bases.py` e `scripts/rcl-exportar.py`, na raiz do projeto.

Funciona: cinco trocas usando a mesma instância de cabelo; GLBs separados; quatro vistas; prévia da base isolada; exportação da montagem. As peças do conjunto são servidas com o aplicativo; importações anteriores e suas seleções válidas são preservadas.

Verificado: dez reimportações no Blender (cinco pares separados e cinco montagens), igualdade geométrica/material, superfície craniana comum e zero interseções base/cabelo. Os 11 GLBs de origem/montagem passaram no Khronos com zero erros e avisos. `npm run build` passou. `npm run test:rcl` conferiu, sem interface gráfica, as cinco trocas usando `SceneManager` e `GLTFExporter` reais, cabelo com a mesma identidade/transformação, prévia isolada e reimportação dos arquivos exportados pelo app. Resultados em `validacao.json`, `khronos.txt` e `exportacoes-app/resultado.json`.

Limitações: semelhança visual ainda aproximada; cabelo pesado e vertical nas laterais, órbitas pouco definidas, alguns planos e transições de mandíbula/pescoço precisam de acabamento. As bases 2 e 3 são mais difíceis de distinguir com o cabelo montado. Não há validação de encaixe com olhos/narizes nem rig. O build avisa sobre o tamanho do bundle Three.js.

A conferência por cliques no navegador não foi concluída: o Computer Use interrompeu o acesso por não identificar com segurança a URL. Isso não foi contornado. Servidor e arquivos foram conferidos por HTTP, e a integração de troca/exportação por teste de código.

Próximo alinhamento de produto: avaliar se a diferença visual entre os cinco formatos é suficiente para o seletor; decidir esse ponto antes de expandir as categorias.
