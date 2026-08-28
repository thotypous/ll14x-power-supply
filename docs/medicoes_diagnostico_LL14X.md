# Medições e diagnóstico elétrico — placa LL14X

Período do registro: **24–28/08/2026**

O documento começou como registro da placa desenergizada, com R3 e a trilha
DRAIN–T1 removidos. As seções finais registram a reconstrução e os testes energizados
posteriores.

## 1. Instrumentação e método

- Multímetro simples, com leitura de **0,6 Ω** ao encostar diretamente as pontas.
- Medidor LCR caseiro disponível, mas inadequado para estas medições em circuito; não
  foi usado para evitar dessoldagem.
- Osciloscópio disponível somente com sonda passiva ×10; não há sonda diferencial.
- Não há transformador de isolamento. Posteriormente foi obtida e utilizada uma
  lâmpada incandescente de 40 W como limitador na primeira energização.
- Valores resistivos abaixo devem ser tratados como leituras brutas; a diferença para
  0,6 Ω serve apenas como indicação aproximada, não como medição de precisão.
- Testes de semicondutores feitos no modo diodo, sem dessoldar componentes.
- O display `1` foi registrado como circuito aberto/infinito.
- Todos os resultados são medições em circuito e podem incluir caminhos paralelos.

## 2. Continuidade e resistências

| Ponto/componente | Leitura | Interpretação atual |
|---|---:|---|
| pontas do multímetro em curto | 0,6 Ω | resistência de referência das pontas |
| FUSE1 | 0,6 Ω | continuidade; resistência indistinguível das pontas |
| FUSE2 | 0,6 Ω | continuidade; resistência indistinguível das pontas |
| R3 original | infinito | queimado, aberto e posteriormente removido |
| L1 | 0,7 Ω | continuidade; resistência efetiva muito baixa |
| L2 | 1,5 Ω | continuidade; aproximadamente 0,9 Ω acima das pontas |
| T1, primário | 5,4 Ω | enrolamento contínuo |
| T1, secundário | 0,9 Ω | enrolamento contínuo |
| T1, primário para secundário | >2 MΩ | sem curto detectável na escala disponível |
| DRAIN de IC1 para pino correspondente de T1 | infinito | esperado: trilha danificada foi removida |
| outro terminal do primário de T1 para E1/E2(+) | continuidade | conexão preservada |
| E1(+) para E2(+) | 1,7 Ω estabilizado | terminais interligados; valor bruto |
| E1(−) para E2(−) | 1,0 Ω estabilizado | terminais interligados; valor bruto |

O resultado acima de 2 MΩ em T1 é apenas triagem com multímetro. Não substitui ensaio
de resistência de isolamento em tensão apropriada.

## 3. Ponte DB1 — modo diodo

| Ponta vermelha | Ponta preta | Leitura |
|---|---|---:|
| `−` | AC1 ou AC2 | ≈0,511 V |
| AC1 ou AC2 | `+` | ≈0,480 V |
| quatro sentidos inversos | — | infinito |

Diagnóstico: quatro junções coerentes, sem curto ou abertura detectável.

## 4. Diodos discretos

| Componente | Preta na faixa | Vermelha na faixa | Interpretação |
|---|---:|---:|---|
| D1 | 0,493 V | infinito | junção coerente |
| D2 | 0,498 V | infinito | junção coerente; um terminal esteve na área carbonizada |
| D3 | 0,452 V | infinito | junção coerente |
| D7 | 0,242 V | 1,749 V | queda direta compatível com Schottky; sentido oposto afetado por caminhos paralelos |

O modo diodo não verifica capacidade de bloqueio na tensão real de trabalho.

## 5. IC1 — LNK3604P

| Medição | Leitura |
|---|---:|
| vermelha em SOURCE, preta em DRAIN | 0,424 V |
| vermelha em DRAIN, preta em SOURCE | infinito |

Diagnóstico: comportamento compatível com o diodo interno do MOSFET; não há curto
DRAIN–SOURCE detectável. Isso não comprova chaveamento nem bloqueio em alta tensão.

## 6. Capacitores e rails

### E1/E2

- Vermelha no negativo: E1 = 1,197 kΩ; E2 = 1,199 kΩ, estabilização rápida.
- Polaridade inversa: infinito em ambos.
- Não há curto de baixa resistência detectável no barramento.

### E3

- Vermelha em E3(+): aproximadamente 1 kΩ, subindo para infinito em cerca de 1 s.
- Vermelha em E3(−): 103 Ω, subindo para 402 Ω em menos de 1 s.
- Comportamento compatível com carregamento em circuito; sem curto permanente.

### E4

