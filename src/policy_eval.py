from typing import List, Dict
from .model import InventoryModel

# Simula a execução de uma política PI[t][I] ao longo de uma sequência de demandas
def simulate_policy(model: InventoryModel, PI: List[List[int]], demands: List[int]) -> Dict:
    I = model.I0
    total_cost = 0.0
    traj = []
    for t, d in enumerate(demands, start=1):
        a = PI[min(t, model.T)][I] # trava no último t se demands > T
        c_day, I_next, shortage = model.immediate_cost_and_nextI(I, a, d)
        total_cost += c_day
        traj.append({
            't': t,
            'I': I,
            'a': a,
            'd': d,
            'shortage': shortage,
            'I_next': I_next,
            'cost': c_day,
        })
        I = I_next
    return {'total_cost': total_cost, 'trajectory': traj}