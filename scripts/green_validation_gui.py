"""4×4 Magic Square GUI — Answer + Verify (scripts demo, not production)."""

from __future__ import annotations

import logging
import sys
from pathlib import Path
from typing import Any

import tkinter as tk
from tkinter import messagebox, scrolledtext, ttk

_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT / "src") not in sys.path:
    sys.path.insert(0, str(_ROOT / "src"))
if str(_ROOT / "scripts") not in sys.path:
    sys.path.insert(0, str(_ROOT / "scripts"))

from demo_solver import (  # noqa: E402
    SolveError,
    VerifyError,
    VerifySuccess,
    find_all_solutions,
    grid_key,
    verify_grid,
)
from magicsquare.boundary.validation import (  # noqa: E402
    ValidationFailure,
    dimension_validation_failure,
)

logger = logging.getLogger(__name__)

GRID_SIZE = 4


class MagicSquareGui(tk.Tk):
    """4×4 grid with Answer (cycle solutions) and Verify."""

    def __init__(self) -> None:
        super().__init__()
        self.title("MagicSquare 4×4 — Answer & Verify")
        self.geometry("520x520")
        self._cells: list[list[tk.StringVar]] = []
        self._answer_solutions: list[Any] = []
        self._answer_index = 0
        self._answer_source_key: tuple[tuple[int, ...], ...] | None = None
        self._verification_state = "idle"
        self._build_widgets()
        self.load_grid([[0] * GRID_SIZE for _ in range(GRID_SIZE)])

    def _build_widgets(self) -> None:
        ttk.Label(
            self,
            text="4×4 Magic Square (M=34) · 0 = blank",
            font=("Segoe UI", 12, "bold"),
        ).pack(pady=(12, 4))

        grid_frame = ttk.Frame(self)
        grid_frame.pack(pady=8)

        for r in range(GRID_SIZE):
            row_vars: list[tk.StringVar] = []
            row_frame = ttk.Frame(grid_frame)
            row_frame.pack()
            for c in range(GRID_SIZE):
                var = tk.StringVar(value="0")
                row_vars.append(var)
                entry = ttk.Entry(
                    row_frame,
                    textvariable=var,
                    width=4,
                    justify="center",
                    font=("Consolas", 14),
                )
                entry.grid(row=r, column=c, padx=3, pady=3)
            self._cells.append(row_vars)

        btn_row = ttk.Frame(self)
        btn_row.pack(pady=8)
        ttk.Button(btn_row, text="Clear", command=self._on_clear).pack(
            side="left", padx=4,
        )
        ttk.Button(btn_row, text="답안", command=self._on_answer).pack(
            side="left", padx=4,
        )
        ttk.Button(btn_row, text="Verify", command=self._on_verify).pack(
            side="left", padx=4,
        )

        self.status_label = ttk.Label(
            self,
            text="격자 입력 → 답안 → Verify",
        )
        self.status_label.pack(pady=(0, 4))

        self.result_box = scrolledtext.ScrolledText(
            self, height=10, font=("Consolas", 10), state="disabled",
        )
        self.result_box.pack(fill="both", expand=True, padx=12, pady=(0, 12))

    def _set_result(self, text: str) -> None:
        self.result_box.configure(state="normal")
        self.result_box.delete("1.0", tk.END)
        self.result_box.insert("1.0", text)
        self.result_box.configure(state="disabled")

    def read_grid(self) -> list[list[int]] | str:
        """Read 4×4 grid from entries; return error message on parse failure."""
        grid: list[list[int]] = []
        for r in range(GRID_SIZE):
            row: list[int] = []
            for c in range(GRID_SIZE):
                raw = self._cells[r][c].get().strip()
                if raw == "":
                    row.append(0)
                    continue
                try:
                    value = int(raw)
                except ValueError:
                    return f"Cell ({r + 1},{c + 1}): integer required."
                row.append(value)
            grid.append(row)
        return grid

    def load_grid(self, grid: list[list[int]], *, reset_answers: bool = True) -> None:
        """Write grid values into the 4×4 entries."""
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                self._cells[r][c].set(str(grid[r][c]))
        if reset_answers:
            self._reset_answers()

    def _reset_answers(self) -> None:
        self._answer_solutions = []
        self._answer_index = 0
        self._answer_source_key = None
        self._verification_state = "idle"

    def _on_clear(self) -> None:
        self.load_grid([[0] * GRID_SIZE for _ in range(GRID_SIZE)])
        self.status_label.configure(text="격자 초기화")
        self._set_result("")

    def _boundary_size_ok(self, grid: list[list[int]]) -> str | None:
        """Demo-only dimension check (does not call full validate / domain resolve)."""
        result = dimension_validation_failure(grid)
        if isinstance(result, ValidationFailure):
            return result.message
        return None

    def _on_answer(self) -> None:
        grid = self.read_grid()
        if isinstance(grid, str):
            messagebox.showerror("Input", grid)
            return

        size_err = self._boundary_size_ok(grid)
        if size_err:
            self._set_result(f"답안: FAILED\n{size_err}")
            return

        key = grid_key(grid)
        if self._answer_source_key != key:
            found = find_all_solutions(grid)
            if isinstance(found, SolveError):
                self._reset_answers()
                self._set_result(f"답안: FAILED\n{found.message}")
                self.status_label.configure(text="답안 실패")
                return
            if not found:
                self._reset_answers()
                self._set_result("답안: FAILED\n해가 없습니다 (unsolvable).")
                self.status_label.configure(text="답안 실패")
                return
            self._answer_solutions = found
            self._answer_index = 0
            self._answer_source_key = key

        total = len(self._answer_solutions)
        pos = self._answer_index % total
        solution = self._answer_solutions[pos]
        self.load_grid(solution.filled_grid, reset_answers=False)
        self._verification_state = "unverified"

        payload = solution.payload
        lines = [
            "답안: APPLIED (미검증)",
            "※ 답안만 채운 상태입니다. FAIL이 아닙니다. Verify로 판정하세요.",
            "",
            f"답안 {pos + 1} / {total}",
            f"payload (int[6]): {payload}",
            f"  blank 1 → row={payload[0]}, col={payload[1]}, value={payload[2]}",
            f"  blank 2 → row={payload[3]}, col={payload[4]}, value={payload[5]}",
            "",
            "Completed 4×4 grid:",
        ]
        for row in solution.filled_grid:
            lines.append("  " + " ".join(f"{v:2d}" for v in row))
        self._set_result("\n".join(lines))
        self.status_label.configure(
            text=f"답안 적용됨 (미검증) — Verify로 확인",
        )
        self._answer_index = (self._answer_index + 1) % total

    def _on_verify(self) -> None:
        grid = self.read_grid()
        if isinstance(grid, str):
            messagebox.showerror("Input", grid)
            return

        size_err = self._boundary_size_ok(grid)
        if size_err:
            self._set_result(f"Verify: FAILED\nBoundary: {size_err}")
            self.status_label.configure(text="Verify 실패 (size)")
            return

        outcome = verify_grid(grid)
        if isinstance(outcome, VerifyError):
            self._verification_state = "failed"
            self._set_result(
                f"Verify: FAILED\n{outcome.message}\n\n"
                "(답안 적용 후 검증 실패 — 격자 또는 답안을 다시 확인하세요.)",
            )
            self.status_label.configure(text="Verify 실패")
            return

        assert isinstance(outcome, VerifySuccess)
        self._verification_state = "verified"
        lines = [outcome.message, "", "Grid:"]
        for row in grid:
            lines.append("  " + " ".join(f"{v:2d}" for v in row))
        self._set_result("\n".join(lines))
        self.status_label.configure(text="Verify 성공")
        messagebox.showinfo("Verify", "SUCCESS — valid magic square!")


def main() -> None:
    """Launch the 4×4 GUI."""
    logging.basicConfig(level=logging.INFO)
    app = MagicSquareGui()
    app.mainloop()


if __name__ == "__main__":
    main()
