# Diagrama levantado da fonte, dos relés e do aquecimento — LL14X

| Campo | Identificação |
|---|---|
| Data do levantamento | **26/08/2026** |
| Placa | **WQP12-7601S.D.1-1 V1.1**, nº **17176000033271** |
| Aplicação | lava-louças Electrolux LL14X, versão para rede de **127 V** |

Este documento registra o circuito reconstruído a partir das fotografias das duas
faces da placa, das medições feitas sem dessoldar componentes, das serigrafias e do
manual de serviço da família Midea WQP12-7601S. Ele não é um esquema oficial do
fabricante.

Fotografias principais:

- [face dos componentes](../imagens/originais/PXL_20260823_033933343.jpg);
- [face das soldas](../imagens/originais/PXL_20260823_033906993.jpg).

Referências externas:

- [manual de serviço Midea MDWEF1433D, placa WQP12-7601S](https://www.midea.com/content/dam/midea-aem/fr/fr-new/pdp/guide-de-r%C3%A9paration/Service-manual-MDWEF1433D-SS-W.pdf);
- [manual de serviço Electrolux LL10B/LL10X/LL14B/LL14X, rev. 00 (mar./2021)](https://pt.scribd.com/document/893500928/Manual-Servicos-Lava-Loucas-LL10B-LL10X-LL14B-LL14X-Rev00-Marco2021);
- [datasheet do ULN2003A — Texas Instruments](https://www.ti.com/lit/gpn/ULN2003A).
- [SH79F6484 — SinoWealth](https://en.sinowealth.com/detaile?pro_id=18).

## 1. Convenções e grau de confiança

| Marca | Significado |
|---|---|
| **[F]** | confirmado diretamente por fotografia ou serigrafia |
| **[M]** | confirmado por medição na placa |
| **[D]** | confirmado por documentação da mesma família de placa |
| **[I]** | inferência forte pela topologia, pelo layout ou pelo componente empregado |
| **[P]** | pendente de confirmação por continuidade ou medição energizada |

As trilhas da placa estão distribuídas nas duas faces e algumas passam sob relés,
conectores e o microcontrolador. Por isso, toda ligação não visível integralmente foi
mantida como inferência ou pendência, mesmo quando corresponde ao circuito usual.

## 2. Diagrama funcional consolidado

```text
REDE 127 Vca
     │
     ├── CON1(L) ── FUSE1 ─┐
     │                     ├── proteção/filtro ── DB1 ── E1 ── L2/L1 ── E2 ── primário de T1
     └── CON1(N) ── FUSE2 ─┘                         │
                                                    │ flyback: IC1 = LNK3604P
                                                    │ realimentação: IC2 + IC3
                                                    ▼
                                    secundário de T1 ── D7 ── filtragem secundária
                                                        (E3/E4, conexões pendentes [P])

                       relação com o barramento dos relés: não confirmada

VREL (barramento de 12 V ainda não localizado) ──┬─ bobinas dos relés menores [I]
                                                  └─ bobina de RY5, 270 Ω [M]
                                                            │
                  IC4 = ULN2003 [F/I] ou Q9 [I/P] ── possível chaveamento para GND_S

MCU em 5 V ── sete entradas de IC4 [I]
      │
      └── R21, `202` = 2 kΩ ── Q9 ── RY5 [F/M]

CIRCUITO DE POTÊNCIA DO AQUECEDOR

CON1(L) ── fio marrom ── P01 ── contato normalmente aberto de RY5 ── P02
                                                                    │
                                                   fio lilás/rosado │
                                                                    ▼
                                                        H1 da resistência

H2 da resistência ── fio azul ── fluxostato ── CON1(N), fio azul [D/M]
```

O diagrama acima separa dois domínios:

- a **bobina de RY5**, que trabalha com aproximadamente 12 Vcc e consome apenas
  dezenas de miliampères;
- o **contato de RY5**, P01 e P02, que conduz a corrente de rede da resistência,
  próxima de 8 A na versão de 127 V.

Não existe conversão direta de um sinal de 5 V do microcontrolador em uma saída de
12 V. As bobinas recebem a rail de 12 V em uma extremidade; o ULN2003 ou Q9 liga a
outra extremidade ao GND. O sinal lógico de 5 V apenas controla esse chaveamento.

## 3. Entrada de rede e fonte flyback

### 3.1 Primário

| Nó ou componente | Conexão/função | Evidência |
|---|---|---|
| CON1 | entrada da rede, pinos serigrafados `L` e `N` | **[F]** e informação do proprietário |
| FUSE1/FUSE2 | fusíveis em série com os dois condutores de entrada | **[F/M]** |
| ZR1, C1 e resistor axial de 51 kΩ | proteção, filtragem e descarga entre os condutores da rede | **[F/I]** |
| R3 | 33 Ω, limitador da corrente de irrupção na energização; original carbonizado e aberto | **[F/M]** |
| DB1 | ponte retificadora da entrada | **[F/M]** |
| E1/E2 | 4,7 µF / 450 V cada, capacitores do barramento primário | **[F]** |
| L2 | entre E1(+) e E2(+) | **[M/F]** |
| L1 | entre E2(−) e E1(−) | **[M/F]** |
| IC1 | LNK3604P, controlador/MOSFET da flyback | **[F/M]** |
| T1 | EE16-1.5mH WM, transformador isolador da flyback | **[F/M]** |

As ligações levantadas no filtro do barramento são:

```text
E1(+) ── L2 ── E2(+)
E1(−) ── L1 ── E2(−)
```

Assim, E1 e E2 não estão diretamente em paralelo: L1/L2 formam um filtro entre os
dois capacitores. As resistências brutas medidas foram 0,7 Ω em L1 e 1,5 Ω em L2;
como as pontas do multímetro variam entre 0,6 Ω e 1,3 Ω, ambas são compatíveis com
baixa resistência em corrente contínua.

O caminho funcional do primário é:

```text
CON1(L/N) → FUSE1/FUSE2 → proteção/filtro → DB1 → E1/E2
E1/E2(+) → primário de T1 → DRAIN de IC1
E1/E2(−) → SOURCE de IC1
```

A trilha entre DRAIN de IC1 e o primário de T1 foi destruída pelo arco e
posteriormente reconstruída. A máquina voltou a inicializar e acionar cargas, o que
comprova que a flyback está operando, embora suas tensões ainda não tenham sido
medidas diretamente.

### 3.2 Secundário e rail principal

| Nó ou componente | Conexão/função | Evidência |
|---|---|---|
| D7 | retificação do secundário de T1 | **[F/I]** |
| E3 | 680 µF / 25 V, capacitor no secundário; tensão e conexões ainda não identificadas | **[F/P]** |
| L1/L2 | indutores axiais no setor secundário; sua ligação exata aos capacitores deve ser reidentificada | **[F/P]** |
| E4 | 220 µF / 16 V, capacitor do secundário; tensão e carga alimentada ainda não foram identificadas | **[F/P]** |
| IC3/IC2 | TL431C e PC817, realimentação isolada da flyback | **[F/I]** |
| VREL | barramento que alimenta as bobinas de 12 V; ainda não localizado na placa | **[I/P]** |

Há pelo menos um barramento de aproximadamente 12 V, pois as bobinas dos relés são
marcadas para 12 V. Contudo, não se demonstrou ainda que ele seja E3/E4. Os indícios
para a existência da alimentação de 12 V são:

1. RY5 está marcado `12V` **[F]**;
2. os relés menores também estão marcados `12V` **[F]**;
3. válvulas, circulação e drenagem funcionaram, comprovando o acionamento de relés
   de 12 V **[M]**.

Uma falta geral da alimentação das bobinas de 12 V é incompatível com o funcionamento
já observado. Ainda seria possível uma interrupção localizada entre esse barramento e
a bobina de RY5.

## 4. Rail lógica de 5 V

A presença de 5 V está confirmada pela serigrafia dos conectores e pontos de teste,
inclusive `+5V`, `GND`, `VDD`, `TURB`, `PWM`, `RE` e interfaces de comunicação
**[F]**. O funcionamento do painel, do microcontrolador e dos sensores confirma que
essa rail está operacional **[M]**.

O circuito exato que deriva 5 V da saída principal ainda não foi completamente
rastreado. Pela posição e pelas trilhas, o bloco discreto em torno de **Q1, Q10 e D8**
é candidato à regulação/condicionamento dessa rail **[I/P]**. Não há evidência
suficiente para nomear seus terminais ou fechar o esquema sem medições de
continuidade.

Rastreamento ainda necessário:

```text
fonte secundária / barramento ainda não identificado → bloco Q1/Q10/D8 [P]
                                                → +5V dos conectores → VDD do MCU
referência secundária ainda não identificada ───→ GND do MCU
```

## 5. Banco dos sete relés menores — IC4

IC4 é um encapsulamento SOIC-16 cuja marcação é compatível com **ULN2003** **[F]**.
Esse componente contém sete pares Darlington de coletor aberto e sete diodos internos
de roda-livre. Seu pinout padrão é:

| Pino de IC4 | Função |
|---:|---|
| 1–7 | entradas lógicas 1B–7B |
| 8 | GND |
| 9 | COM dos diodos internos; normalmente ligado ao positivo das bobinas |
| 10–16 | saídas 7C–1C para as bobinas |

A placa possui sete relés menores e um relé grande, RY5. A correspondência numérica
entre sete canais e sete relés menores, somada à presença do estágio discreto Q9/D9
ao lado de RY5, sustenta esta topologia **[I forte]**:

```text
MCU(5 V) → IC4, entradas 1–7
IC4, saídas 10–16 → extremidade comutada das sete bobinas menores
IC4, pino 8 → referência negativa do secundário
IC4, pino 9 → VREL
outra extremidade de cada bobina → VREL
```

O manual da placa identifica as seguintes saídas de carga, mas as fotografias ainda
não permitem associar com segurança cada uma delas a um número RY específico:

- `ML-H`: velocidade alta da bomba de circulação;
- `ML-L`: velocidade baixa da bomba de circulação;
- `PS`: bomba de drenagem;
- `EV1`: válvula de entrada;
- `EV2`: válvula de regeneração;
- `EV3`: válvula desviadora;
- `D/Ed`: dispenser;
- além das saídas auxiliares `FAN` e `LIGHT`, que podem usar estágios distintos.

Não se deve inferir a correspondência `RYn → carga` apenas pela ordem física dos
relés; ela deverá ser determinada seguindo cada contato até o pino serigrafado do
conector correspondente.

## 6. RY5, P01/P02, D9 e Q9 — aquecimento

### 6.1 Caminho de potência

O manual de serviço da placa identifica explicitamente **P01/P02 como `Heating
Element`** **[D]**. Nas fotografias, os dois fast-ons ficam próximos da inscrição
`Mark` e do relé grande RY5 **[F]**.

- **P01:** terminal cuja ilha grande foi claramente arrancada da placa durante a
  remoção do conector **[F]**;
- **P02:** terminal imediatamente adjacente a P01 **[F]**;
- ambos tiveram as trilhas reparadas e apresentaram continuidade estática do fast-on
  até pinos de potência do relé **[M]**;
- o contato entre P01 e P02 deve permanecer aberto enquanto RY5 está desenergizado
  **[I]**.

Topologia levantada:

```text
P01 → trilha/ilha reparada → contato de potência de RY5
                                   /
                         normalmente aberto
                                   \
P02 ← trilha/ilha reparada ← outro contato de potência de RY5
```

#### Chicote externo confirmado

O rastreamento feito fora da placa confirmou as duas primeiras partes do caminho de
potência, sem depender da cor como prova única:

```text
CON1(L) ── fio marrom ── P01 ── contato NA de RY5 ── P02 ── fio lilás/rosado ── H1
```

- há continuidade entre o fio marrom de `CON1(L)` e o fio marrom de `P01` **[M]**;
- há continuidade entre o fio lilás/rosado de `P02` e um terminal da resistência
  (`H1`) **[M]**.

Logo, RY5 comuta o condutor de linha para a resistência, e não o retorno. A
serigrafia `L`/`N` é a identificação funcional determinante: `L` é *line* (fase) e
`N` é neutro. O marrom também é uma cor normalizada para condutor de fase; a cor só
corrobora a serigrafia, não a substitui. O outro terminal da resistência (`H2`) usa
fio azul, mas **não** apresentou continuidade até o fio azul de `CON1(N)` **[M]**.
O manual de serviço específico da Electrolux resolve esta ambiguidade: o
**fluxostato está ligado em série com a resistência** **[D]**. Portanto, sem
pressão/fluxo de água, essa ausência de continuidade é o comportamento previsto; não
é indício de um segundo relé. O manual orienta testar o fluxostato entre os fios
branco e violeta de `CN04`: sem pressão, aberto; com pressão e nível de água atingido,
fechado **[D]**.

O chicote foi rastreado e há continuidade até ambos os conectores do fluxostato
**[M]**. Assim, a cadeia externa confirmada é `P02 → resistência → fluxostato →
CON1(N)`; o único estado ainda desconhecido nessa cadeia é o fechamento do contato
interno do fluxostato sob pressão de circulação.

O mesmo manual estabelece duas referências úteis para os demais chicotes de potência:

```text
CON1(L), marrom ── interruptor da porta ── CON2(IS), marrom

CON1(N), azul ───────────────────────────── retorno da válvula EV1
CON3(EV1), azul ── contato do relé de EV1 ── fase somente durante o enchimento
```

- para o interruptor da porta, ele manda medir entre o marrom de `CON1` e o marrom de
  `CON2`: porta fechada = continuidade; porta aberta = circuito aberto. Assim,
  `CON2(IS)` recebe fase **após** o interruptor da porta estar fechado **[D]**;
- para a válvula de entrada, ele manda medir a tensão entre o azul de `CON1` e o azul
  de `CON3` enquanto EV1 é acionada. Assim, o azul de `CON1` é o retorno/neutro de
  referência e `CON3(EV1)` é a fase chaveada da válvula — embora ambos os fios sejam
  azuis **[D]**.

Para a LL14X de 127 V, o manual Electrolux especifica aproximadamente **14 Ω** para a
resistência. Isso corresponde aproximadamente a 1,15 kW e à seguinte corrente no
contato e nas trilhas:

```text
I ≈ V / R ≈ 127 V / 14 Ω ≈ 9,1 A
```

Uma continuidade audível não prova que o reparo suporta essa corrente. Por exemplo,
1 Ω de resistência parasita, ainda detectado como continuidade pelo multímetro,
dissiparia aproximadamente 83 W com 9,1 A.

### 6.2 Bobina e diodo de roda-livre

RY5 possui marcação `12V` **[F]**. A medição direta da bobina foi:

| Escala do multímetro | Leitura | Interpretação |
|---:|---:|---|
| 20 kΩ | 0,27 kΩ | aproximadamente 270 Ω; bobina contínua |
| 2 kΩ ou 200 Ω | valor transitório e depois infinito | comportamento anômalo do multímetro/circuito em paralelo |

Com 270 Ω, a corrente e a potência nominais estimadas são:

```text
I_bobina ≈ 12 V / 270 Ω ≈ 44 mA
P_bobina ≈ 12² / 270 Ω ≈ 0,53 W
```

D9 está em paralelo com a bobina de RY5, confirmado por fotografia e continuidade
entre seus terminais e os dois nós da bobina **[F/M]**. Portanto, é o diodo de
roda-livre da bobina. No modo diodo foram lidos aproximadamente **254 mV nos dois
sentidos** **[M]**; a bobina em paralelo explica por que essa medição em circuito não
mostra a queda direta isolada de D9.

Nenhum terminal de D9 apresentou **continuidade audível** com E4(+) **[M]**. Isso
descarta uma ligação direta D9–E4(+), mas não descarta uma ligação por uma bobina ou
resistor: aproximadamente 270 Ω normalmente não aciona o bip de continuidade.

Foi confirmada visualmente e por continuidade a ligação entre o **terminal inferior de
D9** e o **pad isolado/superior de Q9** (o pad central, oposto aos dois pads inferiores
do encapsulamento SOT-23) **[F/M]**. Esse é um dos dois nós da bobina de RY5.

O **pad inferior direito de Q9**, na orientação da fotografia de referência, apresentou
continuidade audível e indicação `001` até um `GND` de conector de baixa tensão
**[M]**. Assim, Q9 é confirmado como chave de baixa lateral: seu pad superior é o nó
comutado da bobina (coletor ou dreno) e o pad inferior direito é a referência negativa
(emissor ou fonte). No modo diodo, entre o pad inferior esquerdo e o direito foram
medidos **618 mV** com a ponta vermelha à esquerda e infinito no sentido inverso
**[M]**. Isso confirma a junção base–emissor de um transistor **NPN**: o pad inferior
esquerdo é a base e o direito é o emissor. O pad superior é, consequentemente, o
coletor. A junção base–coletor também foi medida íntegra: **612 mV** com a ponta
vermelha na base e a preta no coletor, e infinito no sentido inverso **[M]**. Esses
testes não validam o ganho do transistor sob carga, mas descartam curto ou abertura
nas duas junções principais.

Topologia esperada:

```text
                   bobina de RY5
VREL ────────────────/\/\/\/────────────── nó RY5_COIL_LOW
  │                                             │
  └────────── cátodo ──|<|── ânodo ─────────────┘
                       D9
```

O nó VREL e a polaridade efetiva de D9 permanecem **[P]**. Não se deve usar E4(+) como
referência para essa identificação até que se meça a tensão de E3/E4 e se rastreie o
caminho até uma bobina de relé.

Com a placa energizada em bancada, foi medida tensão de aproximadamente **12,8 Vcc**
entre o terminal superior de D9 e um `GND` de conector de baixa tensão **[M]**. Como o
terminal inferior de D9 é o coletor de Q9, essa leitura confirma a alimentação positiva
da bobina de RY5; o terminal superior é VREL e também o cátodo de D9.

### 6.3 Driver discreto Q9

Q9 é o transistor SOT-23 localizado imediatamente ao lado de D9 **[F]**. A topologia
mais provável é um driver NPN de baixa lateral:

```text
                     +12 V / VREL
                           │
                      bobina de RY5
                           │
                           C
MCU ── resistor de base ── B  Q9
                           E
                           │
                         GND_S
```

O rastreamento visual do lado de solda confirmou o caminho de comando:

```text
base de Q9 → R21, `202` = 2 kΩ → MCU
```

Não há jumper de 0 Ω nesse caminho. R21 mediu aproximadamente **2 kΩ nos dois sentidos**
com a placa desligada **[M]**, confirmando a marcação `202`. O pino específico do MCU
foi identificado por continuidade: **pino 34** do LQFP-44 **[M]**.
No SH79F6484P, esse pino é **P1.7**, compartilhado com `SEG8/LED_S8`; nesta placa ele
é empregado como GPIO de comando de RY5 **[D/M]**.

Conexões que devem existir se essa reconstrução estiver correta:

| Teste desenergizado | Resultado esperado |
|---|---|
| pad isolado/superior de Q9 → terminal inferior de D9 | continuidade confirmada; coletor/nó comutado da bobina |
| pad inferior direito de Q9 → GND de baixa tensão | continuidade confirmada, leitura `001`; emissor |
| base (pad inferior esquerdo) → emissor (pad inferior direito) | 618 mV, vermelho na base; infinito ao inverter | junção B–E NPN íntegra |
| base (pad inferior esquerdo) → coletor (pad superior) | 612 mV, vermelho na base; infinito ao inverter | junção B–C NPN íntegra |
| base (pad inferior esquerdo) → terminal de R21 | rota visual confirmada | resistor de comando R21, `202` = 2 kΩ |
| R21 → pino 34 do MCU | continuidade confirmada | P1.7 / `SEG8` / `LED_S8`; comando de RY5 |

Há dois pads/vias expostos no ramo de comando **[F/M]**:

```text
TP-MCU ── P1.7/pino 34 ── R21 (2 kΩ) ── TP-BASE ── base de Q9
```

Eles permitem acessar P1.7 e a base de Q9 sem encostar a ponta de prova na perna do
LQFP ou no SOT-23. O manual de serviço não lhes dá designação nem procedimento
específico. O `PT1` que aparece no mapa do manual é outro ponto, situado junto a
CON1/entrada de rede. O manual diagnostica cargas pelos conectores e pelo programa de
teste, não por pontos internos do MCU **[D]**.

Quando P1.7 comandar RY5, o comportamento esperado é aproximadamente 5 V em TP-MCU,
0,6–0,8 V em TP-BASE e 4,2–4,4 V de queda em R21. Sem comando, ambos os pontos devem
ficar próximos de 0 V. Esses valores são previstos pela medição de 2 kΩ em R21 e pela
queda B–E de 618 mV de Q9 **[I/M]**.
| lado MCU do resistor → um pino do microcontrolador | continuidade |

## 7. Microcontrolador e sinais de comando

O microcontrolador é um **SinoWealth SH79F6484P**, encapsulamento **LQFP-44** **[F]**.
É um microcontrolador de 8 bits compatível com 8051, com 64 KB de Flash, segundo o
datasheet do fabricante **[D]**. O rebaixo circular do encapsulamento indica o pino 1
nas fotografias ampliadas **[F]**.

Há dois grupos de saídas:

```text
sete pinos do MCU → entradas 1–7 de IC4 → sete relés menores
pino 34 / P1.7    → R21 → Q9 → RY5/aquecimento
```

Para identificar o pino físico de RY5 sem dessoldar:

1. confirmar primeiro, com a matriz de testes, se Q9 e D9 pertencem de fato à bobina
   de RY5;
2. identificar em Q9 o terminal ligado ao nó comutado e o terminal ligado à referência
   negativa comum;
3. o terminal restante será a base, se Q9 for mesmo o transistor de acionamento;
4. seguir a base até o resistor em série;
5. colocar uma ponta no pad de R21 voltado ao MCU;
6. a continuidade foi confirmada no pino 34, P1.7.

As saídas do MCU provavelmente trabalham em nível lógico de 5 V. O ULN2003 e Q9 não
elevam essa tensão; apenas afundam a corrente das bobinas para GND_S.

## 8. Matriz de testes para fechar o esquema

Todos os testes desta seção devem ser realizados com a placa desligada da rede e com
E1/E2 previamente verificados como descarregados.

| Nº | Pontos | Resultado esperado | O que confirma |
|---:|---|---|---|
| 1 | cada terminal de D9 ↔ E4(+) na escala de 20 kΩ | anotar valores, sem usar apenas o bip | existência ou não de caminho resistivo até E4 |
| 2 | um terminal de D9 ↔ um terminal da bobina de RY5 | resistência das pontas ou aproximadamente 270 Ω, conforme o nó | relação real entre D9 e a bobina |
| 3 | terminais da bobina de RY5 entre si | aproximadamente 270 Ω | referência para os testes seguintes |
| 4 | pinos de Q9 ↔ terminais da bobina/D9 | anotar as três resistências | identificação do possível coletor |
| 5 | base de Q9 ↔ R21 | continuidade | resistor e rede de comando |
| 6 | lado MCU do resistor ↔ pino físico do MCU | resistência das pontas | saída exata de aquecimento |
| 7 | pino 9 (COM) de IC4 ↔ uma ponta de cada bobina menor | resistência das pontas ou caminho via diodos | topologia do ULN2003 |
| 8 | pino 8 (GND) de IC4 ↔ referência negativa do secundário | resistência das pontas | terra comum dos drivers |
| 9 | P01 ↔ primeiro contato de potência de RY5 | resistência das pontas, estável ao movimentar | primeiro reparo mecânico |
| 10 | P02 ↔ segundo contato de potência de RY5 | resistência das pontas, estável ao movimentar | segundo reparo mecânico |
| 11 | P01 ↔ P02, RY5 desligado | infinito | contato normalmente aberto |
| 12 | P01 ↔ P02, bobina alimentada em 12 V | próximo da resistência das pontas | fechamento do relé e das trilhas |

O multímetro utilizado varia a resistência das próprias pontas, já tendo indicado de
0,6 Ω a 1,3 Ω. Assim, leituras de baixa resistência devem ser comparadas com um curto
das pontas feito imediatamente antes ou depois do teste. Mesmo assim, o instrumento
não mede adequadamente a resistência de contato esperada, que deveria estar na faixa
de milésimos de ohm.

## 9. Estado diagnóstico atual

Já foi observado na máquina:

- inicialização e painel funcionando;
- válvula de entrada funcionando;
- bomba de circulação funcionando com pressão;
- bomba de drenagem funcionando;
- ausência de aquecimento em programa que deveria aquecer;
- NTC e chicote medindo **12,1 kΩ**, valor compatível com aproximadamente 20 °C;
- resistência de aquecimento contínua, embora a leitura anterior de 7–8 Ω divirja da
  especificação de aproximadamente 14 Ω do manual e o multímetro tenha apresentado
  leituras inconsistentes de baixa resistência;
- bobina de RY5 contínua, aproximadamente 270 Ω;
- P01/P02 sofreram dano mecânico conhecido e tiveram trilhas reparadas.

O defeito de aquecimento está, portanto, concentrado nos seguintes blocos:

1. reparos e resistência de contato em P01/P02;
2. contato de potência interno de RY5;
3. alimentação localizada da bobina de RY5;
4. Q9 e sua rede de base;
5. saída específica do microcontrolador;
6. fluxostato hidráulico externo, que está em série com a resistência e permanece
   aberto sem pressão/fluxo, devendo fechar com pressão e nível de água atingido.

A operação dos relés menores reduz fortemente a probabilidade de falha geral nas
rails de 12 V ou 5 V.

## 10. Programa de teste do manual — comando controlado de aquecimento

O manual de serviço da família WQP12-7601S descreve um programa de teste destinado a
acionar cargas individualmente **[D]**. Segundo ele, com a porta aberta e dentro de
60 s após energizar a máquina, deve-se manter `Start/Pause` pressionado e pressionar
`POWER` até entrar no modo de teste; depois, fechar a porta para iniciá-lo. O próprio
manual avisa que o método de ativação pode variar entre modelos.

| Etapa | Ação descrita no manual | Utilidade neste diagnóstico |
|---:|---|---|
| 0 | inicialização/espera | confirmar entrada no modo de teste |
| 1 | válvula de entrada até cerca de 3,6 L | estabelece nível de água para a etapa seguinte |
| 2 | bomba de lavagem em alta; **10 s depois, aquecimento** até 57 °C | mede o comando P1.7 e o acionamento de RY5 |
| 3 | bomba em baixa e dispenser | não é relevante para RY5 |
| 4 | válvula de regeneração | não é relevante para RY5 |
| 5 | drenagem | não é relevante para RY5 |

Na etapa 2, depois dos 10 s iniciais da bomba, os pontos expostos fornecem uma
sequência de decisão direta:

| Medida | Resultado | Interpretação |
|---|---:|---|
| TP-MCU ↔ GND | aproximadamente 5 V | firmware está ordenando RY5 |
| TP-BASE ↔ GND | aproximadamente 0,6–0,8 V | Q9 recebe corrente de base |
| TP-MCU ↔ GND | aproximadamente 0 V | a ordem de aquecimento não foi emitida |

O programa só é útil para essa medição com a máquina montada e em posição normal,
pois ele depende do enchimento e da circulação de água. Ele não deve ser usado para
forçar aquecimento em bancada.

O painel da LL14X não mostra a temperatura instantânea da água no uso normal; o
indicador `70 °C` pertence à função Higienizar e não é um termômetro em tempo real.
Portanto, a indicação `Temperature value` descrita no manual da família Midea não deve
ser pressuposta nesta variante. Na LL14X, o programa de teste serve para estabelecer o
momento conhecido de comando do aquecimento; a confirmação deve ser feita por TP-MCU,
TP-BASE ou medição externa de temperatura **[M/D]**.

## 11. Segurança

- O primário contém tensão de rede e um barramento retificado perigoso.
- A lâmpada em série limita corrente, mas não fornece isolamento galvânico.
- Não conectar o osciloscópio comum com sonda passiva ao primário.
- Para teste externo de RY5, a placa deve estar completamente desconectada da rede e
  dos chicotes.
- Não aplicar 12 V à bobina por tentativa enquanto a ligação de D9 e dos terminais da
  bobina não estiver confirmada; uma polaridade errada pode aplicar curto pela suposta
  proteção de roda-livre.
- A continuidade do multímetro não valida um reparo destinado a conduzir cerca de
  8 A; inspeção mecânica e teste sob corrente controlada continuam necessários.
