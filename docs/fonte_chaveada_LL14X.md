# Subsistema de fonte chaveada — placa de potência LL14X / LC14S
**PCB: WQP12-7601S.D.1-1 V1.1** — topologia: **flyback isolado em torno de IC1 = LNK3604P
(LinkSwitch, Power Integrations)**. A realimentação é formada por **IC3 = TL431C** e
**IC2 = PC817**.

Sim, a região danificada **é** a fonte chaveada: ela ocupa a extremidade da placa onde
estão ZR1/FUS1/FUSE2/C1 (entrada de rede), DB1/E1/E2 (primário), IC1/T1 (conversor) e
D7/E3/E4/IC2/IC3 (secundário). O arquivo
[`modelos/fonte_chaveada_LL14X.cir`](../modelos/fonte_chaveada_LL14X.cir) simula esse
subsistema.

Legenda: **(foto)** = conexão/designador lido das fotos; **(típ.)** = suposição baseada
na aplicação típica do LNK3604 e no layout (valores não legíveis nas fotos).

---

## 1. Inventário do subsistema

| Ref | Parte | Pacote | Função |
|-----|-------|--------|--------|
| CON1 | conector 2 vias | TH | entrada de rede L/N (fio do filtro) |
| FUS1 | fusível T3.15AL/AC250V | caixa retangular | proteção de sobrecorrente da linha |
| FUSE2 | fusível (2ª linha) | caixa retangular | proteção do neutro |
| ZR1 | varistor (≈471K) **(típ.)** | disco | grampeamento de surto |
| C1 | capacitor X2 0,22 µF/275 VAC **(típ.)** | caixa amarela | filtragem EMI diferencial |
| R(51k) | resistor axial 51 kΩ (verde-marrom-laranja) | TH | descarga/bleeder da entrada |
| R3 | 33 Ω (SMD "33R0") | 1206 | limitador de inrush/surto; original queimado e aberto **(medido)** |
| DB1 | ponte retificadora | SMD 4 terminais | retificação de entrada |
| E1, E2 | 4,7 µF / 450 V / 105 °C cada **(lido)** | TH | bulk do primário; 9,4 µF no modelo |
| IC1 | **LNK3604P** | DIP-8 | MOSFET 700 V + controlador flyback |
| T1 | **EE16-1.5mH WM** **(lido)** | TH | transformador flyback; marcação indica 1,5 mH |
| D1, D2, D3 | diodos 1N400x | TH | snubber/retorno do primário |
| C2, R1, R2 | 100 kΩ/MLCC | SMD | rede de snubber/descarga do primário |
| IC2 | **PC817**, marcação adicional “CT12” **(lido)** | DIP-4 | optoacoplador da realimentação isolada |
| IC3 | **TL431C TI**, marcação “19WO4D1” **(lido)** | 3 terminais | referência shunt ajustável; amplificador de erro |
| IC9 | optoacoplador 4 pinos | SMD | função ainda não rastreada; não confundir com IC2 |
| D7 | marcação parcial **“SRII?”** | axial | retificação rápida do secundário; código exato incerto |
| E3 | 680 µF / 25 V / 105 °C **(lido)** | TH | filtro antes de L1/L2 |
| L1 | laranja–laranja–dourado–prata **(lido)** | axial | entre E3(−) e E4(−); 3,3 µH ±10 % pela codificação usual **(hip.)** |
| L2 | marrom–preto–laranja–prata **(lido)** | axial | entre E3(+) e E4(+); 10 mH ±10 % pela codificação usual **(hip.)** |
| E4 | 220 µF / 16 V / 105 °C **(lido)** | TH | filtro após L1/L2, no lado da carga |
| L(5V) | bead/indutor da rail 5 V (serigrafia "5V") | TH | desacoplamento da rail p/ lógica |

## 2. Nets / conexões (primário)

- **NET-L**: CON1(1) → FUS1 → nó **LA**.
- **NET-N**: CON1(2) → FUSE2 → nó **N1**.
- **Entre LA e N1** (paralelo): ZR1, C1, R(51k).
- **LA → R3 → AC+** de DB1; **N1 → AC−** de DB1 (retorno).
- **DB1+ → VB**: E1(+), E2(+), primário de T1 (ponto), ramo de snubber (D1/D2 + C2/R1/R2).
- **DB1− → GND_P**: E1(−), E2(−), pino SOURCE de IC1.
- **T1 primário (sem ponto) → DRAIN** de IC1 (pinos de dreno).
- **FB de IC1 ← fototransistor de IC2 (PC817)**; pino BP com capacitor local **(típ.)**.

## 3. Nets / conexões (secundário, isolado — GND_S)
- **T1 secundário (ponto) → GND_S** (retorno da saída).
- **T1 secundário (sem ponto) → ânodo de D7**; **cátodo de D7 → V12**.
- **VRET-RAW → L1 → GND_S**: L1 está entre os terminais negativos de E3 e E4.
- **VOUT-RAW → L2 → VOUT**: L2 está entre os terminais positivos de E3 e E4.
- **E3** filtra a saída diretamente após D7; **E4** filtra o lado da carga após
  L1/L2. Portanto, os capacitores não estão exatamente em paralelo.
