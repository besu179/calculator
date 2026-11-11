"""Calculation logic for the calculator."""

import math


class CalculatorLogic:
    """Handles expression evaluation and number formatting."""

    @staticmethod
    def evaluate(expression: str):
        """Evaluate a math expression safely. Returns a number or raises."""
        allowed = set("0123456789+-*/. ()")
        if not expression or not set(expression).issubset(allowed):
            raise ValueError("Invalid expression")
        # Prevent empty operands like "1+" or trailing operators
        if expression[-1] in "+-*/.":
            raise ValueError("Incomplete expression")
        result = eval(expression, {"__builtins__": None}, {"math": math})
        return result

    @staticmethod
    def format_number(value) -> str:
        """Format a number for display."""
        if isinstance(value, float) and value.is_integer():
            return str(int(value))
        return f"{value:.8g}"

    @staticmethod
    def apply_unary(value: float, op: str) -> float:
        """Apply a unary operation to a value."""
        if op == "sqrt":
            if value < 0:
                raise ValueError("Negative square root")
            return math.sqrt(value)
        if op == "sqr":
            return value ** 2
        if op == "recip":
            if value == 0:
                raise ZeroDivisionError()
            return 1 / value
        if op == "pct":
            return value / 100
        if op == "neg":
            return -value
        raise ValueError("Unknown operation")
