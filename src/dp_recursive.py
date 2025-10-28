from functools import lru_cache
from .model import InventoryModel


# Versão recursiva "pura". Usamos lru_cache controlada
# Para comportar-se como a versão recursiva com/sem memo variando o maxsize.


def solve_recursive(model: InventoryModel, use_memo: bool = False):
    T, I_max = model.T, model.I_max


    def _cache(maxsize=None):
        def deco(func):
            return lru_cache(maxsize=maxsize)(func)
        return deco

    maxsize = None if use_memo else 1


    @_cache(maxsize=maxsize)
    def V(t: int, I: int):
        if t == T + 1:
            return 0.0, 0 # custo futuro 0, ação nula
        best = float('inf')
        best_a = 0
        for a in model.actions(I):
            # custo esperado do dia
            c_exp = 0.0
            v_future = 0.0
            for d, p in enumerate(model.pmf):
                if p == 0.0:
                    continue
                c_day, I_next, _ = model.immediate_cost_and_nextI(I, a, d)
                v_next, _ = V(t + 1, I_next)
                c_exp += p * c_day
                v_future += p * v_next
            total = c_exp + v_future
            if total < best:
                best = total
                best_a = a
        return best, best_a


    # custo e ação ótimos iniciais
    v0, a0 = V(1, model.I0)
    return {
        'value_fn': V, # callable: V(t,I)->(valor,acao)
        'V0': v0,
        'A0': a0,
    }