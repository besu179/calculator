"""Tkinter user interface for the calculator."""

import tkinter as tk

from config import COLORS, APP_TITLE, APP_SIZE, FONT_DISPLAY, FONT_SUB, FONT_BUTTON
from logic import CalculatorLogic


class CalculatorUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(APP_TITLE)
        self.geometry(APP_SIZE)
        self.resizable(False, False)
        self.configure(bg=COLORS["bg"])

        self.expression = ""
        self._build_display()
        self._build_buttons()
        self._bind_keys()

    # --- Display ---

    def _build_display(self):
        frame = tk.Frame(self, bg=COLORS["bg"], padx=10, pady=10)
        frame.pack(fill="x")

        self.sub_var = tk.StringVar(value="")
        self.sub_display = tk.Label(
            frame,
            textvariable=self.sub_var,
            font=FONT_SUB,
            fg=COLORS["muted"],
            bg=COLORS["display_bg"],
            anchor="e",
            padx=12,
        )
        self.sub_display.pack(fill="x")

        self.display_var = tk.StringVar(value="0")
        self.display = tk.Label(
            frame,
            textvariable=self.display_var,
            font=FONT_DISPLAY,
            fg=COLORS["text"],
            bg=COLORS["display_bg"],
            anchor="e",
            padx=12,
            pady=8,
        )
        self.display.pack(fill="x")

    # --- Buttons ---

    def _build_buttons(self):
        frame = tk.Frame(self, bg=COLORS["bg"], padx=10, pady=5)
        frame.pack(fill="both", expand=True)

        for col in range(4):
            frame.columnconfigure(col, weight=1, uniform="equal")
        for row in range(5):
            frame.rowconfigure(row, weight=1, uniform="equal")

        buttons = [
            ("C", 0, 0, self._clear, COLORS["clear_bg"], COLORS["clear_fg"]),
            ("⌫", 0, 1, self._backspace, COLORS["clear_bg"], COLORS["text"]),
            ("%", 0, 2, lambda: self._unary("pct"), COLORS["clear_bg"], COLORS["text"]),
            ("÷", 0, 3, lambda: self._append_op("/"), COLORS["op_bg"], COLORS["op_fg"]),
            ("7", 1, 0, lambda: self._append_digit("7"), COLORS["digit_bg"], COLORS["text"]),
            ("8", 1, 1, lambda: self._append_digit("8"), COLORS["digit_bg"], COLORS["text"]),
            ("9", 1, 2, lambda: self._append_digit("9"), COLORS["digit_bg"], COLORS["text"]),
            ("×", 1, 3, lambda: self._append_op("*"), COLORS["op_bg"], COLORS["op_fg"]),
            ("4", 2, 0, lambda: self._append_digit("4"), COLORS["digit_bg"], COLORS["text"]),
            ("5", 2, 1, lambda: self._append_digit("5"), COLORS["digit_bg"], COLORS["text"]),
            ("6", 2, 2, lambda: self._append_digit("6"), COLORS["digit_bg"], COLORS["text"]),
            ("-", 2, 3, lambda: self._append_op("-"), COLORS["op_bg"], COLORS["op_fg"]),
            ("1", 3, 0, lambda: self._append_digit("1"), COLORS["digit_bg"], COLORS["text"]),
            ("2", 3, 1, lambda: self._append_digit("2"), COLORS["digit_bg"], COLORS["text"]),
            ("3", 3, 2, lambda: self._append_digit("3"), COLORS["digit_bg"], COLORS["text"]),
            ("+", 3, 3, lambda: self._append_op("+"), COLORS["op_bg"], COLORS["op_fg"]),
            ("±", 4, 0, self._negate, COLORS["digit_bg"], COLORS["text"]),
            ("0", 4, 1, lambda: self._append_digit("0"), COLORS["digit_bg"], COLORS["text"]),
            (".", 4, 2, self._append_dot, COLORS["digit_bg"], COLORS["text"]),
            ("=", 4, 3, self._calculate, COLORS["equals_bg"], COLORS["equals_fg"]),
        ]

        for text, r, c, cmd, bg, fg in buttons:
            btn = tk.Button(
                frame,
                text=text,
                command=cmd,
                bg=bg,
                fg=fg,
                activebackground="#585b70",
                activeforeground="#ffffff",
                font=FONT_BUTTON,
                relief="flat",
                bd=0,
                cursor="hand2",
            )
            btn.grid(row=r, column=c, padx=3, pady=3, sticky="nsew")

    # --- Key bindings ---

    def _bind_keys(self):
        self.bind("<Return>", lambda e: self._calculate())
        self.bind("<KP_Enter>", lambda e: self._calculate())
        self.bind("<BackSpace>", lambda e: self._backspace())
        self.bind("<Escape>", lambda e: self._clear())
        for d in "0123456789":
            self.bind(d, lambda e, digit=d: self._append_digit(digit))
            self.bind(f"<KP_{d}>", lambda e, digit=d: self._append_digit(digit))
        for op in "+-*/":
            self.bind(op, lambda e, operator=op: self._append_op(operator))
        self.bind(".", lambda e: self._append_dot())

    # --- Logic helpers ---

    def _current(self) -> str:
        return self.display_var.get()

    def _append_digit(self, char: str):
        if self._current() in ("0", "Error"):
            self.display_var.set(char)
        else:
            self.display_var.set(self._current() + char)

    def _append_dot(self):
        curr = self._current()
        tokens = curr.replace("+", " ").replace("-", " ").replace("*", " ").replace("/", " ").split()
        if tokens and "." not in tokens[-1]:
            self.display_var.set(curr + ".")
        elif not tokens:
            self.display_var.set("0.")

    def _append_op(self, op: str):
        curr = self._current()
        if curr == "Error":
            return
        if curr and curr[-1] in "+-*/":
            self.display_var.set(curr[:-1] + op)
        else:
            self.display_var.set(curr + op)

    def _clear(self):
        self.display_var.set("0")
        self.sub_var.set("")

    def _backspace(self):
        curr = self._current()
        if curr in ("Error", "0") or len(curr) == 1:
            self.display_var.set("0")
        else:
            self.display_var.set(curr[:-1])

    def _negate(self):
        curr = self._current()
        try:
            val = float(curr)
            self.display_var.set(CalculatorLogic.format_number(-val))
        except ValueError:
            pass

    def _unary(self, op: str):
        try:
            val = float(self._current())
            res = CalculatorLogic.apply_unary(val, op)
            formatted = CalculatorLogic.format_number(res)
            self.sub_var.set(f"{op}({val})")
            self.display_var.set(formatted)
        except ZeroDivisionError:
            self.display_var.set("Error: Div by 0")
        except Exception:
            self.display_var.set("Error")

    def _calculate(self):
        expr = self._current()
        try:
            result = CalculatorLogic.evaluate(expr)
            formatted = CalculatorLogic.format_number(result)
            self.sub_var.set(expr + " =")
            self.display_var.set(formatted)
        except ZeroDivisionError:
            self.display_var.set("Error: Div by 0")
        except Exception:
            self.display_var.set("Error")
