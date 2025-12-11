import ast
import operator as op
import math
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# ---------- Safe evaluation setup ----------

# Allowed binary / unary operators
ALLOWED_OPERATORS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.FloorDiv: op.floordiv,
    ast.Mod: op.mod,
    ast.Pow: op.pow,
    ast.USub: op.neg,  # unary -
}

# Allowed math functions.
# For trig we assume DEGREES input (calculator-style).
def sin_deg(x): return math.sin(math.radians(x))
def cos_deg(x): return math.cos(math.radians(x))
def tan_deg(x): return math.tan(math.radians(x))

ALLOWED_FUNCS = {
    "sin": sin_deg,
    "cos": cos_deg,
    "tan": tan_deg,
    "log": math.log,   # natural log
    "sqrt": math.sqrt,
}

# Allowed constants
ALLOWED_CONSTANTS = {
    "pi": math.pi,
    "e": math.e,
}


def safe_eval(expr: str) -> float:
    """
    Safely evaluate a math expression using Python's AST.

    Supported:
      - Operators: +, -, *, /, //, %, **, parentheses, unary -
      - Functions (degree-based trig): sin(x), cos(x), tan(x)
      - Functions: log(x) [natural log], sqrt(x)
      - Constants: pi, e

    Examples:
      sin(30)       -> 0.5
      sqrt(25)      -> 5
      log(e)        -> 1
      sin(45)*sqrt(2)
    """
    expr = str(expr).strip()
    print(f"Evaluating expression: {expr}")

    def _eval(node):
        # Numbers (Python 3.8+ uses Constant)
        if isinstance(node, ast.Constant):
            if isinstance(node.value, (int, float)):
                return node.value
            raise ValueError("Invalid constant")

        # Named constants like pi, e
        if isinstance(node, ast.Name):
            if node.id in ALLOWED_CONSTANTS:
                return ALLOWED_CONSTANTS[node.id]
            raise ValueError(f"Unknown identifier: {node.id}")

        # Unary operations, e.g. -3
        if isinstance(node, ast.UnaryOp) and type(node.op) in ALLOWED_OPERATORS:
            operand = _eval(node.operand)
            return ALLOWED_OPERATORS[type(node.op)](operand)

        # Binary operations, e.g. 2+3, 4*5
        if isinstance(node, ast.BinOp) and type(node.op) in ALLOWED_OPERATORS:
            left = _eval(node.left)
            right = _eval(node.right)
            return ALLOWED_OPERATORS[type(node.op)](left, right)

        # Function calls: sin(...), log(...), sqrt(...)
        if isinstance(node, ast.Call):
            # Only allow simple names like sin, log, sqrt – not attributes, etc.
            if isinstance(node.func, ast.Name) and node.func.id in ALLOWED_FUNCS:
                func = ALLOWED_FUNCS[node.func.id]
                # For simplicity, only a single positional argument
                if len(node.args) != 1:
                    raise ValueError("Only single-argument functions are supported")
                arg_val = _eval(node.args[0])
                return func(arg_val)
            raise ValueError("Unsupported function or call")

        # Parentheses are reflected indirectly in the AST structure,
        # so nothing specific to do for them.
        raise ValueError("Unsupported or unsafe expression")

    try:
        parsed = ast.parse(expr, mode="eval")  # ast.Expression
        return _eval(parsed.body)
    except ZeroDivisionError:
        raise
    except Exception as e:
        print("safe_eval error:", repr(e))
        raise ValueError("Invalid expression")

# ---------- In-memory history ----------

calculation_history = []  # list of {"expression": str, "result": number}

# ---------- Routes ----------

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/calculate", methods=["POST"])
def calculate():
    data = request.get_json() or {}
    expression = data.get("expression", "")

    print("Expression from client:", repr(expression))

    try:
        result = safe_eval(expression)

        # Store in history
        calculation_history.append({
            "expression": expression,
            "result": result,
        })

        return jsonify({"result": result})
    except ZeroDivisionError:
        return jsonify({"error": "Division by zero"}), 400
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception:
        return jsonify({"error": "Invalid expression"}), 400

@app.route("/api/history", methods=["GET"])
def get_history():
    # Return the last 10 entries
    return jsonify(calculation_history[-10:])

@app.route("/api/history/clear", methods=["POST"])
def clear_history():
    calculation_history.clear()
    return jsonify({"status": "cleared"})

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})

# ---------- Entry point ----------

if __name__ == "__main__":
    app.run(debug=True)