- **Realimentação**: um divisor da saída alimenta REF de IC3 (TL431C). Quando VOUT
  sobe, IC3 aumenta a corrente no LED de IC2; o fototransistor de IC2, no primário,
  atua no FB de IC1 e reduz a energia transferida.
- A serigrafia **5V** confirma uma rail de 5 V em outra parte da placa, mas as fotos
  atuais não bastam para atribuir seu regulador ou conexão exata. Não há base para
  afirmar uma rail de 3,3 V.
- GND_P e GND_S são separados; T1 e IC2 atravessam funcionalmente a barreira de
  isolamento.

## 4. Operação (resumo)

IC1 chaveia o primário de T1 a ~66 kHz **(típ.)**; na desmagnetização, D7 entrega
energia a E3/E4, gerando a saída principal (12 V é a hipótese atual). IC3 compara uma
fração da saída com sua referência interna e controla o LED de IC2; IC2 fecha o laço
até o FB de IC1. ZR1/C1/R3/RF1/FUS1/FUSE2 formam a frente de proteção e filtragem de
rede — região em que ocorreu o arco, embora ZR1 esteja visualmente íntegro.

## 5. Simulação reproduzível

Arquivos:

- [`fonte_chaveada_LL14X.cir`](../modelos/fonte_chaveada_LL14X.cir): modelo médio funcional para ngspice;
- [`sim_fonte.py`](../modelos/sim_fonte.py): implementação independente em Python/NumPy;
- `resultados/ll14x_fonte.dat` e `resultados/ll14x_ondas.csv`: formas de onda geradas nas validações e não versionadas.

```
ngspice -b modelos/fonte_chaveada_LL14X.cir
python3 modelos/sim_fonte.py
python3 modelos/sim_fonte.py --waveform
```

Os dois modelos mantêm explícitos a rede 220 Vrms/50 Hz, os fusíveis, ZR1, C1, R3,
DB1 e E1/E2. O estágio IC1–T1–D7–IC3–IC2 é médio: uma fonte controlada retira potência
do barramento e outra a entrega, isoladamente, à saída de 12 V. O erro de V12 comanda
a potência. O limite ilustrativo de aproximadamente 8 W resulta de 1,5 mH, 0,40 A
estimado e 66,7 kHz. Assim, o modelo serve para conferir nós,
polaridades, níveis DC e sequência de alimentação, mas não prevê esforço de pico no
MOSFET, ringing, snubber, EMI ou estabilidade ciclo a ciclo.

### 5.1 Resultado validado em 24/08/2026

| Grandeza | Python (40–60 ms) | ngspice (60–80 ms) |
|---|---:|---:|
| barramento E1/E2, média | 309,2 V | 309,47 V |
| barramento E1/E2, mín.–máx. | — | 308,88–310,03 V |
| saída principal após L1/L2 | 12,01 V | 12,0111 V |

As duas execuções terminaram sem erro de convergência. A proximidade entre elas
confirma apenas a consistência das hipóteses compartilhadas; não substitui medição da
placa. O valor de 12 V é um alvo presumido a partir da topologia e das tensões dos
capacitores, não uma medição de uma unidade funcional.

### 5.2 Parâmetros ainda estimados

- C1 = 0,22 µF e ZR1 ≈ MOV 471;
- E1 // E2 = 9,4 µF, confirmados pelos valores informados;
- E3 = 680 µF/25 V e E4 = 220 µF/16 V, separados em ambos os condutores por L1/L2;
- L1 = 3,3 µH ±10 % e L2 = 10 mH ±10 % se as faixas seguirem a codificação padrão
  de indutores axiais; a diferença entre eles recomenda confirmar com um medidor LCR;
- T1 marcado EE16-1.5mH WM; relação de espiras e polaridade ainda desconhecidas;
- potência permanente equivalente = 0,30 W e eficiência = 80 %;
- valores do divisor e da compensação do TL431C/PC817;
- código exato e características de D7; leitura atual “SRII?”;
- topologia da rail de 5 V e função de IC9.

O modelo ngspice médio representa L1/L2 apenas por resistências série de 0,2 Ω, pois
seu objetivo validado é o regime DC. A resposta transitória do filtro deve ser incluída
somente após confirmar as indutâncias e resistências série com um medidor LCR.

Para um modelo chaveado confiável ainda são necessárias a relação de espiras e a
polaridade dos enrolamentos de T1, além dos valores do snubber, do divisor e da
compensação da realimentação.

> **Segurança:** o barramento simulado fica próximo de 310 Vcc e permanece perigoso
> após desligar. Não energize a placa carbonizada diretamente na rede. Ensaios exigem
> isolamento, limitação de corrente, descarga verificada dos eletrolíticos e práticas
> adequadas para alta tensão.
