#!/usr/bin/env python3
"""Simulador do subsistema de fonte chaveada da placa LL14X / LC14S
(PCB WQP12-7601S.D.1-1 V1.1) — flyback com IC1 = LNK3604P.

Frente de rede integrada por backward-Euler (L-estável) via MNA linear por
trechos; flyback representado por balanço médio de potência com controle PI.
Sem Newton/SPICE: passo fixo e comportamento numérico reprodutível.

Topologia funcional inferida das fotos (mesmas hipóteses do netlist ngspice):
  CON1 -> FUSE1/FUSE2 -> ZR1 // C1(X2) // R(51k) -> R3 -> DB1
  -> equivalência concentrada de E1/L1/L2/E2
  -> T1 (flyback 1,5 mH) -> IC1 (chave 66 kHz)
  -> D7 -> E3 (saída modelada em 12 V; ligação de E4 ainda não rastreada)
  -> IC3 (TL431C) -> IC2 (PC817) -> realimentação isolada de IC1.

Uso:  python3 modelos/sim_fonte.py             -> tensões de regime
      python3 modelos/sim_fonte.py --waveform  -> grava resultados/ll14x_ondas.csv
"""
import sys

from pathlib import Path

import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RESULTS_DIR = PROJECT_ROOT / "resultados"

# ----------------------------------------------------------------------------
# Parâmetros (mesmas suposições do netlist ngspice; R3 lido da placa: 33R0)
# ----------------------------------------------------------------------------
F = 60.0
VPK = 127.0 * np.sqrt(2)
FSW = 66.7e3                      # LNK3604 ~66 kHz
LP = 1.5e-3                       # T1 marcado “EE16-1.5mH WM”
ILIM = 0.40                       # limite de corrente ciclo-a-ciclo LNK3604
ETA = 0.80                        # eficiência típica
R3 = 33.0                         # SMD "33R0"
RFUS = 0.05
RBLD = 51e3
C_X2 = 0.22e-6
C_E12 = 4.7e-6 + 4.7e-6           # equivalência concentrada de E1/L1/L2/E2
C_OUT = 680e-6                     # E3; ligação de E4 ainda não rastreada
C_SNS = 10e-6
R_SNS = 1e3
P_MAX = 0.5 * LP * ILIM ** 2 * FSW   # ~8 W; ILIM ainda é estimado
RL12, RL12B = 1.2e3, 22e3
VCLAMP = 390.0                    # varistor ZR1 (471K típico)
VD = 0.7
RD_ON = 1.0
RD_OFF = 1e9

DT = 0.5e-6
TSTOP = 60e-3

N = ["nL1", "nN1", "nz", "a1", "a2", "vb", "v12", "vsense"]
IX = {n: i for i, n in enumerate(N)}
M = len(N)


