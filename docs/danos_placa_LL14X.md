# Danos visíveis — placa de potência lava-louças Electrolux LL14X
**PCB: WQP12-7601S.D.1-1 V1.1 (2021-01-04-F)** — mesma família da placa Continental LC14S
Causa relatada: curto-circuito provocado por inseto sobre trilhas/pads da entrada de rede.

> **Nota de método:** “visível” descreve somente o que as imagens permitem afirmar.
> Identificações ou causas não legíveis estão marcadas como hipótese e precisam de
> continuidade elétrica, teste de componente ou foto macro para confirmação.

Fontes visuais usadas:
- [`PXL_20260823_033906993.jpg`](../imagens/originais/PXL_20260823_033906993.jpg) — face de solda, mesma orientação da referência íntegra;
- [`PXL_20260823_033933343.jpg`](../imagens/originais/PXL_20260823_033933343.jpg) — face de componentes, fotografada girada 180°;
- [`placa Continental LC14S`](../imagens/referencias/D_NQ_NP_2X_771331-MLB103020104988_012026-F-placa-potencia-para-lava-loucas-continental-lc14s-original.webp) — referência íntegra da face de solda.

A placa tem a seção de **fonte chaveada isolada** concentrada em uma das extremidades
(a direita na face de solda / a direita também na face de componentes girada). É nessa
extremidade que se concentram todos os danos. O restante da placa (lógica, relés,
buzzer, conectores) não apresenta dano visual.

---

## 1. Face de solda (lado dos SMD)

### 1.1 Cratera de arco elétrico (dano principal)
- **Localização:** entre o par de pads rotulados **"IN"** (furos de entrada da rede,
  vindos do conector CON1 da face oposta) e o grupo **R1/R2/C2**, imediatamente acima
  da serigrafia vertical **ZD1**, na borda direita da imagem, e à esquerda do
  triângulo de aviso de alta tensão serigrafado na
  máscara (zona de rede). Abaixo de **DB1** (ponte retificadora SMD) e do grupo
  **D11/D13**.
- **O que se vê:** cratera com ~5–8 mm de **carbonização do substrato** (fibra
  exposta e enegrecida), máscara de solda queimada/descolada num raio maior ao redor,
  e **cobre exposto oxidado** (tom dourado/castanho) nas bordas da cratera.
- **Componente SMD destruído no centro da cratera:** restam terminais e corpo
  carbonizado de um SMD. A comparação espacial sugere **C4 e/ou R4**, mas a foto não
  permite resolver inequivocamente o designador nem o valor.
- **Slot de isolamento carbonizado:** a ranhura de isolamento entre a zona de rede e o
  primário, que na placa íntegra está limpa, aparece **pretejada/parcialmente
  preenchida por carvão** — o arco saltou por cima dela.
- **Pads "IN" superaquecidos:** as duas ilhas de solda da entrada apresentam
  descoloração térmica (solda e máscara amarronzadas), coerente com condução de
  corrente de arco.
- Na placa íntegra essa região contém, de cima para baixo: **R4/C4**, o slot,
  **R3 (SMD "33R0" = 33 Ω)**, os pads **IN** e o grupo **R1 (104) / R2 (104) / C2**.
  **R3 está confirmado queimado e eletricamente aberto**. R4/C4 não são mais
  identificáveis na região destruída; **R1, R2 e C2** permanecem presentes e
  visualmente íntegros na borda superior da cratera.

### 1.2 Componentes próximos usados como referência espacial (íntegros)
- **R1, R2** — SMD "104" (100 kΩ), logo acima da cratera;
- **C2** — MLCC ao lado de R2;
- **D11, D13** — diodos SMD acima de R1/R2;
- **DB1** — ponte retificadora SMD de 4 terminais, canto superior direito da zona;
- **ZD1** — a serigrafia aparece verticalmente imediatamente à direita da cratera na
  foto da face de solda; componente/pads estão na região escurecida e não são
  identificáveis com segurança. Sua função não deve ser confundida com a referência
  principal da fonte, agora identificada como **IC3 = TL431C**;
- **C46, R11** e o indutor da rail de **5 V** (serigrafia "5V" com símbolo de bobina)
  à esquerda, já na zona de baixa tensão — sem dano.

Não há nenhum outro ponto de queima, trilha rompida ou componente estufado no
restante da face de solda.

---

## 2. Face de componentes (lado dos through-hole)

### 2.1 ZR1 — varistor de óxido metálico (visualmente íntegro)
- **Localização:** entre **FUSE2** (caixa marrom à esquerda) e **FUS1** (caixa marrom
  à direita, serigrafia "FUS T3.15AL/AC250V"), imediatamente acima de **C1**
  (capacitor X2 amarelo).
