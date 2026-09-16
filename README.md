# 3DC — Criador de personagens do Real Car Lifestyle

O 3DC será o protótipo do menu de criação de personagens e o gerador de GLB do jogo **Real Car Lifestyle**, com evolução para randomização e produção dos 50 personagens e 200 NPCs da cidade.

A visão, o escopo inicial e as etapas futuras estão em [Visão do 3DC para Real Car Lifestyle](VISAO_3DC_REAL_CAR_LIFESTYLE.md).

## Implementação atual — bases faciais + cabelo único

As instruções abaixo descrevem a versão atual: ela recebe GLB, alterna as bases e exporta a combinação com um cabelo. A criação da geometria e o randomizador ainda não estão implementados. O primeiro experimento terá somente bases de rosto e um cabelo fixo, sem olhos, nariz ou outros módulos faciais.

Nesta etapa, dois slots:

| Slot | Conteúdo |
| --- | --- |
| **Base feminina** | as 5 bases (cabeça/rosto, sem cabelo) |
| **Cabelo** | o "Corte feminino 1" |

Sem editor de rosto: nada de olhos, boca, nariz, orelhas, morph targets ou blendshapes.
Sem ajuste de posição/rotação/escala — o encaixe vem do Blender.

---

## Como rodar

```powershell
npm install
npm run dev
```

URL local: **http://localhost:5173/**

| Comando | O que faz |
| --- | --- |
| `npm run typecheck` | `tsc --noEmit` |
| `npm run build` | typecheck + build de produção em `dist/` |
| `npm run preview` | serve o `dist/` |
| `npm run validate:glb -- <arquivo.glb>` | roda o **Khronos glTF Validator** no arquivo |

Página auxiliar (só no `npm run dev`): **http://localhost:5173/verify.html** abre um `.glb`
em cena limpa, sem a biblioteca, e mostra malhas, triângulos, materiais e caixa envolvente.

---

## Como importar os 6 arquivos

1. Abra a URL local. Com a biblioteca vazia o visualizador explica o que falta.
2. No slot **Base feminina**, arraste os 5 arquivos (`base 1 feminino.glb` … `base 5 feminino.glb`)
   de uma vez sobre a área tracejada, ou clique e selecione os 5.
3. No slot **Cabelo**, arraste `Corte feminino 1.glb`.
4. A primeira peça de cada slot entra montada sozinha. Use **◀ ▶** ou as **setas do teclado**
   para trocar a base; o cabelo continua montado e imóvel.
5. **Exportar GLB** grava base + cabelo em um único `.glb` binário.

A ordem do ◀ ▶ segue o nome do arquivo com ordenação numérica ("base 2" antes de "base 10").
A base escolhida é lembrada ao recarregar a página.

---

## Versões fixadas

Dependências pinadas (sem `^`), com `package-lock.json` versionado.

| Pacote | Versão |
| --- | --- |
| three | 0.186.0 |
| @types/three | 0.186.0 |
| react / react-dom | 19.3.0 |
| vite | 8.3.0 |
| @vitejs/plugin-react | 6.1.1 |
| typescript | 5.9.3 |
| idb | 8.0.3 |
| gltf-validator (dev) | 2.0.0-dev.3.10 |

`GLTFLoader` e `GLTFExporter` vêm do próprio pacote `three`, então loader, exporter e core
são sempre a mesma versão.

---

## Armazenamento

Peças e seleção ficam em **IndexedDB** (banco `montador-3dc`, versão 2), neste navegador e
neste computador. Os binários ficam em um store separado (`blobs`), então listar a biblioteca
não desserializa ArrayBuffers. Nada de modelo vai para `localStorage`; não há backend.

Limpar os dados do site apaga a biblioteca — seus arquivos do Blender continuam sendo a cópia
de segurança. Em *Armazenamento* há uso/cota e o botão para pedir persistência ao navegador.

A versão 2 do banco migra bases de dados antigas: remove as categorias editáveis, os transforms
por slot e qualquer peça que não seja base nem cabelo.

---

## Decisões de comportamento

- **Nada é normalizado.** Sem centralização, sem normalização de escala, sem união de malhas.
- **Trocas rápidas.** Cada slot tem um contador monotônico; toda etapa assíncrona confere se
  ainda é a seleção corrente, então uma base antiga que termine de carregar depois é descartada.
- **Recursos compartilhados.** Cada arquivo é parseado uma vez e guardado em cache; cada uso é
  um clone que compartilha geometrias, materiais e texturas. Trocar de base só desanexa o objeto;
  `dispose()` acontece apenas quando a peça é removida da biblioteca.
- **Importação validada.** Todo arquivo passa por conferência do container GLB e por um parse
  completo antes de entrar; arquivo inválido não é gravado e o motivo aparece na tela.
- **Exportação.** O grupo do personagem é movido para uma `Scene` temporária, então grade, luzes
  e câmera nunca entram no `.glb`. O resultado é conferido byte a byte (magic `glTF`, versão 2,
  tamanho declarado) antes de virar download — não há JSON renomeado para `.glb`.

---

## Limitações verificadas desta versão

Lidas no código do `GLTFExporter`/`GLTFLoader` do three 0.186.0 instalado. As mesmas notas
aparecem no diálogo de exportação.

- **Animação não faz parte desta versão.** Clipes presentes nos arquivos não são tocados nem
  exportados; se houver algum, o relatório avisa antes de exportar.
- **Materiais.** Só `MeshStandardMaterial` / `MeshPhysicalMaterial` / `MeshBasicMaterial` têm
  correspondência direta em glTF; outros são aproximados e `ShaderMaterial` é ignorado.
- **Texturas.** Reescritas via `canvas`. Comprimidas (KTX2/Basis, DDS) fazem o exporter lançar
  *"Invalid image type"* e `DataTexture` só é aceita em RGBA — esses casos são bloqueados antes.
- **Skinning.** `SkinnedMesh` só exporta certo com o esqueleto dentro do grafo exportado.
- **Morph targets.** Apenas `POSITION` e `NORMAL`.
- **Objetos ocultos** não são exportados (`onlyVisible: true`).
- **Resolução de textura** não é reduzida, então o `.glb` pode ficar grande.
- **Nomes** podem ganhar sufixo para ficarem únicos (`Personagem` → `Personagem_1`).
- **Compatibilidade com Unity não foi testada** e portanto não é afirmada.

---

## Verificação feita no navegador

Com 3 bases + 1 cabelo importados (usando um `.glb` válido como arquivo de teste):

- ◀ ▶ e as setas do teclado percorrem as bases nos dois sentidos, com volta no fim da lista,
  e o slot de cabelo permanece montado e selecionado.
- Recarregar a página restaura a base escolhida e o cabelo.
- O relatório de exportação mostra exatamente as duas peças montadas.
- `npm run build` conclui sem erro de TypeScript.
- Validação de arquivo: `npm run validate:glb -- artifacts/personagem-fixtures.glb` reportou
  0 erros e 0 avisos no Khronos glTF Validator, sem recursos externos.

Não verificado: importação na Unity e os arquivos reais de produção (bases e corte do Blender).
