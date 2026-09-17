# 3DC — Criador e gerador de personagens para Real Car Lifestyle

**Data:** 16 de setembro de 2026  
**Projeto:** 3DC  
**Jogo de destino:** Real Car Lifestyle (RCL)  
**Natureza deste documento:** visão e escopo definidos pelo criador do projeto. Descreve o que será construído e distingue essa intenção do que já existe no código.

## Atualização de direção — 17/09/2026

O projeto é o **3DC Lab v1**: laboratório que documenta a criação dos personagens e gerador v1 dos GLBs destinados ao jogo 3D Real Car Lifestyle. Referências, conceitos, escolhas de modelagem, scripts, cenas, imagens de revisão e verificações devem ser rastreáveis em commits, comentários de código e arquivos Markdown. O histórico faz parte do produto do laboratório.

O experimento inicial de base + cabelo avançou para cinco bases femininas + Corte 1 + Olho 1 + Nariz 1, com sobrancelhas, boca e orelhas fixas em cada base. Continua dentro da v1 do laboratório. Os nomes `conjunto-feminino-v1/v2` identificam revisões dos modelos. Corpo, rig, animação e randomização permanecem futuros; importação no jogo não foi comprovada.

As seções abaixo preservam a formulação inicial de 16/09/2026. As exclusões de olhos/nariz no **primeiro experimento** são históricas, não restrições do escopo atual. Estado vigente: [README](README.md), [processo](docs/PROCESSO_3DC_LAB_V1.md) e [contrato](docs/referencias-rcl/Contrato_pecas_interfaces_RCL.md).

## 1. Para que existe o 3DC

O **3DC será o protótipo do menu de criação de personagens do Real Car Lifestyle e também o gerador de personagens em GLB para o jogo**.

O projeto reúne usos que devem evoluir juntos:

1. **Criação e estudo do personagem:** experimentar bases, trocar componentes e avaliar o resultado visual. Esse trabalho servirá de base para o menu de criação do jogo.
2. **Produção de personagens:** gerar combinações utilizáveis e seus arquivos GLB. Futuramente, um randomizador usará os módulos para gerar a base dos **50 personagens e dos 200 NPCs da cidade**.
3. **Documentação do processo:** conservar o motivo de cada decisão, suas referências, a versão das peças e o resultado dos testes. O jogo deve receber arquivos acompanhados da sua origem e dos limites conhecidos.

Essas quantidades representam o objetivo informado para a produção. Os papéis dos 50 personagens, os critérios de distribuição e as regras de repetição do randomizador ainda não foram definidos.

As decisões faciais continuam em estudo. A proposta é **já começar a produzir os GLB, testá-los no 3DC e melhorar os modelos e o aplicativo durante esse processo**, sem esperar a definição de todo o personagem ou do corpo.

## 2. O que vamos construir primeiro

O primeiro experimento é deliberadamente pequeno:

> **Um único cabelo, mantido fixo, enquanto todas as bases de formato de rosto do conjunto em teste são alternadas. Sem olhos, sem nariz e sem outros módulos faciais nesta etapa.**

O usuário deve conseguir trocar a base e observar como o mesmo cabelo se comporta em cada rosto. O cabelo conserva sua identidade, posição, orientação e escala ao longo da troca. As bases precisam ser construídas de modo compatível com esse encaixe.

| Elemento | Nesta etapa |
|---|---|
| Formato de rosto | Várias bases, cada uma em seu GLB, alternadas uma por vez |
| Cabelo | Um único modelo GLB, mantido nas trocas |
| Olhos | Não incluir |
| Nariz | Não incluir |
| Outros módulos faciais | Não incluir agora |
| Corpo | Etapa posterior |
| Randomização da população | Objetivo futuro; não faz parte deste primeiro experimento |

O formato do rosto é a geometria da base. Ele não deve ser tratado como um rosto completo com todos os componentes já incorporados. A presença de olhos, nariz ou outros detalhes em uma imagem de referência não significa que devam ser modelados junto da base nesta etapa.

O conjunto de bases femininas e o Corte Feminino 1 descritos na implementação atual podem servir a esse primeiro teste. Esse recorte não limita a visão completa do 3DC a personagens femininos ou a um único cabelo.

## 3. O princípio de modularidade

Cada opção de componente será um **arquivo GLB independente**. Assim, poderemos trocar uma categoria sem precisar recriar o personagem inteiro.

| Categoria | Responsabilidade do módulo |
|---|---|
| Tipo/formato de rosto | Definir a forma da base facial |
| Cabelo | Definir o corte ou penteado |
| Olhos | Fornecer a opção de olhos, separada da base |
| Nariz | Fornecer a opção de nariz, separada da base |

