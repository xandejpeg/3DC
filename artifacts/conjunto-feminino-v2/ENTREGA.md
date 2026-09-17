# Retomada facial — 17/09/2026

Reaproveitados: cinco bases v1, Corte Feminino 1, cena/iluminação, seletor e código de exportação. Não havia componentes faciais novos salvos após a interrupção. A v1 continua intacta.

Entregues: cinco bases com sobrancelhas/boca/orelhas fixas, um par de Olho 1 e um Nariz 1. Quatro slots no seletor; trocar a base mantém as instâncias e transformações de cabelo, olhos e nariz. A escolha anterior de base v1 migra para a correspondente v2. Os arquivos importados pelo usuário são preservados.

- [Cena Blender](conjunto-feminino-v2.blend)
- [Comparação das cinco bases](comparacao.png) e [antes/depois da base 1](antes-depois.png)
- [Módulos GLB](../../public/models/rcl-feminino-v2/) e [cinco montagens](montagens/)
- Vistas reimportadas em `previas/`: frente, sem cabelo, três quartos; perfil e costas da base 1.

Verificado: dez reimportações no Blender (módulos separados e montagem de cada base), geometria e materiais preservados; bordas de pele coincidentes, zero interseções base/cabelo. O arquivo do cabelo conserva o SHA-256 da v1. O teste com SceneManager/GLTFExporter reais troca cinco bases sem recriar os módulos compartilhados e reimporta cada exportação com geometria/materiais iguais. Build aprovado; Khronos sem erros ou avisos nos módulos e montagens. Teste automatizado da interface por cliques não realizado nesta retomada.

Limites visuais: a franja herdada cobre mais o rosto e as orelhas que a referência; a transição inferior das pálpebras ainda produz sombra pesada e precisa de refinamento; o nariz permanece mais anguloso e a boca mais fina que a referência. As bases 2/3 ainda se distinguem menos com cabelo. As uniões são de objetos coincidentes, sem soldagem global; contato de orelhas/lábios com a base é sobreposição interna deliberada. Sem rig ou animação.

Problemas resolvidos nesta execução: faces dobradas na pálpebra foram substituídas por triangulação sem cruzamentos; a íris recebeu subdivisões radiais para acompanhar a esfera, evitando ficar escondida pela esclera. Falta de memória do Windows encerrou execuções iniciais e o Blender aberto durante uma tentativa de cópia da sessão; a produção continuou a partir da v1 salva, em segundo plano com dois threads. A tentativa de copiar a sessão aberta não chegou a gerar arquivo.

Decisão de produto para uma próxima etapa: abrir a franja para aproximar a visibilidade facial da referência. O cabelo foi preservado nesta retomada.
