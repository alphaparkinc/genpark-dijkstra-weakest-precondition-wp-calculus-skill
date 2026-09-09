"""
Demonstration of Dijkstra's Weakest Precondition (wp) Calculus Skill
"""

from client import WeakestPreconditionEngine

def main():
    print("=== Dijkstra's Weakest Precondition (wp) Calculus Demonstration ===")
    wp_engine = WeakestPreconditionEngine()

    # Program: x := x + 1; y := x * 2
    # Desired Postcondition Q: y >= 10
    # Backward wp derivation:
    #   wp(y := x * 2, y >= 10) <=> x * 2 >= 10 (x >= 5)
    #   wp(x := x + 1, x >= 5)  <=> x + 1 >= 5  (x >= 4)
    stmts = [
        ("x", lambda s: s["x"] + 1),
        ("y", lambda s: s["x"] * 2)
    ]
    postcondition_q = lambda s: s["y"] >= 10

    synthesized_wp = wp_engine.wp_sequence(stmts, postcondition_q)

    print("Evaluating Synthesized Weakest Precondition:")
    # Boundary test 1: x = 4 -> should satisfy wp
    res_4 = synthesized_wp({"x": 4, "y": 0})
    print(f"  State {{x: 4}} satisfies wp: {res_4}")
    assert res_4 is True

    # Boundary test 2: x = 3 -> should NOT satisfy wp
    res_3 = synthesized_wp({"x": 3, "y": 0})
    print(f"  State {{x: 3}} satisfies wp: {res_3}")
    assert res_3 is False

    print("\nWeakest Precondition Calculus Verification PASS!")

if __name__ == "__main__":
    main()