Olhos e nariz estão nesta visão de expansão, mas ficam fora da implementação do primeiro experimento. A composição de outros elementos faciais será definida depois.

O objetivo é que **qualquer opção de uma categoria funcione com as opções das outras categorias**, formando combinações realmente utilizáveis. Isso exige modelar e testar as peças como partes de um mesmo sistema. Ter arquivos separados, por si só, não comprova compatibilidade.

Nas trocas, será necessário conferir:

- Escala, orientação e posicionamento coerentes entre os arquivos.
- Encaixes sem buracos, sobreposições visíveis ou interpenetrações inadequadas.
- Preservação da identidade de cada base e de cada componente.
- Continuidade visual suficiente para que a combinação seja percebida como um personagem.
- Preservação da combinação quando ela for exportada e reaberta em GLB.

Esses pontos são requisitos a desenvolver e validar. Não significam que as referências ou os arquivos atuais já atendam a todos eles.

## 4. O que significa gerar, mesclar e fundir

O resultado pretendido é que o 3DC permita **formar personagens a partir das opções disponíveis e gerar seus GLB**. A montagem e a exportação precisam fazer parte da evolução do projeto.

A maneira de criar a geometria de cada módulo ainda não está fechada: podemos produzir peças com o Blender e ferramentas assistidas por IA, desenvolver geração dentro do 3DC ou combinar esses caminhos. Este documento não decide essa arquitetura por antecipação.

Da mesma forma, “mesclar e fundir” expressa a necessidade de as peças funcionarem juntas. Ainda será preciso decidir quando isso significa:

- Montar objetos separados com encaixe e aparência contínuos.
- Exportar a montagem inteira em um GLB, preservando os objetos internos.
- Unir ou fundir efetivamente as malhas.

Exportar vários objetos no mesmo arquivo não equivale automaticamente a fundir sua geometria. A solução deverá ser escolhida a partir do resultado visual e das necessidades do jogo. Os módulos de origem devem continuar disponíveis para permitir outras combinações.

## 5. Como o trabalho evolui

| Etapa | Resultado esperado |
|---|---|
| **1 — Bases + cabelo único** | Gerar os primeiros GLB, alternar as bases e validar o mesmo cabelo em todas |
| **2 — Componentes faciais** | Introduzir olhos, narizes e outras opções conforme forem definidos; testar as combinações entre categorias |
| **3 — Corpo** | Estender o sistema de peças compatíveis ao corpo, após consolidar o experimento facial |
| **4 — Randomização e produção** | Usar os módulos para gerar personagens e apoiar a produção dos 50 personagens e 200 NPCs |

Essa ordem descreve a progressão de escopo, não um cronograma. O menu e o processo de produção serão refinados com os testes reais.

## 6. Critérios para considerar o primeiro experimento funcionando

1. Cada base do conjunto em teste está disponível em um GLB próprio, sem os módulos faciais que ficaram fora desta etapa.
2. Existe um único GLB de cabelo, usado em todas as trocas.
3. A interface alterna a base e mantém o mesmo cabelo montado.
4. Cada combinação pode ser examinada de frente, de perfil e por trás para conferir forma e encaixe.
5. Os problemas encontrados orientam correções nos GLB e, quando necessário, melhorias no 3DC.
6. A combinação escolhida pode ser exportada e reaberta, preservando as peças, o posicionamento e os materiais esperados.

Não considerar esse teste concluído apenas porque os arquivos carregam. O encaixe entre o cabelo e cada base precisa ser verificado visualmente.

## 7. Situação atual e direção do projeto

Na leitura do código em 16/09/2026, o 3DC é um aplicativo web em React e Three.js. Ele já contém importação de GLB, armazenamento local da biblioteca, alternância de bases, um slot de cabelo e exportação da combinação.

O código inspecionado ainda não implementa criação de geometria a partir das referências, um randomizador de personagens ou geração em lote dos 50 personagens e 200 NPCs. Essas capacidades pertencem à direção de evolução descrita aqui.

A descrição antiga do README, voltada a um alternador que recebe peças do Blender, retrata o recorte implementado naquele momento. **Ela não define o limite final do projeto.** A visão atual é um criador e gerador de personagens para o Real Car Lifestyle, começando pelo experimento de bases faciais com cabelo único.

Este documento orienta a continuidade do trabalho. Nesta entrega, foram documentados os objetivos; nenhuma das funcionalidades futuras foi implementada.
