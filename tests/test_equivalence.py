import math
from src.model import InventoryModel
from src.dp_recursive import solve_recursive
from src.dp_memo import solve_memoized
from src.dp_bottom_up import solve_bottom_up

# Teste simples garantindo que as três abordagens concordam
def test_equivalence_small():
    model = InventoryModel(
        T=5,
        I_max=10,
        A_max=5,
        I0=3,
        K=1.0,
        c=1.0,
        h=0.1,
        s=2.0,
        pmf=[0.3, 0.4, 0.3], # demanda 0,1,2
    )

    rec = solve_recursive(model, use_memo=False)
    mem = solve_memoized(model)
    bot = solve_bottom_up(model)

    assert math.isclose(rec['V0'], mem['V0'], rel_tol=1e-9, abs_tol=1e-9)
    assert math.isclose(bot['V0'], mem['V0'], rel_tol=1e-9, abs_tol=1e-9)

    # Também compara a primeira ação ótima
    assert rec['A0'] == mem['A0'] == bot['A0']