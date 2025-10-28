from .dp_recursive import solve_recursive
from .model import InventoryModel

# Versão recursiva com memorização é a mesma função com cache amplo
def solve_memoized(model: InventoryModel):
    return solve_recursive(model, use_memo=True)