def main():
    steps = int(TSTOP / DT)
    v = np.zeros(M)
    v[IX["vb"]] = 170.0
    v[IX["v12"]] = 12.0
    v[IX["vsense"]] = 12.0
    # O histórico dos capacitores deve ser coerente com as condições iniciais.
    # Inicializá-lo em zero cria um degrau artificial, sobretudo em VSENSE, que
    # carrega indevidamente o integrador do laço durante os primeiros passos.
    H = {"x2": 0.0, "vb": 170.0, "v12": 12.0, "sns": 12.0}
    st = {k: False for k in ("db1", "db2", "db3", "db4", "z1", "z2")}
    p_int = 0.0                   # integrador do laço (PI)
    rec = "--waveform" in sys.argv
    acc = {k: [] for k in ("t", "vb", "v12")}


    sums = {"vb": 0.0, "v12": 0.0}
    n_avg = 0

    for it in range(steps):
        t = it * DT
        vac = VPK * np.sin(2 * np.pi * F * t)
        G = np.zeros((M, M))
        I = np.zeros(M)

        def r(a, b, g):
            if a >= 0:
                G[a, a] += g
            if b >= 0:
                G[b, b] += g
            if a >= 0 and b >= 0:
                G[a, b] -= g
                G[b, a] -= g

        def cap(a, b, c, h):
            g = c / DT
            r(a, b, g)
            if a >= 0:
                I[a] += g * h
            if b >= 0:
                I[b] -= g * h

        def diode(d, a, b):
            on = st[d]
            g = 1 / RD_ON if on else 1 / RD_OFF
            r(a, b, g)
            if on:
                if a >= 0:
                    I[a] += g * VD
                if b >= 0:
                    I[b] -= g * VD

        # ---- frente de rede ----
        G[IX["nL1"], IX["nL1"]] += 1 / RFUS          # FUSE1 até a fonte vac
        I[IX["nL1"]] += vac / RFUS
        r(IX["nN1"], -1, 1 / RFUS)                   # FUSE2
        # varistor ZR1: dois diodos antissérie com joelho VCLAMP
        for d, a, b in (("z1", IX["nL1"], IX["nz"]),
                        ("z2", IX["nN1"], IX["nz"])):
            on = st[d]
            g = 1 / 5.0 if on else 1 / RD_OFF
            r(a, b, g)
            if on:
                s = 1.0 if v[a] - v[b] > 0 else -1.0
                I[a] += g * s * VCLAMP
                I[b] -= g * s * VCLAMP
        r(IX["nL1"], IX["nN1"], 1 / RBLD)
        r(IX["nL1"], IX["a1"], 1 / R3)
        r(IX["nN1"], IX["a2"], 1 / 0.01)
        diode("db1", IX["a1"], IX["vb"])
        diode("db2", IX["a2"], IX["vb"])
        diode("db3", -1, IX["a1"])
        diode("db4", -1, IX["a2"])
        r(IX["vb"], -1, 1 / 10e6)
        r(IX["v12"], -1, 1 / RL12)
        r(IX["v12"], -1, 1 / RL12B)
        r(IX["v12"], IX["vsense"], 1 / R_SNS)

        cap(IX["nL1"], IX["nN1"], C_X2, H["x2"])
        cap(IX["vb"], -1, C_E12, H["vb"])
        cap(IX["v12"], -1, C_OUT, H["v12"])
        cap(IX["vsense"], -1, C_SNS, H["sns"])

        # ---- flyback em modelo médio (balanço de energia por ciclo) ----
        err = 12.0 - v[IX["vsense"]]
        p_int = np.clip(p_int + DT * 2.0 * err, 0.0, P_MAX)
        # 0,30 W aproxima a carga permanente; o termo proporcional representa
        # IC3/IC2/FB; o integrador elimina o erro estático sem modelar a
        # compensação não identificável nas fotos.
        p_out = np.clip(0.30 + 20.0 * err + p_int, 0.0, P_MAX)
        vb_now = max(v[IX["vb"]], 50.0)
        i_in = p_out / (ETA * vb_now)      # corrente média sacada do bulk
        I[IX["vb"]] -= i_in
        I[IX["v12"]] += p_out / max(v[IX["v12"]], 3.0)

        v = np.linalg.solve(G, I)

        def idiode(d, a, b):
            va = v[a] if a >= 0 else 0.0
            vb = v[b] if b >= 0 else 0.0
            if st[d]:
                i = (va - vb - VD) / RD_ON
                st[d] = i > 0.0          # desliga por corrente reversa
            else:
                st[d] = va - vb > VD     # liga por polarização direta
        idiode("db1", IX["a1"], IX["vb"])
        idiode("db2", IX["a2"], IX["vb"])
        idiode("db3", -1, IX["a1"])
        idiode("db4", -1, IX["a2"])
        st["z1"] = abs(v[IX["nL1"]] - v[IX["nz"]]) > VCLAMP * 0.9
        st["z2"] = abs(v[IX["nN1"]] - v[IX["nz"]]) > VCLAMP * 0.9

        H["x2"] = v[IX["nL1"]] - v[IX["nN1"]]
        H["vb"] = v[IX["vb"]]
        H["v12"] = v[IX["v12"]]
        H["sns"] = v[IX["vsense"]]

        if t > 40e-3:
            for k in sums:
                sums[k] += v[IX[k]]
            n_avg += 1
        if rec and it % 20 == 0:
            acc["t"].append(t * 1e3)
            for k in ("vb", "v12"):
                acc[k].append(v[IX[k]])

    print(f"VB   barramento primário equivalente : {sums['vb'] / n_avg:7.1f} V méd")
    print(f"V12  saída secundária modelada (E3)  : {sums['v12'] / n_avg:7.2f} V méd")
    if rec:
        import csv
        RESULTS_DIR.mkdir(exist_ok=True)
        output_path = RESULTS_DIR / "ll14x_ondas.csv"
        with output_path.open("w", newline="") as f:
            wr = csv.writer(f)
            wr.writerow(["t_ms", "vb", "v12"])
            for i in range(len(acc["t"])):
                wr.writerow([f"{acc['t'][i]:.3f}", f"{acc['vb'][i]:.1f}",
                             f"{acc['v12'][i]:.2f}"])
        print(f"gravado: {output_path.relative_to(PROJECT_ROOT)}")


if __name__ == "__main__":
    main()
