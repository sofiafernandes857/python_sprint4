PD para Reposição de Insumos em Unidades de Diagnóstico — Relatório Explicativo (Passo a Passo)


1) Contexto e Objetivo

Em unidades de diagnóstico, o consumo diário de insumos (reagentes e descartáveis) oscila conforme a demanda de exames. Sem registro preciso, o planejamento de estoque fica frágil: ora falta material (atrasos/SLA), ora sobra (dinheiro parado/validade). Nosso objetivo é decidir quanto comprar por dia para minimizar o custo total de operação, equilibrando:

- Faltas (penalidade por não atender toda a demanda),

- Excesso (custo de manter estoque),

- Pedido (custo fixo e unitário ao comprar).

Usamos Programação Dinâmica (PD) porque é um problema de decisão sequencial no tempo: a decisão de hoje afeta o amanhã (estoque futuro e custos).

2) Formulação do Problema 
3.1 Estado (o que precisamos saber no dia t)

I_t = estoque disponível no início do dia t.

3.2 Decisão (o que podemos fazer no dia t)

a_t = quantidade a comprar no início do dia t (antes do consumo). A compra pode ter custo fixo K (se comprar qualquer quantidade) e custo unitário c por unidade comprada.

3.3 Demanda (o que será consumido no dia t)

D_t = consumo do dia t. Modelamos como distribuição discreta (PMF) sobre {0, 1, 2, ..., D_max}, parametrizada em pmf (ver run_example.py). Isso permite calcular custos esperados de forma simples (média ponderada pelas probabilidades).

3.4 Transição (como o estoque evolui de hoje para amanhã)

Intuição:

estoque_amanha = max(0, estoque_hoje + comprado_hoje - consumido_hoje)

Em símbolos:
I_{t+1} = max(0, I_t + a_t - D_t)
Se a demanda for maior que o disponível (I_t + a_t < D_t), ocorre falta shortage = D_t - (I_t + a_t).

3.5 Função de custo do dia

Pedido: K (se a_t > 0) + c * a_t.

Estoque (holding): h * I_{t+1}.

Falta (shortage): s * max(0, D_t - (I_t + a_t)).

3.6 Objetivo (o que otimizamos)

Minimizar a soma dos custos esperados ao longo dos T dias. Em linguagem da PD, definimos a função valor V(t, I) como o melhor custo possível do dia t até o final, se hoje temos I em estoque:

V(t, I) = min_a  E_D[  custo_do_dia(I, a, D) + V(t+1, I_amanha)  ]
com V(T+1, I) = 0

De onde veio isso? É a equação de Bellman, que formaliza o raciocínio “custo de hoje + melhor custo futuro”. Nosso código simplesmente implementa essa equação de três jeitos diferentes.

3) Do Modelo para o Código (mapeamento direto)

src/model.py
Define a estrutura do problema (parâmetros, espaço de estados/ações, custos e transição).
Funções-chave:

actions(I): quais compras são possíveis dado o estoque I (respeitando capacidade).

immediate_cost_and_nextI(I, a, d): dado I, ação a e demanda d, retorna custo do dia, I_{t+1} e falta.

O custo esperado é calculado somando custos por cada d ponderados por pmf[d].

src/dp_recursive.py
Implementa a equação de Bellman recursivamente. A função solve_recursive(..., use_memo=False) calcula V(t, I) via chamada recursiva. Com use_memo=True, liga-se um cache (memorização) para não recalcular subproblemas iguais.

src/dp_memo.py
Apenas expõe a versão recursiva com memorização.

src/dp_bottom_up.py
Implementa a solução iterativa (bottom-up): preenche tabelas V[t][I] e PI[t][I] do fim para o começo, escolhendo a ação de menor custo esperado em cada par (t, I).

src/policy_eval.py
Dada uma política ótima PI (tabela de ações), simula um cenário específico de demandas e registra a trajetória (estoque, faltas, custos por dia). Serve para interpretação prática.

src/run_example.py
Roteiro reprodutível: configura um cenário, roda as três soluções, checa equivalência de resultados e simula a política para uma sequência exemplo de demandas.

4) As Três Abordagens — por que existem e quando usar

Recursiva (top-down)
Espelha literalmente a equação de Bellman e é a mais didática. Porém, sem cache, recalcula muitos subproblemas.

Recursiva com Memorização
Igual à recursiva, mas com cache (armazenamento dos resultados de V(t, I)) para evitar recomputações. Em geral, já é bem eficiente para problemas de porte médio.

Iterativa (bottom-up)
Constrói V e PI começando de t = T até t = 1. O controle da ordem de cálculo e o uso de tabelas a tornam previsível e rápida — ótima para produção.

Resultado esperado: todas retornam o mesmo custo ótimo e a mesma ação ótima para o estado inicial, confirmando correção.

5) Garantia de Equivalência (o que prova que está certo)

Testes automatizados em tests/test_equivalence.py comparam o custo ótimo inicial (V0) e a primeira ação (A0) entre recursiva, memo e bottom-up, com tolerâncias numéricas apertadas.

Checagens adicionais em run_example.py usam assert para reforçar a equivalência.

Isso comprova o item “Garantir que ambas produzam os mesmos resultados (15 pts)” da atividade.

6) Estrutura do Repositório e Execução
.
├── README.md
├── requirements.txt
├── .gitignore
├── src/
│   ├── model.py
│   ├── dp_recursive.py
│   ├── dp_memo.py
│   ├── dp_bottom_up.py
│   ├── policy_eval.py
│   └── run_example.py
└── tests/
    └── test_equivalence.py

Como rodar:

python -m venv .venv
source .venv/bin/activate   # Windows: .venv/Scripts/activate
pip install -r requirements.txt
python -m src.run_example

Como rodar testes:

pytest -q
7) Parâmetros, Suposições e Como Personalizar

Horizonte: T dias (ex.: 10).

Capacidade de tabelas: I_max (estoque até onde avaliamos) e A_max (máximo que se pode comprar num dia).

Custos: K (fixo por pedido), c (unitário), h (manter estoque), s (falta).

Demanda: pmf discreta (vetor que soma 1).

Para casos reais, ajuste pmf a partir de dados históricos (média/variância por dia ou sazonalidade) e calibração de custos com a área financeira/operacional.

8) Interpretação dos Resultados

V0 = custo ótimo esperado do horizonte, partindo de I0.

A0 = quantidade ótima a comprar hoje dado I0.

A tabela PI[t][I] (output do bottom-up) fornece a política ótima: para cada dia e estoque, qual compra fazer.

Com policy_eval.py, é possível simular a política em sequências específicas de demanda (reais ou sintéticas) e visualizar impactos em faltas e estoque.

9) Limitações e Extensões

Sem lead time (pedidos chegam no mesmo dia). Extensão natural: adicionar fila de recebimentos ao estado.

Sem backorder (não cumulamos falta para atender depois). Extensão: permitir backorder e ajustar custos/transição.

Item único. Extensão: múltiplos itens via decomposição por item (se independentes) ou heurísticas.

Demanda discreta i.i.d. Extensão: sazonalidade, dias da semana, ou demanda condicionada a volume de exames.

10) FAQ — de onde vêm as fórmulas?

Equação de Bellman: é a formalização do raciocínio “decida hoje pensando no custo de hoje + melhor custo futuro”.

Custo esperado: como a demanda é incerta, somamos custos ponderados pelas probabilidades em pmf.

Transição I_{t+1}: é contabilidade de estoque (entra compra, sai consumo, não pode ficar negativo se não modelamos backorder).
