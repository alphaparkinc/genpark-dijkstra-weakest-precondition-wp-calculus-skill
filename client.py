"""
Dijkstra's Weakest Precondition (wp) Calculus Skill Client
Pure Python Standard Library implementation of Dijkstra's predicate transformer calculus.
Propagates postconditions backwards through assignment sequences and conditional branches
to synthesize the necessary and sufficient weakest precondition ensuring valid termination.
"""

from typing import Dict, Any, Callable, List, Tuple


class WeakestPreconditionEngine:
    def wp_assign(
        self,
        var: str,
        expr_fn: Callable[[Dict[str, Any]], Any],
        postcond: Callable[[Dict[str, Any]], bool]
    ) -> Callable[[Dict[str, Any]], bool]:
        """Axiom of Assignment: wp(x := E, Q) = Q[x -> E]."""
        def wp_fn(state: Dict[str, Any]) -> bool:
            next_state = dict(state)
            next_state[var] = expr_fn(state)
            return postcond(next_state)
        return wp_fn

    def wp_sequence(
        self,
        stmts: List[Tuple[str, Callable[[Dict[str, Any]], Any]]],
        postcond: Callable[[Dict[str, Any]], bool]
    ) -> Callable[[Dict[str, Any]], bool]:
        """Composition: wp(S1; S2, Q) = wp(S1, wp(S2, Q))."""
        curr_wp = postcond
        for var, expr in reversed(stmts):
            curr_wp = self.wp_assign(var, expr, curr_wp)
        return curr_wp

    def wp_if(
        self,
        cond_fn: Callable[[Dict[str, Any]], bool],
        then_wp: Callable[[Dict[str, Any]], bool],
        else_wp: Callable[[Dict[str, Any]], bool]
    ) -> Callable[[Dict[str, Any]], bool]:
        """Conditional: wp(if B then S1 else S2, Q) = (B => wp(S1, Q)) and (~B => wp(S2, Q))."""
        def wp_fn(state: Dict[str, Any]) -> bool:
            if cond_fn(state):
                return then_wp(state)
            else:
                return else_wp(state)
        return wp_fn
