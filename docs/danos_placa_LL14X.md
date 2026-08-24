# Danos e estado atual — placa de potência Electrolux LL14X

**PCB:** WQP12-7601S.D.1-1 V1.1 (2021-01-04-F), da mesma família da placa Continental LC14S.

**Causa relatada:** curto-circuito provocado por um inseto sobre trilhas ou ilhas da
entrada de rede.

Este documento separa o estado inicial registrado nas fotografias do que foi
confirmado posteriormente por inspeção, limpeza e medições. As imagens abaixo foram
feitas antes da remoção da carbonização:

- [`PXL_20260823_033906993.jpg`](../imagens/originais/PXL_20260823_033906993.jpg) — face de solda;
- [`PXL_20260823_033933343.jpg`](../imagens/originais/PXL_20260823_033933343.jpg) — face de componentes;
- [`placa Continental LC14S`](../imagens/referencias/D_NQ_NP_2X_771331-MLB103020104988_012026-F-placa-potencia-para-lava-loucas-continental-lc14s-original.webp) — referência visual íntegra.

As leituras completas estão em
[`medicoes_diagnostico_LL14X.md`](medicoes_diagnostico_LL14X.md).

## 1. Estado inicial registrado nas fotos

### 1.1 Face de solda

O dano principal concentrava-se na área de alta tensão entre os pontos marcados
**IN**, o conjunto R1/R2/C2 e a região do resistor R3. Nas fotos anteriores à limpeza
eram visíveis:

- substrato enegrecido e fibra exposta;
- máscara de solda queimada ou descolada;
- cobre exposto e oxidado;
- material carbonizado sobre a ranhura de isolamento;
- sinais de aquecimento nas ilhas **IN**;
- destruição térmica de R3, originalmente marcado **33R0** (33 Ω);
- dano na trilha entre o DRAIN de IC1 e um terminal do primário de T1.

As fotografias não permitem atribuir com segurança a R4, C4 ou ZD1 os resíduos que
apareciam junto à área queimada. Esses componentes ou designadores não devem ser
considerados destruídos apenas pela interpretação visual das imagens antigas.

R1, R2 e C2 apareciam presentes na borda da área afetada. Não foi identificado outro
ponto evidente de carbonização no restante da face de solda.

### 1.2 Face de componentes

- **ZR1:** o disco e seu revestimento aparecem íntegros, sem ruptura, lasca ou material
  interno exposto. A sobreposição de outro elemento e a iluminação da foto não são
  danos no encapsulamento.
- **FUSE1 e FUSE2:** não apresentam queima ou rachadura externa visível.
- **IC1 (LNK3604P):** o corpo não aparece trincado. O escurecimento da placa entre IC1
  e T1 era compatível com o dano existente na face oposta, mas não comprovava falha
  interna do CI.
- **D1 e D2:** sem ruptura visual; um terminal de D2 estava dentro da região alcançada
  pela carbonização.
- **C1, E1 e E2:** sem trinca, estufamento ou vazamento visível.
- **T1, D3, D7, IC2, IC3, E3 e E4:** sem dano externo evidente.

## 2. Danos confirmados

### 2.1 R3 aberto e removido

R3 carbonizou, passou a medir circuito aberto e foi removido. Seu valor original é
**33 Ω**, conforme a marcação **33R0**. O componente substituto ainda não foi comprado;
além da resistência e do encapsulamento, precisam ser confirmadas potência e classe
de segurança apropriadas para a função na entrada da fonte.

### 2.2 Substrato e cobre danificados

A carbonização atingiu o substrato e a máscara de solda. Toda a carbonização visível
já foi removida, e a região foi planificada para a reconstrução. Essa intervenção
removeu o caminho condutivo de carvão visível, mas deixou perda de material, de cobre
e de resistência mecânica local.

### 2.3 Conexão DRAIN–T1 interrompida

A trilha entre o DRAIN de IC1 e o terminal correspondente do primário de T1
carbonizou e foi removida. A ligação permanece deliberadamente aberta até ser
reconstruída; a medição de continuidade confirma circuito aberto nesse trajeto.

