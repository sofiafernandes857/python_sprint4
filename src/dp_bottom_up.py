from .model import InventoryModel

# Versão iterativa (bottom-up): preenche tabelas V[t][I] e PI[t][I]
def solve_bottom_up(model: InventoryModel):
    T, I_max = model.T, model.I_max

    # Tabelas (t vai de 1..T; criamos T+2 para usar V[T+1]=0)
    V = [[0.0 for _ in range(I_max + 1)] for _ in range(T + 2)]
    PI = [[0 for _ in range(I_max + 1)] for _ in range(T + 1)]

    # Condição terminal: V[T+1][I] = 0 já está


    for t in range(T, 0, -1):
        for I in range(I_max + 1):
            best = float('inf')
            best_a = 0
            for a in model.actions(I):
                c_exp = 0.0
                v_future = 0.0
                for d, p in enumerate(model.pmf):
                    if p == 0.0:
                        continue
                    c_day, I_next, _ = model.immediate_cost_and_nextI(I, a, d)
                    c_exp += p * c_day
                    v_future += p * V[t + 1][I_next]
                total = c_exp + v_future
                if total < best:
                    best = total
                    best_a = a
    V[t][I] = best
    PI[t][I] = best_a


    V0 = V[1][model.I0]
    A0 = PI[1][model.I0]
    return {
        'V': V,
        'PI': PI,
        'V0': V0,
        'A0': A0,
    }