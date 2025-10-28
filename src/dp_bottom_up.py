# src/dp_bottom_up.py
from .model import InventoryModel

def solve_bottom_up(model: InventoryModel):
    """
    Solução iterativa (bottom-up) para a equação de Bellman.

    V[t][I]  = valor ótimo do custo esperado do dia t..T dado estoque I no início de t
    PI[t][I] = ação ótima correspondente

    t: 1..T (usamos V com T+2 linhas para ter V[T+1][*] = 0 como terminal)
    I: 0..I_max
    """
    T, I_max = model.T, model.I_max

    # Tabelas
    V = [[0.0 for _ in range(I_max + 1)] for _ in range(T + 2)]  # V[T+1][I] = 0 já inicializado
    PI = [[0 for _ in range(I_max + 1)] for _ in range(T + 1)]   # PI só precisa até T

    # Preenchimento do fim para o começo
    for t in range(T, 0, -1):
        for I in range(0, I_max + 1):
            best_total = float("inf")
            best_a = 0

            # Sempre deve haver pelo menos a ação '0'
            for a in model.actions(I):
                # custo esperado do dia t dada a ação a
                c_exp = 0.0
                v_future = 0.0

                # Expectativa sobre a demanda discreta
                for d, p in enumerate(model.pmf):
                    if p == 0.0:
                        continue
                    c_day, I_next, _ = model.immediate_cost_and_nextI(I, a, d)
                    c_exp   += p * c_day
                    v_future += p * V[t + 1][I_next]

                total = c_exp + v_future
                if total < best_total:
                    best_total = total
                    best_a = a

            # Segurança: se por algum motivo não entrou no laço (não deveria), mantém 0
            if best_total == float("inf"):
                best_total = 0.0
                best_a = 0

            V[t][I] = best_total
            PI[t][I] = best_a

    V0 = V[1][model.I0]
    A0 = PI[1][model.I0]
    return {"V": V, "PI": PI, "V0": V0, "A0": A0}