- **O que se vê:** disco amarelo com revestimento contínuo, sem fenda, lasca,
  estufamento ou material interno exposto identificável na foto. O elemento sobreposto
  e a iluminação não constituem ruptura do encapsulamento.
- A aparência íntegra não comprova as características elétricas do MOV; fuga e tensão
  de grampeamento exigem teste apropriado ou substituição preventiva por peça de
  especificação confirmada.

### 2.2 FUS1 / FUSE2 — fusíveis (caixas marrons retangulares)
- Sem rachadura ou queima externa visível. O estado elétrico de **FUS1
  (T3.15AL/250 V)** e FUSE2 não pode ser inferido visualmente; verificar continuidade
  com a placa desenergizada e os eletrolíticos descarregados.

### 2.3 IC1 — LNK3604P (DIP-8) e entorno
- **Fuligem/escurecimento** da placa entre **IC1** e **T1** (transformador EE16),
  junto aos pinos superiores do IC1 — indicação de aquecimento/sobretensão no CI
  chaveador. O corpo do CI não está trincado; somente uma medição pode determinar se
  o MOSFET interno está em curto, aberto ou funcional.
- **D2** (diodo axial sob IC1) e **D1** (diodo axial abaixo) sem dano visível.

### 2.4 Região de entrada (mesma zona da cratera, vista por cima)
- **RF1** (resistor axial pequeno, corpo cinza, ao lado de ZR1): terminal
  **torto/descolorido**, coerente com calor do arco na face oposta.
- **Resistor axial de 51 kΩ** (faixas verde-marrom-laranja-dourado, à direita de
  FUS1): íntegro.
- **C1** (X2 amarelo): íntegro, sem trincas.
- **E1/E2** (eletrolíticos do primário, manga amarela): sem estufamento, sem
  eletrólito vazado, topo com vent intacto.

### 2.5 Demais componentes da fonte e da placa (sem dano visível)
**T1** (EE16-1.5mH WM), **D3**, **D7**, **IC9** (optoacoplador), **IC2** (PC817),
**IC3** (TL431C), **E3/E4/E7**, relés **RY1…**, **BUZ1**, conectores **CNx/CON1**.

---

## 3. Interpretação do evento (compatível com as evidências)
1. Inseto pousou sobre a zona de rede da **face de solda**, ponteando os pads **IN** /
   nós de R3–R4–C4 (diferença de potencial de linha, ~220 V).
2. O arco elétrico **carbonizou o substrato** e queimou R3, confirmado aberto. R4/C4
   ocupavam a mesma ilha afetada, mas seu estado e designadores ainda não foram
   confirmados individualmente.
3. **Não há evidência visual de ruptura de ZR1.** As fotos também não permitem afirmar
   se FUS1/FUSE2 abriram nem determinar a ordem temporal das falhas.
4. O escurecimento junto a **IC1 (LNK3604P)** justifica testar o estágio chaveador,
   mas não demonstra por si só que o MOSFET interno foi destruído.

### Componentes condenados ou sob teste

- **R3:** condenado; queimado e aberto, confirmado por medição;
- **ZR1:** encapsulamento visualmente íntegro; estado elétrico ainda não testado;
- **R4/C4:** identificação e estado ainda incertos;
- **FUS1/FUSE2:** continuidade confirmada;
- **DB1, D1/D2/D3, D7 e IC1:** triagem em modo diodo favorável, sem comprovação sob
  alta tensão;
- **T1:** enrolamentos contínuos e isolamento superior a 2 MΩ na escala disponível;
- **E1–E4, PC817 e TL431:** sem curto detectável em circuito.

As leituras completas e suas limitações estão em
[`medicoes_diagnostico_LL14X.md`](medicoes_diagnostico_LL14X.md).

## 4. Estado da reconstrução

- Toda a carbonização visível foi removida da placa.
- A região foi planificada para receber um novo R3.
- A trilha entre DRAIN de IC1 e o primário de T1 foi removida e permanece aberta.
- Está planejada a fixação mecânica com resina epóxi **Araldite Hobby 10 min**.

A remoção do carvão elimina o caminho condutivo visível, mas também altera espessura,
distâncias de escoamento e resistência mecânica do substrato. A resina citada não é
tratada aqui como isolante certificado para rede: antes de energizar, é necessário
confirmar que sua ficha técnica atende à tensão, temperatura, resistência a arco e
comportamento antichama exigidos, além de medir a resistência de isolamento e conferir
as distâncias entre cobre exposto, terminais e regiões de baixa tensão. Se essas
condições não puderem ser garantidas, a placa deve ser substituída.
