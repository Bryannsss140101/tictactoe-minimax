import tkinter as tk
from tkinter import messagebox
import threading
import subprocess

from .ai_engine import IA
from .game_logic import winner, is_draw


class TicTacToeApp:
    def __init__(self, root):
        self.root = root
        self._init_window()
        self._init_state()
        self._init_style()
        self._build_ui()
        self.render()
        self._maybe_ai_starts()

    def _init_window(self):
        self.root.title("TicTacToe")
        self.root.configure(bg="#0b1220")
        self.root.resizable(False, False)

    def _init_state(self):
        self.board = [0] * 9
        self.diff = 0
        self.game_over = False
        self.ai_thinking = False

        self.start_player = 1
        self.turn_player = self.start_player

        self.score_x = 0
        self.score_o = 0
        self.score_d = 0

    def _init_style(self):
        self.c_bg = "#0b1220"
        self.c_card = "#0f1b33"
        self.c_card2 = "#101f3d"
        self.c_text = "#e6edf7"
        self.c_muted = "#9db0d0"
        self.c_x = "#7dd3fc"
        self.c_o = "#fda4af"
        self.c_grid = "#1f335f"
        self.c_btn = "#162b52"
        self.c_btn_hover = "#1b386e"
        self.c_accent = "#a78bfa"
        self.c_danger = "#fb7185"

        self.font_title = ("Segoe UI", 18, "bold")
        self.font_sub = ("Segoe UI", 10)
        self.font_cell = ("Segoe UI", 28, "bold")
        self.font_ui = ("Segoe UI", 10, "bold")

    def _build_ui(self):
        self.container = tk.Frame(self.root, bg=self.c_bg, padx=14, pady=14)
        self.container.pack()

        self._build_header(self.container)
        self._build_body(self.container)

    def _build_header(self, parent):
        header = tk.Frame(parent, bg=self.c_bg)
        header.pack(fill="x")

        tk.Label(
            header,
            text="Tic Tac Toe",
            font=self.font_title,
            fg=self.c_text,
            bg=self.c_bg,
        ).pack(anchor="center")

        self.status = tk.Label(
            header,
            text="Your turn • X",
            font=("Segoe UI", 11, "bold"),
            fg=self.c_muted,
            bg=self.c_bg,
        )
        self.status.pack(anchor="center", pady=(2, 10))

    def _build_body(self, parent):
        body = tk.Frame(parent, bg=self.c_bg)
        body.pack()

        self.left = tk.Frame(body, bg=self.c_card, padx=14, pady=14)
        self.left.grid(row=0, column=0, padx=(0, 12), pady=0)

        self.right = tk.Frame(body, bg=self.c_card, padx=14, pady=14)
        self.right.grid(row=0, column=1, padx=0, pady=0, sticky="n")

        self._build_board(self.left)
        self._build_panel(self.right)

    # -------------------- UI: BOARD --------------------
    def _build_board(self, parent):
        self.buttons = []

        card = tk.Frame(
            parent,
            bg=self.c_card2,
            padx=14,
            pady=14,
            highlightthickness=1,
            highlightbackground=self.c_grid,
        )
        card.pack()

        board_frame = tk.Frame(card, bg=self.c_card2)
        board_frame.pack()

        for i in range(3):
            board_frame.grid_rowconfigure(i, weight=1, uniform="row")
            board_frame.grid_columnconfigure(i, weight=1, uniform="col")

        for r in range(3):
            for c in range(3):
                idx = r * 3 + c
                btn = tk.Button(
                    board_frame,
                    text="",
                    width=3,
                    height=1,
                    font=self.font_cell,
                    fg=self.c_text,
                    bg=self.c_btn,
                    activebackground=self.c_btn_hover,
                    activeforeground=self.c_text,
                    relief="flat",
                    bd=0,
                    highlightthickness=1,
                    highlightbackground=self.c_grid,
                    highlightcolor=self.c_grid,
                    cursor="hand2",
                    command=lambda i=idx: self.on_human_move(i),
                )
                btn.grid(row=r, column=c, padx=8, pady=8, ipadx=16, ipady=16)

                btn.bind("<Enter>", lambda e, b=btn: self._hover(b, True))
                btn.bind("<Leave>", lambda e, b=btn: self._hover(b, False))

                self.buttons.append(btn)

    # -------------------- UI: PANEL --------------------
    def _build_panel(self, parent):
        panel = tk.Frame(parent, bg=self.c_card)
        panel.pack(fill="x")

        self._build_score(panel)

        tk.Frame(panel, bg=self.c_grid, height=1).pack(fill="x", pady=(10, 12))

        self._build_difficulty(panel)

        self._build_start_player(panel)

        tk.Frame(panel, bg=self.c_grid, height=1).pack(fill="x", pady=(10, 12))

        self._build_actions(panel)

    def _build_score(self, parent):
        tk.Label(
            parent, text="Scoreboard", font=self.font_ui, fg=self.c_text, bg=self.c_card
        ).pack(anchor="w")

        score_card = tk.Frame(parent, bg=self.c_card2, padx=12, pady=10)
        score_card.pack(fill="x", pady=(8, 14))

        score_card.grid_columnconfigure(0, weight=1)
        score_card.grid_columnconfigure(1, weight=0)

        self.lbl_x_name = tk.Label(
            score_card,
            text="X (You)",
            font=("Segoe UI", 10, "bold"),
            fg=self.c_x,
            bg=self.c_card2,
        )
        self.lbl_x_val = tk.Label(
            score_card,
            text=str(self.score_x),
            font=("Segoe UI", 12, "bold"),
            fg=self.c_text,
            bg=self.c_card2,
        )

        self.lbl_o_name = tk.Label(
            score_card,
            text="O (PC)",
            font=("Segoe UI", 10, "bold"),
            fg=self.c_o,
            bg=self.c_card2,
        )
        self.lbl_o_val = tk.Label(
            score_card,
            text=str(self.score_o),
            font=("Segoe UI", 12, "bold"),
            fg=self.c_text,
            bg=self.c_card2,
        )

        self.lbl_d_name = tk.Label(
            score_card,
            text="Draw",
            font=("Segoe UI", 10, "bold"),
            fg=self.c_muted,
            bg=self.c_card2,
        )
        self.lbl_d_val = tk.Label(
            score_card,
            text=str(self.score_d),
            font=("Segoe UI", 12, "bold"),
            fg=self.c_text,
            bg=self.c_card2,
        )

        self.lbl_x_name.grid(row=0, column=0, sticky="w")
        self.lbl_x_val.grid(row=0, column=1, sticky="e")

        self.lbl_o_name.grid(row=1, column=0, sticky="w", pady=(6, 0))
        self.lbl_o_val.grid(row=1, column=1, sticky="e", pady=(6, 0))

        self.lbl_d_name.grid(row=2, column=0, sticky="w", pady=(6, 0))
        self.lbl_d_val.grid(row=2, column=1, sticky="e", pady=(6, 0))

    def _build_difficulty(self, parent):
        card = tk.Frame(parent, bg=self.c_card2, padx=12, pady=10)
        card.pack(fill="x", pady=(8, 0))

        diff_row = tk.Frame(card, bg=self.c_card2)
        diff_row.pack(fill="x")

        self.btn_medium = self._pill(diff_row, "Medium", 0)
        self.btn_hard = self._pill(diff_row, "Hard", 1)
        self.btn_medium.pack(side="left", padx=(0, 8))
        self.btn_hard.pack(side="left")
        self._refresh_diff_buttons()

    def _build_start_player(self, parent):
        card = tk.Frame(parent, bg=self.c_card2, padx=12, pady=10)
        card.pack(fill="x", pady=(8, 0))

        start_row = tk.Frame(card, bg=self.c_card2)
        start_row.pack(fill="x")

        self.btn_start_x = self._pill_start(start_row, "Player X", 1)
        self.btn_start_o = self._pill_start(start_row, "Player O", -1)
        self.btn_start_x.pack(side="left", padx=(0, 8))
        self.btn_start_o.pack(side="left")
        self._refresh_start_buttons()

    def _build_actions(self, parent):
        actions = tk.Frame(parent, bg=self.c_card2, padx=12, pady=10)
        actions.pack(fill="x", pady=(8, 0))

        btn_new_game = tk.Button(
            actions,
            text="New Game",
            font=self.font_ui,
            fg=self.c_text,
            bg=self.c_accent,
            activebackground=self.c_accent,
            activeforeground=self.c_text,
            relief="flat",
            bd=0,
            command=self.new_game,
        )
        btn_new_game.pack(fill="x", pady=(0, 8), ipady=10)

        btn_reset_score = tk.Button(
            actions,
            text="Reset Scoreboard",
            font=self.font_ui,
            fg=self.c_text,
            bg=self.c_btn,
            activebackground=self.c_btn_hover,
            activeforeground=self.c_text,
            relief="flat",
            bd=0,
            command=self.reset_all,
        )
        btn_reset_score.pack(fill="x", pady=(0, 8), ipady=10)

        btn_quit = tk.Button(
            actions,
            text="Quit Game",
            font=self.font_ui,
            fg=self.c_text,
            bg=self.c_danger,
            activebackground=self.c_danger,
            activeforeground=self.c_text,
            relief="flat",
            bd=0,
            command=self.root.destroy,
        )
        btn_quit.pack(fill="x", ipady=10)

    # -------------------- UI helpers --------------------
    def _hover(self, btn, on):
        if btn["state"] == "disabled":
            return
        btn.configure(bg=self.c_btn_hover if on else self.c_btn)

    def _pill(self, parent, text, value):
        return tk.Button(
            parent,
            text=text,
            font=self.font_ui,
            fg=self.c_text,
            bg=self.c_btn,
            activebackground=self.c_btn_hover,
            activeforeground=self.c_text,
            relief="flat",
            bd=0,
            padx=14,
            pady=8,
            command=lambda v=value: self.set_diff(v),
        )

    def _pill_start(self, parent, text, value):
        return tk.Button(
            parent,
            text=text,
            font=self.font_ui,
            fg=self.c_text,
            bg=self.c_btn,
            activebackground=self.c_btn_hover,
            activeforeground=self.c_text,
            relief="flat",
            bd=0,
            padx=14,
            pady=8,
            command=lambda v=value: self.set_start_player(v),
        )

    def _refresh_score(self):
        if not hasattr(self, "lbl_x_val"):
            return
        self.lbl_x_val.configure(text=str(self.score_x))
        self.lbl_o_val.configure(text=str(self.score_o))
        self.lbl_d_val.configure(text=str(self.score_d))

    def _refresh_diff_buttons(self):
        if self.diff == 0:
            self.btn_medium.configure(bg=self.c_accent)
            self.btn_hard.configure(bg=self.c_btn)
        else:
            self.btn_hard.configure(bg=self.c_accent)
            self.btn_medium.configure(bg=self.c_btn)

    def _refresh_start_buttons(self):
        if self.start_player == 1:
            self.btn_start_x.configure(bg=self.c_accent)
            self.btn_start_o.configure(bg=self.c_btn)
        else:
            self.btn_start_o.configure(bg=self.c_accent)
            self.btn_start_x.configure(bg=self.c_btn)

    def _score_text(self):
        return f"X (You): {self.score_x}\nO (PC): {self.score_o}\nDraw: {self.score_d}"

    # -------------------- Game controls --------------------
    def set_diff(self, v):
        self.diff = int(v)
        self._refresh_diff_buttons()

    def set_start_player(self, v):
        self.start_player = int(v)
        self._refresh_start_buttons()

    def new_game(self):
        self.board = [0] * 9
        self.game_over = False
        self.ai_thinking = False
        self.turn_player = self.start_player

        for b in self.buttons:
            b.configure(
                text="", state="normal", bg=self.c_btn, highlightbackground=self.c_grid
            )

        self.render()
        self._update_status()
        self._maybe_ai_starts()

    def reset_all(self):
        self.score_x = self.score_o = self.score_d = 0
        self._refresh_score()
        self.new_game()

    def render(self):
        for i, v in enumerate(self.board):
            if v == 1:
                self.buttons[i].configure(text="X", fg=self.c_x)
            elif v == -1:
                self.buttons[i].configure(text="O", fg=self.c_o)
            else:
                self.buttons[i].configure(text="", fg=self.c_text)

    def _highlight_line(self, line):
        for i in line:
            self.buttons[i].configure(bg=self.c_grid, highlightbackground=self.c_grid)

    def _end(self, msg, winner_code=0, line=None):
        self.game_over = True
        self.ai_thinking = False

        for b in self.buttons:
            b.configure(state="disabled")

        if line:
            self._highlight_line(line)

        if winner_code == 1:
            self.score_x += 1
        elif winner_code == -1:
            self.score_o += 1
        else:
            self.score_d += 1

        self._refresh_score()
        self.status.configure(text=msg, fg=self.c_text)
        messagebox.showinfo("Game Over", msg)

    def check_end(self):
        w, line = winner(self.board)
        if w == 1:
            self._end("Winner • X", winner_code=1, line=line)
            return True
        if w == -1:
            self._end("Winner • O", winner_code=-1, line=line)
            return True
        if is_draw(self.board):
            self._end("Draw", winner_code=0, line=None)
            return True
        return False

    def _update_status(self):
        if self.game_over:
            return
        if self.turn_player == 1:
            self.status.configure(text="Your turn • X", fg=self.c_muted)
        else:
            self.status.configure(text="Thinking • O", fg=self.c_muted)

    def _set_buttons_enabled_for_turn(self):
        if self.game_over or self.ai_thinking:
            for b in self.buttons:
                b.configure(state="disabled")
            return

        if self.turn_player == 1:
            for i, b in enumerate(self.buttons):
                b.configure(state=("normal" if self.board[i] == 0 else "disabled"))
        else:
            for b in self.buttons:
                b.configure(state="disabled")

    def on_human_move(self, idx):
        if self.game_over or self.ai_thinking or self.turn_player != 1:
            return
        if self.board[idx] != 0:
            return

        self.board[idx] = 1
        self.render()

        if self.check_end():
            return

        self.turn_player = -1
        self._update_status()
        self._set_buttons_enabled_for_turn()
        self._start_ai_thread()

    def _maybe_ai_starts(self):
        if not self.game_over and self.turn_player == -1:
            self._update_status()
            self._set_buttons_enabled_for_turn()
            self._start_ai_thread()

    def _start_ai_thread(self):
        if self.ai_thinking or self.game_over:
            return
        self.ai_thinking = True
        self._set_buttons_enabled_for_turn()

        board_snapshot = self.board[:]
        diff_snapshot = self.diff

        def worker():
            try:
                r, c = IA(board_snapshot, turn=0, diff=diff_snapshot, timeout=5.0)
                self.root.after(500, lambda: self._apply_ai_move(r, c))
            except FileNotFoundError:
                self.root.after(
                    0,
                    lambda: self._end("ai.exe (same folder) not found.", winner_code=0),
                )
            except subprocess.TimeoutExpired:
                self.root.after(
                    0,
                    lambda: self._end("The AI ​​took too long (timeout).", winner_code=0),
                )
            except subprocess.CalledProcessError as e:
                err = (e.stderr or b"").decode("utf-8", errors="ignore").strip()
                msg = "Error running ai.exe.."
                if err:
                    msg += f"\n\n{err[:300]}"
                self.root.after(0, lambda: self._end(msg, winner_code=0))
            except Exception as e:
                self.root.after(
                    0, lambda: self._end(f"Unexpected error:\n{e}", winner_code=0)
                )

        threading.Thread(target=worker, daemon=True).start()

    def _apply_ai_move(self, r, c):
        if self.game_over:
            return

        self.ai_thinking = False

        if r not in (0, 1, 2) or c not in (0, 1, 2):
            self._end("The AI ​​returned an invalid move (out of range).", winner_code=0)
            return

        idx = r * 3 + c
        if idx < 0 or idx >= 9 or self.board[idx] != 0:
            self._end(
                "The AI ​​returned an invalid move (occupied cell)",
                winner_code=0,
            )
            return

        self.board[idx] = -1
        self.render()

        if self.check_end():
            return

        self.turn_player = 1
        self._update_status()
        self._set_buttons_enabled_for_turn()