### 2.4 Itens sem dano confirmado

- Não há evidência visual de ruptura do encapsulamento de **ZR1**.
- Não foi confirmado que R4, C4 ou ZD1 tenham sido destruídos.
- Não foi detectado outro ponto de carbonização na placa pelas fotografias disponíveis.

## 3. Triagem elétrica após a limpeza

As medições foram feitas com a placa desenergizada e, salvo indicação contrária, com
os componentes instalados. O multímetro apresenta aproximadamente 0,6 Ω com as pontas
em curto; por isso, leituras baixas são valores brutos e aproximados.

| Item | Resultado observado | Conclusão limitada da triagem |
|---|---:|---|
| FUSE1 | 0,6 Ω | continuidade confirmada |
| FUSE2 | 0,6 Ω | continuidade confirmada |
| DB1 | quatro junções em torno de 480–511 mV | sem curto ou abertura evidente |
| D1 | 493 mV / OL | comportamento unidirecional |
| D2 | 498 mV / OL | comportamento unidirecional apesar da exposição ao calor |
| D3 | 452 mV / OL | comportamento unidirecional |
| D7 | 242 mV em um sentido; 1749 mV no outro | sem curto; leitura reversa influenciada pelo circuito |
| IC1, DRAIN–SOURCE | 424 mV / OL | sem curto estático detectável |
| T1, primário | 5,4 Ω | enrolamento contínuo |
| T1, secundário | 0,9 Ω | enrolamento contínuo |
| T1, primário–secundário | OL na escala de 2 MΩ | sem fuga detectável nessa escala |
| E1–E4 | respostas transitórias e assimétricas | sem curto estático evidente em circuito |
| IC2, PC817 | junções sem curto | funcionamento e CTR não comprovados |
| IC3, TL431C | terminais sem curto | regulação não comprovada |

Esses resultados são favoráveis apenas como triagem estática. Eles não comprovam
isolamento na tensão de trabalho, capacitância, ESR, atuação de ZR1, funcionamento do
optoacoplador ou regulação da fonte.

## 4. Estado atual da reconstrução

Trabalho já realizado:

- R3 queimado removido;
- toda a carbonização visível removida;
- região afetada planificada;
- trecho danificado da trilha DRAIN–T1 removido;
- continuidade e ausência de curtos evidentes verificadas nos principais componentes.

Trabalho ainda pendente:

- identificar e comprar um R3 de 33 Ω com dimensões, potência e características de
  segurança adequadas;
- reconstruir mecanicamente a área, considerando o uso planejado de resina epóxi
  **Araldite Hobby 10 min**;
- reconstruir a conexão DRAIN–T1 com condutor e isolamento apropriados para o primário;
- conferir distâncias de escoamento, separação da baixa tensão e resistência de
  isolamento depois do reparo;
- repetir as verificações estáticas antes de qualquer energização.

## 5. Interpretação atual do evento

O cenário compatível com as evidências é um arco iniciado pelo inseto na zona ligada
à rede, seguido de carbonização do substrato. O carvão formou ou agravou um caminho
condutivo, R3 abriu e a trilha de comutação entre IC1 e T1 foi danificada. A sequência
temporal exata entre a abertura de R3 e a destruição da trilha não pode ser determinada
pelas fotos.

Até o momento, a triagem não encontrou curto estático em DB1, IC1 ou nos diodos, nem
interrupção nos enrolamentos de T1. Isso reduz a evidência de falhas adicionais, mas
não demonstra funcionamento sob tensão.

## 6. Restrição de segurança

A resina epóxi de uso geral não deve ser presumida como isolante certificado para a
rede sem dados de tensão, temperatura, resistência a arco e comportamento antichama.
Como não há transformador de isolamento nem sonda diferencial de alta tensão, o
osciloscópio comum com sonda ×10 não deve ser conectado ao primário energizado. A placa
não deve ser energizada antes da conclusão da reconstrução e de uma estratégia segura
de limitação e isolamento. Se as distâncias elétricas e a resistência mecânica não
puderem ser restabelecidas de forma confiável, a placa deverá ser substituída.