- Vermelha em E4(+): aproximadamente 600 Ω, subindo para 1,9 kΩ em cerca de 2 s.
- Vermelha em E4(−): 368 Ω, estabilizando próximo de 259 Ω.
- A leitura final provavelmente inclui as cargas conectadas após L1/L2; sem curto de
  poucos ohms.

Esses testes não medem capacitância nem ESR.

## 7. IC2 — PC817

| Medição | Leitura |
|---|---:|
| vermelha pino 1, preta pino 2 | 1,494 V |
| preta pino 1, vermelha pino 2 | 1,128 V |
| vermelha pino 3, preta pino 4 | infinito |
| vermelha pino 4, preta pino 3 | 0,564 V |

Não há curto detectável no LED ou fototransistor. As conduções adicionais são
compatíveis com caminhos paralelos pelo TL431 e pelo FB de IC1. O teste não mede CTR
nem comprova transferência óptica.

## 8. IC3 — TL431C

O terminal central tem continuidade com E4(−) e foi identificado como ânodo (`A`). Os
outros terminais foram denominados provisoriamente `X` e `Y`.

| Ponta vermelha | Ponta preta | Leitura |
|---|---|---:|
| A | X | 0,518 V |
| X | A | 1,589 V, evoluindo para infinito |
| A | Y | 0,607 V |
| Y | A | 1,167 V, evoluindo para infinito |
| X | Y | 1,883 V, evoluindo para infinito |
| Y | X | 0,744 V |

Não há curto entre terminais. O teste passivo não comprova referência de 2,5 V nem
regulação sob polarização.

## 9. Diagnóstico consolidado

### Falha original confirmada

- **R3:** carbonizado, aberto e removido; posteriormente substituído por 33 Ω, 1206.
- **Trilha DRAIN–T1:** carbonizada e removida; posteriormente reconstruída.
- **P01/P02:** ilhas/trilhas danificadas mecanicamente ao retirar os fast-ons;
  posteriormente refeitas e reforçadas.

### Triagem estática favorável

- FUSE1 e FUSE2 com continuidade;
- DB1 com quatro junções coerentes;
- D1, D2, D3 e D7 sem curto/abertura detectável;
- IC1 sem curto DRAIN–SOURCE;
- T1 com primário e secundário contínuos e sem curto detectável entre enrolamentos;
- E1–E4 sem curto de baixa resistência;
- PC817 e TL431 sem curto detectável.

### Limitações que permanecem

- estado elétrico de ZR1;
- capacitância e ESR de E1–E4;
- indutância real de L1/L2 e T1;
- bloqueio em alta tensão de DB1, D1–D3, D7 e IC1;
- CTR do PC817 e regulação do TL431;
- resistência de isolamento em tensão apropriada;
- resistência de contato de P01/P02 medida em miliohms; seu funcionamento sob carga,
  contudo, foi confirmado pelo teste do aquecedor.

## 10. Condições usadas na primeira energização

Antes da energização, R3 e DRAIN–T1 foram reconstruídos e repetiram-se as verificações
de continuidade e ausência de curtos. O primeiro teste utilizou lâmpada incandescente
de 40 W em série. A lâmpada limitou a corrente, mas não forneceu isolamento
galvânico; a sonda passiva ×10 não foi conectada ao primário.

## 11. Testes funcionais posteriores

| Teste | Resultado | Conclusão limitada |
|---|---:|---|
| alimentação da bobina de RY5, terminal superior de D9 para GND | ≈12,8 Vcc | rail da bobina presente |
| NTC medido pelo conector da placa | 12,1 kΩ | valor plausível em temperatura ambiente |
| bobina de RY5 | ≈270 Ω | enrolamento contínuo |
| P01–P02 durante a fase de aquecimento, desconectados do chicote | continuidade | comando, Q9, bobina, contato e trilhas fecham no estado reparado |
| fluxostato durante circulação, desconectado eletricamente | continuidade | contato fecha sob circulação real |
| tensão diretamente na resistência, máquina remontada | **123 Vca RMS** | cadeia completa fornece tensão de rede ao aquecedor |
| temperatura após alguns minutos no programa Pesado | parede externa da cuba claramente quente | aquecimento efetivo confirmado |

Os primeiros ensaios em que a água pareceu fria duraram pouco tempo de circulação e
não demonstram que o aquecedor estivesse inoperante. Como P01/P02 foram refeitos antes
dos testes conclusivos, também não é possível atribuir retrospectivamente uma falta
de aquecimento ao reparo anterior. O reforço foi, ainda assim, necessário para uma
conexão que conduz aproximadamente 9 A: continuidade em baixa corrente não comprova
capacidade de condução sob carga.

Estado atual: **fonte e aquecimento funcionando na máquina**. Ainda convém inspecionar
P01/P02, fast-ons e RY5 após um ciclo completo para detectar aquecimento localizado,
odor ou escurecimento.
