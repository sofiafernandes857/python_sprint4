from .model import InventoryModel
from .dp_recursive import solve_recursive
from .dp_memo import solve_memoized
from .dp_bottom_up import solve_bottom_up
from .policy_eval import simulate_policy

# Exemplo pronto para rodar: python -m src.run_example
def main():
    # Parâmetros padrão (fáceis de entender e alterar)
    T = 10
    I_max = 20
    A_max = 10
    I0 = 5

    # custos
    K = 2.0 # custo fixo por pedido
    c = 1.0 # custo unitário
    h = 0.2 # holding (manter estoque)
    s = 3.0 # falta (penalidade por unidade não atendida)

    # demanda discreta simples (0..4) com probabilidades
    pmf = [0.10, 0.20, 0.30, 0.25, 0.15]

    model = InventoryModel(T, I_max, A_max, I0, K, c, h, s, pmf)

    print("== Rodando soluções ==")
    rec = solve_recursive(model, use_memo=False)
    mem = solve_memoized(model)
    bot = solve_bottom_up(model)

    print(f"Recursiva (quase sem cache) V0={rec['V0']:.4f} A0={rec['A0']}")
    print(f"Recursiva+Memo V0={mem['V0']:.4f} A0={mem['A0']}")
    print(f"Bottom-up V0={bot['V0']:.4f} A0={bot['A0']}")

    # Checagens simples de equivalência (tolerância numérica)
    assert abs(rec['V0'] - mem['V0']) < 1e-6
    assert abs(bot['V0'] - mem['V0']) < 1e-6

    # Simulação de uma trajetória de demandas
    demands = [2, 3, 1, 4, 0, 2, 2, 3, 1, 4]
    sim = simulate_policy(model, bot['PI'], demands)
    print("\n== Simulação com política ótima (bottom-up) ==")
    print(f"Custo total na simulação: {sim['total_cost']:.4f}")
    print("Primeiros 5 dias (t, I, a, d, falta, I_next, cost):")
    for row in sim['trajectory'][:5]:
        print(row['t'], row['I'], row['a'], row['d'], row['shortage'], row['I_next'], f"{row['cost']:.2f}")

if __name__ == "__main__":
    main()