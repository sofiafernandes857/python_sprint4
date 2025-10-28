# src/dp_recursive.py
from functools import lru_cache
from .model import InventoryModel

def solve_recursive(model: InventoryModel, use_memo: bool = False):
    """
    Solver recursivo da equação de Bellman.
    - use_memo=False: sem cache (muito lento em instâncias médias/grandes — apenas didático)
    - use_memo=True: com cache ilimitado (rápido)
    """
    T = model.T

    # decorator de identidade (não faz cache)
    def _identity(f):
        return f

    decorator = lru_cache(maxsize=None) if use_memo else _identity

    @decorator
    def V(t: int, I: int):
        # condição terminal
        if t == T + 1:
            return 0.0, 0

        best = float("inf")
        best_a = 0

        for a in model.actions(I):
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

    v0, a0 = V(1, model.I0)
    return {"value_fn": V, "V0": v0, "A0": a0}
