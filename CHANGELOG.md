# Histórico do 3DC Lab v1

## 17/09/2026 — Cortes femininos 2–12

- Onze novos cabelos GLB no catálogo existente, com cenas e progresso independentes por corte.
- 12 cabelos × 5 bases; trocas preservam rosto/cabelo selecionado, olhos, nariz e partes faciais fixas.
- Referências isoladas e montadas consultadas; modelagem por mechas, cachos e casca interna, com correções de têmporas/orelhas no cabelo.
- Onze reimportações Blender, 55 verificações de encaixe dos cabelos novos, 120 trocas no `SceneManager` real, build aprovado e 11 GLBs sem erros/avisos no Khronos Validator.
- Corte 1, bases, peças faciais e fluxo de exportação do app preservados.

Limites: formas ainda interpretadas, algumas mechas/cachos mais regulares que as referências, traseiras estimadas, cabelos cacheados densos e ausência de nova auditoria por cliques (navegador indisponível). [Registro e retomada](docs/registros/2026-09-17-cabelos-femininos.md).

## 17/09/2026 — Conjunto feminino e registro do processo

Este é o primeiro checkpoint completo do laboratório no Git. Ele reúne etapas realizadas antes deste commit; não simula commits retroativos para cada tentativa de modelagem.

- Cinco bases femininas compatíveis com um mesmo Corte Feminino 1; identidade facial concentrada em bochechas, mandíbula e queixo.
- Olho 1 em par e Nariz 1 como módulos GLB; sobrancelhas, boca e orelhas fixas dentro de cada base.
- Quatro slots no seletor; preservação das peças compartilhadas e migração da seleção do catálogo anterior; exportação da montagem para GLB.
- Cenas Blender do piloto, revisão do rosto e dois conjuntos; scripts, comparações, parâmetros e verificações preservados.
- Catálogo de 100 referências copiado sem alteração e conferido por SHA-256; índice portátil para consulta pelo GitHub.
- README, processo, entrega ao jogo e registro de etapa distinguem produto v1, revisão dos modelos e validações pendentes.
- Build aprovado, cinco trocas verificadas por integração, dez reimportações Blender e 18 GLBs sem erros/avisos no Khronos Validator.

Limites: conjunto estático, sem corpo/rig/animação/randomização; franja muito fechada, pálpebras com sombra pesada e nariz/boca ainda aproximados. Integração em engine e auditoria por cliques da interface atual pendentes. [Registro detalhado](docs/registros/2026-09-17-conjunto-feminino.md).
