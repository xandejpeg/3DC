# 17/09/2026 — Primeiro conjunto modular documentado

**Produto:** 3DC Lab v1. **Assets atuais:** revisão `rcl-female-v2`. **Destino:** personagens do jogo 3D Real Car Lifestyle.

Este registro reúne trabalho realizado antes do primeiro commit completo do laboratório. As etapas abaixo são checkpoints de arquivos, não uma alegação de que já existiam commits separados para cada etapa.

## Evolução preservada

| Etapa | Resultado e evidência |
| --- | --- |
| Catálogo | Análise recebida de 100 imagens; contrato e inconsistências documentados; [originais arquivados com hashes](../referencias-rcl/originais/README.md) |
| Piloto | Base feminina 1 + Corte 1, pescoço incluído; [cena, scripts e verificações](../../artifacts/piloto-feminino-01/) |
| Revisão de proporções | Face inferior e pescoço ajustados, cabelo preservado; [antes/depois R02](../../artifacts/piloto-feminino-01/revisao-rosto-02/imagens/antes_depois_resumo.png) |
| Cinco bases | Formas distintas com um cabelo compartilhado; [revisão de modelos 1](../../artifacts/conjunto-feminino-v1/ENTREGA.md) |
| Retomada facial | Olho 1, Nariz 1, sobrancelhas, boca e orelhas; [revisão de modelos 2](../../artifacts/conjunto-feminino-v2/ENTREGA.md) |
| Registro no Git | Código, referências, cenas, GLBs, comparações, parâmetros e validações passam a ser entregas versionadas; produto identificado como Lab v1 |

## Escolhas que orientam o próximo trabalho

Preservar a identidade dos rostos e o cabelo compartilhado. Padronizar regiões de contato, sem impor o mesmo volume à face inteira. Usar exatamente os módulos da cena mestre na montagem e na exportação. Os 24 cm eram uma convenção inicial e não restringem as proporções atuais.

O Olho 1 inclui pálpebras e pele; o Nariz 1 substitui uma região da base com borda correspondente. Sobrancelhas, boca e orelhas são fixas por base neste protótipo. A boca acompanha a forma inferior; olho, nariz e cabelo permanecem compartilhados. O catálogo feminino mantém cinco bases; a legenda isolada que cita base 6 continua uma inconsistência.

## Problemas encontrados e tratamento

- Topologia inicial da pálpebra apresentou cruzamentos e vazamentos: triangulação entre contornos refeita.
- Disco de íris entrava na esclera: subdivisões radiais passaram a acompanhar a esfera.
- Falta de memória do Windows encerrou execuções e o Blender aberto durante uma tentativa de copiar a sessão. Essa cópia não chegou a ser salva. A retomada usou o conjunto anterior salvo e execuções em segundo plano com dois threads.
- A franja herdada cobre mais o rosto que nas referências. Foi preservada nesta etapa; abrir a franja é uma decisão de aparência a alinhar.
- Pálpebra inferior, nariz e boca ainda precisam de refinamento visual. As bases 2/3 se diferenciam menos quando o cabelo está montado.

## Resultado verificável

Build aprovado; cinco trocas em teste de integração mantêm as instâncias de cabelo/olhos/nariz; dez reimportações no Blender preservam geometria/materiais e bordas de contato. Os 18 GLBs finais passaram no Khronos Validator sem erros/avisos. A auditoria atual por cliques e a integração na engine não foram realizadas.

![Comparação das cinco bases com componentes compartilhados](../../artifacts/conjunto-feminino-v2/comparacao.png)

[Antes/depois da base 1](../../artifacts/conjunto-feminino-v2/antes-depois.png) · [processo e scripts](../PROCESSO_3DC_LAB_V1.md) · [entrega ao jogo](../ENTREGA_GLB_JOGO.md).

O commit que introduz este registro é o checkpoint de publicação. Para localizar seu hash sem manter uma referência circular no arquivo: `git log --diff-filter=A --format="%h %s" -- docs/registros/2026-09-17-conjunto-feminino.md`.
