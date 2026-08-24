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

## Simulações

Execute a partir da raiz do repositório:

```bash
python3 modelos/sim_fonte.py
python3 modelos/sim_fonte.py --waveform
ngspice -b modelos/fonte_chaveada_LL14X.cir
```

O modo `--waveform` grava `resultados/ll14x_ondas.csv`; o ngspice grava
`resultados/ll14x_fonte.dat`.

> **Segurança:** os modelos incluem um barramento próximo de 310 Vcc. Não energize
> a placa carbonizada diretamente na rede. Ensaios físicos exigem isolamento,
> limitação de corrente e procedimentos adequados para alta tensão.
