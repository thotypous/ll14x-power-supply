# Firmware e compatibilidade da placa LL14X

| Campo | Identificação |
|---|---|
| Máquina analisada | Electrolux LL14X, rede de 127 V |
| PCB | `WQP12-7601S.D.1-1 V1.1` |
| Número impresso do módulo | `17176000033271` |
| MCU | SinoWealth SH79F6484P, Flash interna de 64 KB |
| Estado desta nota | levantamento documental; não há dump da Flash da placa |

## Conclusão operacional

Não há evidência de que placas de reposição dessa família sejam entregues virgens ou
exijam que o comprador copie firmware após a instalação. A evidência disponível aponta
para módulos que já saem **programados de fábrica**, selecionados por referência de
peça e modelo compatível.

Isso não demonstra que todas as placas `WQP12-7601S.D.1-1` usem o mesmo binário. A
conclusão prudente é que a plataforma de hardware é compartilhada por várias marcas,
mas que podem existir firmwares ou configurações distintos por número completo de
módulo, revisão, tensão de rede, painel e conjunto de cargas.

## Evidências de compatibilidade e programação

### Reposição programada de fábrica

Um anúncio da SEMBoutique, publicado no marketplace Leroy Merlin, descreve o módulo
`WQP12-7601.D.1` como **«programmé d'origine en usine»**: programado originalmente na
fábrica. O item é associado a modelos específicos Valberg e Saba, e o vendedor pede
que a compatibilidade seja validada antes da compra.

Fonte: [Module Wqp12-7601.d.1 — Leroy Merlin / SEMBoutique](https://www.leroymerlin.fr/produits/module-wqp12-7601-d-1-86922626.html).

Essa é a melhor evidência direta contra a hipótese de uma placa virgem cuja Flash
precise ser clonada pelo instalador.

### Reposição por número completo de peça

Um distribuidor espanhol comercializa um módulo original como substituto explícito das
referências:

```text
WQP12-7601S.D.1-1 V1.0 / 17176000032251
WQP12-7601S.D.1-1 V1.0 / 17176000033271
```

Ele lista compatibilidade com máquinas EAS Electric, HighOne e Johnson. Não há etapa
de gravação ou cópia de firmware indicada para a substituição.

Fonte: [Módulo de potência 10639 — Centro Técnico Murcia](https://centrotecnicomurcia.com/index.php?id_product=10639&controller=product).

### A referência `17176000033271` aparece sob outras marcas

O mesmo número de módulo da placa analisada é vendido como peça Danby/Midea. O
catálogo Danby ainda registra uma referência de reposição mais recente,
`17176000001256`, para a peça `17176000033271`.

Fonte: [Danby Dishwasher Control Board 17176000033271 — Provencher Appliance](https://provencherappliance.ca/product/danby-dishwasher-control-board-17176000033271/).

Isso confirma compartilhamento comercial da mesma peça entre marcas, mas não prova
que todo PCB visualmente semelhante seja intercambiável.

### O PCB é uma plataforma Midea compartilhada

O manual de serviço Midea para a placa identifica `WQP12-7601S.D.1-1 V1.0`, número
`17176000022803`, e a mesma nomenclatura funcional dos conectores e cargas: `P01/P02`
(aquecimento), `EV1`, `PS`, `ML-H`, `ML-L`, `RE`, `FM`, `TURB` etc. O manual também
avisa que pode haver pequenas diferenças de posição entre modelos, embora as marcações
tenham o mesmo significado.

Fonte: [Manual de serviço Midea MDWEF1433D](https://www.midea.com/content/dam/midea-aem/fr/fr-new/pdp/guide-de-r%C3%A9paration/Service-manual-MDWEF1433D-SS-W.pdf).

## Implicações para compra de reposição

| Situação | Avaliação |
|---|---|
| Mesma referência `17176000033271` | Melhor opção; deve vir pronta para instalar. |
| Supersessão declarada por catálogo de peças | Provável substituição direta, desde que o catálogo associe o modelo da máquina. |
| Mesmo texto de PCB, mas outro número `171…` ou outra revisão | Não assumir compatibilidade; pode haver firmware/configuração de outra variante. |
| Anúncio genérico que só diz `WQP12-7601S` | Insuficiente. Pedir confirmação escrita de compatibilidade com LL14X e `17176000033271`. |
| Placa usada retirada de máquina identificada pelo mesmo número | Pode ser uma alternativa válida; confirmar revisão, conectores e tensão antes de instalar. |

O número completo de módulo deve prevalecer sobre a marca estampada no eletrodoméstico.
No caso desta máquina, a identidade de compra a informar ao vendedor é:

```text
Electrolux LL14X, 127 V
WQP12-7601S.D.1-1 V1.1
17176000033271
```

## Relação com o firmware do SH79F6484P

O SH79F6484P possui Flash interna de 64 KB e suporta interface de depuração/programação
SWE/JTAG. A SinoWealth documenta suporte a leitura e gravação pela ferramenta própria,
mas a proteção de leitura pode impedir a extração da Flash quando ativada.

Fonte: [SH79F6484 — SinoWealth](https://en.sinowealth.com/detaile?pro_id=18).

Há um relato público de extração de 64 KB de firmware por JTAG de outro equipamento
que usava exatamente o SH79F6484. Esse relato mostra que uma unidade **sem proteção de
leitura ativa** pode ser lida em circuito; ele não demonstra vulnerabilidade capaz de
contornar proteção ativa.

Fontes: [relato do equipamento Hisense](https://lb.lax.hackaday.io/project/204087/logs?page=1&sort=oldest) e [POC de leitura SinoWealth 8051](https://github.com/gashtaan/sinowealth-8051-dumper).

Um dump desta placa seria útil para preservação, comparação entre revisões e engenharia
reversa. Não há, contudo, evidência de que seja necessário gravá-lo em uma reposição
oficial correta: as evidências de mercado apontam para placas de reposição já
programadas.

## Limites deste levantamento

- Não foi encontrada documentação pública da Electrolux que associe o hash/binário do
  firmware a cada código `171…`.
- Não foi localizado procedimento de configuração de campo da Electrolux para essa
  placa após a troca.
- A ausência de relatos de clonagem não prova que não existam variantes; ela apenas
  indica que clonagem não é o procedimento normal de reposição disponível ao público.
- Não se deve comprar uma placa apenas pelo desenho, pelo número de relés ou pela
  inscrição parcial `WQP12-7601S`.
