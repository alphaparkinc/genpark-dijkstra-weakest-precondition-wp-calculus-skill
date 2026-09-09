"""
MCP Server for Dijkstra's Weakest Precondition (wp) Calculus Skill
"""

import json
import sys
from client import WeakestPreconditionEngine

def handle_call(name: str, args: dict) -> dict:
    if name == "compute_weakest_precondition":
        engine = WeakestPreconditionEngine()
        x_val = args.get("x", 4)
        thresh = args.get("y_target", 10)
        stmts = [
            ("x", lambda s: s["x"] + 1),
            ("y", lambda s: s["x"] * 2)
        ]
        wp = engine.wp_sequence(stmts, lambda s: s["y"] >= thresh)
        satisfied = wp({"x": x_val, "y": 0})
        return {"x": x_val, "satisfies_wp": satisfied}
    return {"error": f"Unknown tool: {name}"}

def main():
    for line in sys.stdin:
        if not line.strip():
            continue
        req = json.loads(line)
        res = handle_call(req.get("method"), req.get("params", {}))
        sys.stdout.write(json.dumps(res) + "\n")
        sys.stdout.flush()

if __name__ == "__main__":
    main()
