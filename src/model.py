from typing import List, Tuple

class InventoryModel:
    def __init__(
        self,
        T: int,
        I_max: int,
        A_max: int,
        I0: int,
        K: float, # custo fixo de pedido
        c: float, # custo unitário
        h: float, # custo de manter estoque 
        s: float, # custo de falta 
        pmf: List[float], # distribuição discreta de D em {0,1,...,D_max}
    ):
        assert T >= 1
        assert 0 <= I0 <= I_max
        assert len(pmf) >= 1
        assert abs(sum(pmf) - 1.0) < 1e-8, "PMF deve somar 1"
        self.T = T
        self.I_max = I_max
        self.A_max = A_max
        self.I0 = I0
        self.K = K
        self.c = c
        self.h = h
        self.s = s
        self.pmf = pmf
        self.D_max = len(pmf) - 1


    def states(self):
        return range(0, self.I_max + 1)


    def actions(self, I: int):
        max_a = min(self.A_max, self.I_max - I)
        return range(0, max_a + 1)


    def immediate_cost_and_nextI(self, I: int, a: int, d: int):
        order_cost = (self.K if a > 0 else 0.0) + self.c * a
        available = I + a
        shortage = max(0, d - available)
        I_next = max(0, available - d)
        holding_cost = self.h * I_next
        shortage_cost = self.s * shortage
        total_cost = order_cost + holding_cost + shortage_cost
        return total_cost, I_next, shortage



    def expected_cost_and_next(self, I: int, a: int) -> float:
        # custo esperado do dia dado ação a
        exp_cost = 0.0
        for d, p in enumerate(self.pmf):
            if p == 0.0:
                continue
            c_day, I_next, _ = self.immediate_cost_and_nextI(I, a, d)
            exp_cost += p * c_day
        return exp_cost