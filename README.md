# Análise da placa Electrolux LL14X

Documentação e modelos do subsistema de fonte chaveada da placa
WQP12-7601S.D.1-1 V1.1, usada na lava-louças Electrolux LL14X e em placas da mesma
família.

## Estrutura

- `docs/`: descrição dos danos e análise elétrica da fonte;
- `modelos/`: netlist ngspice e simulador independente em Python;
- `imagens/originais/`: fotografias da placa danificada;
- `imagens/referencias/`: imagens de placas usadas para comparação visual;
- `resultados/`: saídas reproduzíveis das simulações, não versionadas.

## Documentos

- [Danos visíveis](docs/danos_placa_LL14X.md)
- [Subsistema da fonte chaveada](docs/fonte_chaveada_LL14X.md)
- [Medições e diagnóstico elétrico](docs/medicoes_diagnostico_LL14X.md)
- [Diagrama dos relés e do aquecimento](docs/diagrama_controle_reles_aquecimento_LL14X.md)
- [Firmware e compatibilidade da placa](docs/firmware_e_compatibilidade_placa_LL14X.md)

## Simulações

Execute a partir da raiz do repositório:

```bash
python3 modelos/sim_fonte.py
python3 modelos/sim_fonte.py --waveform
ngspice -b modelos/fonte_chaveada_LL14X.cir
```

O modo `--waveform` grava `resultados/ll14x_ondas.csv`; o ngspice grava
`resultados/ll14x_fonte.dat`.

> **Segurança:** os modelos incluem um barramento de alta tensão. A placa foi
> reconstruída e testada, mas ensaios físicos continuam envolvendo a rede elétrica.
> Uma lâmpada em série limita corrente e não fornece isolamento galvânico; uma sonda
> passiva de osciloscópio não deve ser conectada ao primário sem isolamento e técnica
> de medição apropriados.
