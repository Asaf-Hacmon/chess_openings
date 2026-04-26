"""
Chess Openings Trainer
Teaches the 3 most popular chess openings with a full GUI.
"""

import tkinter as tk
from tkinter import ttk, messagebox, font as tkfont
import chess
import chess.pgn
import copy
from openings_db import OPENINGS

# ── Constants ────────────────────────────────────────────────────────────────
SQUARE_SIZE = 72
BOARD_SIZE = SQUARE_SIZE * 8
LIGHT_SQ = "#F0D9B5"
DARK_SQ  = "#B58863"
HIGHLIGHT_FROM  = "#F6F669"
HIGHLIGHT_TO    = "#CDD16E"
HIGHLIGHT_LEGAL = "#7FC97F"
HIGHLIGHT_HINT  = "#FF6B6B"
LAST_MOVE_ALPHA = "#AAD966"

PIECE_UNICODE = {
    "P": "♙", "N": "♘", "B": "♗", "R": "♖", "Q": "♕", "K": "♔",
    "p": "♟", "n": "♞", "b": "♝", "r": "♜", "q": "♛", "k": "♚",
}

BG_MAIN   = "#1A1A2E"
BG_PANEL  = "#16213E"
BG_CARD   = "#0F3460"
ACCENT    = "#E94560"
TEXT_MAIN = "#EAEAEA"
TEXT_DIM  = "#8899AA"


# ── Opening Tree Helpers ─────────────────────────────────────────────────────

def get_node_for_board(tree, board):
    """Walk the tree following the board's move history, return current node."""
    move_stack = list(board.move_stack)
    node = tree
    for move in move_stack:
        found = False
        for child in node.get("children", []):
            if child["move"] == move.uci():
                node = child
                found = True
                break
        if not found:
            return None
    return node


def collect_all_moves(tree):
    """Collect all UCI moves in the tree (for variation tracking)."""
    moves = set()
    def walk(node):
        if node.get("move"):
            moves.add(node["move"])
        for child in node.get("children", []):
            walk(child)
    walk(tree)
    return moves


def get_variation_path(tree, board):
    """Return the list of named nodes from root to current position."""
    move_stack = list(board.move_stack)
    node = tree
    path = []
    for move in move_stack:
        for child in node.get("children", []):
            if child["move"] == move.uci():
                node = child
                path.append(node["name"])
                break
    return path


# ── Main Application ──────────────────────────────────────────────────────────

class ChessOpeningsApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Chess Openings Trainer")
        self.configure(bg=BG_MAIN)
        self.resizable(False, False)
        self._show_menu()

    def _clear(self):
        for w in self.winfo_children():
            w.destroy()

    def _show_menu(self):
        self._clear()
        self.title("Chess Openings Trainer — Menu")
        MenuScreen(self)

    def show_game(self, opening_name, mode):
        self._clear()
        self.title(f"Chess Openings Trainer — {opening_name} ({mode})")
        GameScreen(self, opening_name, mode)


# ── Menu Screen ───────────────────────────────────────────────────────────────

class MenuScreen(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg=BG_MAIN)
        self.pack(fill="both", expand=True, padx=40, pady=40)
        self.master = master
        self._build()

    def _build(self):
        title_font = tkfont.Font(family="Georgia", size=28, weight="bold")
        sub_font   = tkfont.Font(family="Georgia", size=13)
        card_font  = tkfont.Font(family="Segoe UI", size=11)
        btn_font   = tkfont.Font(family="Segoe UI", size=11, weight="bold")

        tk.Label(self, text="♟  Chess Openings Trainer", font=title_font,
                 bg=BG_MAIN, fg=TEXT_MAIN).pack(pady=(0, 4))
        tk.Label(self, text="Master the most important chess openings",
                 font=sub_font, bg=BG_MAIN, fg=TEXT_DIM).pack(pady=(0, 30))

        # Opening cards
        cards_frame = tk.Frame(self, bg=BG_MAIN)
        cards_frame.pack(fill="x")

        self.selected_opening = tk.StringVar(value=list(OPENINGS.keys())[0])

        for name, data in OPENINGS.items():
            card = tk.Frame(cards_frame, bg=BG_CARD, relief="flat", bd=0)
            card.pack(fill="x", pady=6, padx=4)

            rb = tk.Radiobutton(card, variable=self.selected_opening, value=name,
                                bg=BG_CARD, activebackground=BG_CARD,
                                selectcolor=BG_CARD, fg=ACCENT, cursor="hand2")
            rb.pack(side="left", padx=10, pady=10)

            info = tk.Frame(card, bg=BG_CARD)
            info.pack(side="left", fill="x", expand=True, padx=4, pady=8)

            color_tag = "▶ White" if data["color"] == "white" else "▶ Black"
            tk.Label(info, text=f"{name}  —  {color_tag}",
                     font=card_font, bg=BG_CARD, fg=TEXT_MAIN,
                     anchor="w").pack(anchor="w")
            tk.Label(info, text=data["description"],
                     font=tkfont.Font(family="Segoe UI", size=9),
                     bg=BG_CARD, fg=TEXT_DIM, wraplength=480,
                     justify="left", anchor="w").pack(anchor="w")

        # Mode buttons
        btn_frame = tk.Frame(self, bg=BG_MAIN)
        btn_frame.pack(pady=28)

        tk.Button(btn_frame, text="📖  Learning Mode",
                  font=btn_font, bg=ACCENT, fg="white",
                  activebackground="#c73652", activeforeground="white",
                  relief="flat", padx=24, pady=10, cursor="hand2",
                  command=lambda: self._launch("Learning")).pack(side="left", padx=10)

        tk.Button(btn_frame, text="🎯  Practice Mode",
                  font=btn_font, bg=BG_CARD, fg=TEXT_MAIN,
                  activebackground="#1a4a80", activeforeground="white",
                  relief="flat", padx=24, pady=10, cursor="hand2",
                  command=lambda: self._launch("Practice")).pack(side="left", padx=10)

        # Legend
        legend = (
            "Learning Mode: the computer plays the opening moves and explains each one.\n"
            "Practice Mode: play on your own — the app tracks which variation you're in."
        )
        tk.Label(self, text=legend,
                 font=tkfont.Font(family="Segoe UI", size=9),
                 bg=BG_MAIN, fg=TEXT_DIM, justify="center").pack(pady=(0, 4))

    def _launch(self, mode):
        name = self.selected_opening.get()
        self.master.show_game(name, mode)


# ── Game Screen ───────────────────────────────────────────────────────────────

class GameScreen(tk.Frame):
    def __init__(self, master, opening_name, mode):
        super().__init__(master, bg=BG_MAIN)
        self.pack(fill="both", expand=True)
        self.master = master

        self.opening_name = opening_name
        self.opening_data  = OPENINGS[opening_name]
        self.mode = mode  # "Learning" or "Practice"

        self.board = chess.Board()
        self.selected_square = None
        self.legal_move_squares = []
        self.last_move = None
        self.hint_square = None
        self.player_color = chess.WHITE if self.opening_data["color"] == "white" else chess.BLACK
        self.awaiting_computer = False

        self._build_layout()
        self._draw_board()
        self._update_info()

        # Both modes: computer plays the opponent's side
        self._schedule_computer_move()

    # ── Layout ──────────────────────────────────────────────────────────────

    def _build_layout(self):
        left = tk.Frame(self, bg=BG_MAIN)
        left.pack(side="left", padx=(20, 10), pady=20)

        # Top bar above board
        top_bar = tk.Frame(left, bg=BG_MAIN)
        top_bar.pack(fill="x", pady=(0, 6))

        tk.Button(top_bar, text="← Menu",
                  font=tkfont.Font(family="Segoe UI", size=9),
                  bg=BG_CARD, fg=TEXT_MAIN, relief="flat",
                  padx=8, pady=4, cursor="hand2",
                  command=self.master._show_menu).pack(side="left")

        mode_color = ACCENT if self.mode == "Learning" else "#4A90D9"
        tk.Label(top_bar, text=f"{self.mode} Mode",
                 font=tkfont.Font(family="Segoe UI", size=9, weight="bold"),
                 bg=BG_MAIN, fg=mode_color).pack(side="right")

        # Canvas
        self.canvas = tk.Canvas(left, width=BOARD_SIZE, height=BOARD_SIZE,
                                highlightthickness=0, bg=BG_MAIN)
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self._on_click)

        # Coordinates label
        self.coord_var = tk.StringVar(value="")
        tk.Label(left, textvariable=self.coord_var,
                 font=tkfont.Font(family="Consolas", size=9),
                 bg=BG_MAIN, fg=TEXT_DIM).pack(pady=(4, 0))

        # Right panel
        right = tk.Frame(self, bg=BG_PANEL, width=300)
        right.pack(side="left", fill="both", expand=True, padx=(0, 20), pady=20)
        right.pack_propagate(False)
        self._build_panel(right)

    def _build_panel(self, parent):
        pad = {"padx": 14, "pady": 6}

        # Opening name
        tk.Label(parent, text=self.opening_name,
                 font=tkfont.Font(family="Georgia", size=15, weight="bold"),
                 bg=BG_PANEL, fg=TEXT_MAIN, wraplength=270,
                 justify="left").pack(anchor="w", **pad)

        # Variation indicator
        tk.Label(parent, text="Current Variation",
                 font=tkfont.Font(family="Segoe UI", size=8),
                 bg=BG_PANEL, fg=TEXT_DIM).pack(anchor="w", padx=14, pady=(8, 0))

        self.variation_var = tk.StringVar(value="—")
        tk.Label(parent, textvariable=self.variation_var,
                 font=tkfont.Font(family="Segoe UI", size=10, weight="bold"),
                 bg=BG_PANEL, fg=ACCENT, wraplength=270,
                 justify="left").pack(anchor="w", padx=14, pady=(0, 4))

        ttk.Separator(parent, orient="horizontal").pack(fill="x", padx=14, pady=6)

        # Next moves (Learning mode)
        if self.mode == "Learning":
            tk.Label(parent, text="Next Move(s)",
                     font=tkfont.Font(family="Segoe UI", size=8),
                     bg=BG_PANEL, fg=TEXT_DIM).pack(anchor="w", padx=14)
            self.next_moves_frame = tk.Frame(parent, bg=BG_CARD)
            self.next_moves_frame.pack(fill="x", padx=14, pady=(2, 6))
            ttk.Separator(parent, orient="horizontal").pack(fill="x", padx=14, pady=6)

        # Comment box
        tk.Label(parent, text="Move Commentary",
                 font=tkfont.Font(family="Segoe UI", size=8),
                 bg=BG_PANEL, fg=TEXT_DIM).pack(anchor="w", padx=14)

        self.comment_text = tk.Text(parent, height=6, width=30,
                                    font=tkfont.Font(family="Segoe UI", size=10),
                                    bg=BG_CARD, fg=TEXT_MAIN,
                                    relief="flat", wrap="word",
                                    padx=8, pady=6, state="disabled",
                                    cursor="arrow")
        self.comment_text.pack(fill="x", padx=14, pady=(2, 8))

        ttk.Separator(parent, orient="horizontal").pack(fill="x", padx=14, pady=6)

        # Move history
        tk.Label(parent, text="Move History",
                 font=tkfont.Font(family="Segoe UI", size=8),
                 bg=BG_PANEL, fg=TEXT_DIM).pack(anchor="w", padx=14)

        self.history_text = tk.Text(parent, height=5, width=30,
                                    font=tkfont.Font(family="Consolas", size=9),
                                    bg=BG_CARD, fg=TEXT_MAIN,
                                    relief="flat", wrap="word",
                                    padx=8, pady=6, state="disabled",
                                    cursor="arrow")
        self.history_text.tag_config("num",    foreground=TEXT_DIM)
        self.history_text.tag_config("white",  foreground="#FFFFFF")
        self.history_text.tag_config("black",  foreground="#AADDFF")
        self.history_text.tag_config("you",    foreground=ACCENT)
        self.history_text.pack(fill="x", padx=14, pady=(2, 8))

        ttk.Separator(parent, orient="horizontal").pack(fill="x", padx=14, pady=6)

        # Buttons
        btn_frame = tk.Frame(parent, bg=BG_PANEL)
        btn_frame.pack(fill="x", padx=14, pady=4)

        bf = tkfont.Font(family="Segoe UI", size=9, weight="bold")

        tk.Button(btn_frame, text="↩ Undo", font=bf,
                  bg=BG_CARD, fg=TEXT_MAIN, relief="flat",
                  padx=10, pady=5, cursor="hand2",
                  command=self._undo_move).pack(side="left", padx=(0, 6))

        tk.Button(btn_frame, text="↺ Restart", font=bf,
                  bg=BG_CARD, fg=TEXT_MAIN, relief="flat",
                  padx=10, pady=5, cursor="hand2",
                  command=self._restart).pack(side="left", padx=(0, 6))

        if self.mode == "Practice":
            tk.Button(btn_frame, text="💡 Hint", font=bf,
                      bg=ACCENT, fg="white", relief="flat",
                      padx=10, pady=5, cursor="hand2",
                      command=self._show_hint).pack(side="left")

        # Status label
        self.status_var = tk.StringVar(value="")
        tk.Label(parent, textvariable=self.status_var,
                 font=tkfont.Font(family="Segoe UI", size=9),
                 bg=BG_PANEL, fg=ACCENT, wraplength=270,
                 justify="center").pack(pady=(6, 0), padx=14)

    # ── Board Drawing ────────────────────────────────────────────────────────

    def _sq_to_xy(self, sq):
        """Square index → canvas (x, y) top-left corner."""
        file = chess.square_file(sq)
        rank = chess.square_rank(sq)
        if self.player_color == chess.WHITE:
            x = file * SQUARE_SIZE
            y = (7 - rank) * SQUARE_SIZE
        else:
            x = (7 - file) * SQUARE_SIZE
            y = rank * SQUARE_SIZE
        return x, y

    def _xy_to_sq(self, x, y):
        """Canvas click → square index."""
        file = x // SQUARE_SIZE
        rank = y // SQUARE_SIZE
        if self.player_color == chess.WHITE:
            return chess.square(file, 7 - rank)
        else:
            return chess.square(7 - file, rank)

    def _draw_board(self):
        self.canvas.delete("all")
        pf = tkfont.Font(family="Segoe UI", size=int(SQUARE_SIZE * 0.52))
        coord_f = tkfont.Font(family="Segoe UI", size=8)

        lm_from = self.last_move.from_square if self.last_move else None
        lm_to   = self.last_move.to_square   if self.last_move else None

        for sq in chess.SQUARES:
            x, y = self._sq_to_xy(sq)
            file = chess.square_file(sq)
            rank = chess.square_rank(sq)
            is_light = (file + rank) % 2 == 1

            # Base color
            color = LIGHT_SQ if is_light else DARK_SQ

            # Last move highlight
            if sq in (lm_from, lm_to):
                color = HIGHLIGHT_FROM if sq == lm_from else HIGHLIGHT_TO

            # Selected square
            if sq == self.selected_square:
                color = HIGHLIGHT_FROM

            # Hint
            if sq == self.hint_square:
                color = HIGHLIGHT_HINT

            self.canvas.create_rectangle(x, y, x + SQUARE_SIZE, y + SQUARE_SIZE,
                                         fill=color, outline="")

            # Legal move dots
            if sq in self.legal_move_squares:
                piece_on = self.board.piece_at(sq)
                cx, cy = x + SQUARE_SIZE // 2, y + SQUARE_SIZE // 2
                if piece_on:
                    # Ring around occupied square
                    r = SQUARE_SIZE // 2 - 3
                    self.canvas.create_oval(cx - r, cy - r, cx + r, cy + r,
                                            outline=HIGHLIGHT_LEGAL, width=3)
                else:
                    r = SQUARE_SIZE // 6
                    self.canvas.create_oval(cx - r, cy - r, cx + r, cy + r,
                                            fill=HIGHLIGHT_LEGAL, outline="")

            # Piece
            piece = self.board.piece_at(sq)
            if piece:
                symbol = PIECE_UNICODE[piece.symbol()]
                fg = "#FFFFFF" if piece.color == chess.WHITE else "#1A1A1A"
                shadow = "#555555"
                self.canvas.create_text(x + SQUARE_SIZE // 2 + 1,
                                        y + SQUARE_SIZE // 2 + 1,
                                        text=symbol, font=pf, fill=shadow)
                self.canvas.create_text(x + SQUARE_SIZE // 2,
                                        y + SQUARE_SIZE // 2,
                                        text=symbol, font=pf, fill=fg)

            # Coordinates
            if self.player_color == chess.WHITE:
                if file == 0:
                    self.canvas.create_text(x + 5, y + 5,
                                            text=str(rank + 1),
                                            font=coord_f,
                                            fill=DARK_SQ if is_light else LIGHT_SQ,
                                            anchor="nw")
                if rank == 0:
                    self.canvas.create_text(x + SQUARE_SIZE - 4, y + SQUARE_SIZE - 4,
                                            text=chess.FILE_NAMES[file],
                                            font=coord_f,
                                            fill=DARK_SQ if is_light else LIGHT_SQ,
                                            anchor="se")
            else:
                if file == 7:
                    self.canvas.create_text(x + SQUARE_SIZE - 5, y + 5,
                                            text=str(rank + 1),
                                            font=coord_f,
                                            fill=DARK_SQ if is_light else LIGHT_SQ,
                                            anchor="ne")
                if rank == 7:
                    self.canvas.create_text(x + 4, y + SQUARE_SIZE - 4,
                                            text=chess.FILE_NAMES[file],
                                            font=coord_f,
                                            fill=DARK_SQ if is_light else LIGHT_SQ,
                                            anchor="sw")

    # ── Click Handling ───────────────────────────────────────────────────────

    def _on_click(self, event):
        if self.awaiting_computer:
            return

        sq = self._xy_to_sq(event.x, event.y)

        # In Learning mode, only let the player move on their turn
        if self.mode == "Learning":
            if self.board.turn != self.player_color:
                return

        if self.selected_square is None:
            piece = self.board.piece_at(sq)
            if piece and piece.color == self.board.turn:
                self.selected_square = sq
                self.legal_move_squares = [
                    m.to_square for m in self.board.legal_moves
                    if m.from_square == sq
                ]
                self.hint_square = None
        else:
            move = self._find_move(self.selected_square, sq)
            if move:
                self._make_player_move(move)
            else:
                # Re-select if clicking another own piece
                piece = self.board.piece_at(sq)
                if piece and piece.color == self.board.turn:
                    self.selected_square = sq
                    self.legal_move_squares = [
                        m.to_square for m in self.board.legal_moves
                        if m.from_square == sq
                    ]
                else:
                    self.selected_square = None
                    self.legal_move_squares = []

        self._draw_board()

    def _find_move(self, from_sq, to_sq):
        """Find legal move; auto-promote to queen."""
        for m in self.board.legal_moves:
            if m.from_square == from_sq and m.to_square == to_sq:
                if m.promotion and m.promotion != chess.QUEEN:
                    continue
                return m
        return None

    # ── Move Execution ───────────────────────────────────────────────────────

    def _make_player_move(self, move):
        self.hint_square = None
        tree = self.opening_data["tree"]
        node = get_node_for_board(tree, self.board)

        if self.mode == "Learning":
            # Validate against the opening tree
            expected = [c["move"] for c in (node or {}).get("children", [])]
            if move.uci() not in expected:
                self.status_var.set("⚠ That's not in the opening. Try again!")
                self.selected_square = None
                self.legal_move_squares = []
                self._draw_board()
                self.after(1800, lambda: self.status_var.set(""))
                return

        self.board.push(move)
        self.last_move = move
        self.selected_square = None
        self.legal_move_squares = []
        self._draw_board()
        self._update_info()

        self._schedule_computer_move()

    def _schedule_computer_move(self):
        """Schedule the computer's reply whenever it's not the player's turn."""
        if self.board.turn != self.player_color:
            self.awaiting_computer = True
            if self.mode == "Learning":
                self.status_var.set("Computer is thinking…")
            self.after(500, self._computer_move)

    def _computer_move(self):
        self.awaiting_computer = False
        tree = self.opening_data["tree"]
        node = get_node_for_board(tree, self.board)

        if node is None or not node.get("children"):
            if self.mode == "Learning":
                self.status_var.set("End of prepared opening line.")
            else:
                self.status_var.set("End of book — continue freely or restart.")
            return

        children = node["children"]

        # Filter to legal moves only (sanity check)
        legal_children = [c for c in children
                          if chess.Move.from_uci(c["move"]) in self.board.legal_moves]
        if not legal_children:
            self.status_var.set("Opening database move is invalid here.")
            return

        if len(legal_children) > 1:
            # Let the player choose which variation the opponent plays
            self.status_var.set("")
            self._show_branch_chooser(legal_children)
        else:
            self._play_computer_child(legal_children[0])

    def _play_computer_child(self, child):
        """Execute a single computer move (chosen branch)."""
        move = chess.Move.from_uci(child["move"])
        self.board.push(move)
        self.last_move = move
        self.selected_square = None
        self.legal_move_squares = []
        self._draw_board()
        self._update_info()

        if child.get("trap_mistake"):
            self.status_var.set(
                f"⚠ Opponent mistake! Find the TRAP — check Next Move(s)!"
            )
        elif self.mode == "Learning":
            self.status_var.set("")

        if self.board.turn != self.player_color:
            self._schedule_computer_move()

    def _show_branch_chooser(self, children):
        """Modal dialog: player picks which opponent variation to practice against."""
        # Sort by popularity descending; nodes without popularity get 50 (mid)
        sorted_children = sorted(children,
                                 key=lambda c: c.get("popularity", 50),
                                 reverse=True)

        dialog = tk.Toplevel(self)
        dialog.title("Choose Variation")
        dialog.configure(bg=BG_MAIN)
        dialog.resizable(False, False)
        dialog.transient(self.master)
        dialog.grab_set()

        # Center over main window
        self.master.update_idletasks()
        mx = self.master.winfo_x()
        my = self.master.winfo_y()
        mw = self.master.winfo_width()
        mh = self.master.winfo_height()
        dw, dh = 420, 120 + len(sorted_children) * 72
        dialog.geometry(f"{dw}x{dh}+{mx + (mw - dw)//2}+{my + (mh - dh)//2}")

        hf = tkfont.Font(family="Georgia", size=13, weight="bold")
        sf = tkfont.Font(family="Segoe UI", size=9)
        mf = tkfont.Font(family="Consolas", size=14, weight="bold")
        nf = tkfont.Font(family="Segoe UI", size=10)

        tk.Label(dialog, text="Choose Opponent's Variation",
                 font=hf, bg=BG_MAIN, fg=TEXT_MAIN).pack(padx=20, pady=(16, 2))
        tk.Label(dialog, text="Which line do you want to practice against?",
                 font=sf, bg=BG_MAIN, fg=TEXT_DIM).pack(padx=20, pady=(0, 12))

        for child in sorted_children:
            pop          = child.get("popularity", 50)
            is_mistake   = child.get("trap_mistake", False)
            bar_filled   = round(pop / 10)
            bar_empty    = 10 - bar_filled
            bar_str      = "█" * bar_filled + "░" * bar_empty
            card_bg      = "#3D1515" if is_mistake else BG_CARD

            card = tk.Frame(dialog, bg=card_bg, cursor="hand2")
            card.pack(fill="x", padx=16, pady=5)

            # Top row: popularity bar + label
            top = tk.Frame(card, bg=card_bg)
            top.pack(fill="x", padx=10, pady=(8, 2))
            bar_color = "#E05555" if is_mistake else ACCENT
            tk.Label(top, text=bar_str,
                     font=tkfont.Font(family="Consolas", size=9),
                     bg=card_bg, fg=bar_color).pack(side="left")
            suffix = "  ⚠ Opponent mistake — practice punishing it!" if is_mistake else f"  {pop}% of games"
            suffix_col = "#E05555" if is_mistake else TEXT_DIM
            tk.Label(top, text=suffix,
                     font=sf, bg=card_bg, fg=suffix_col).pack(side="left")

            # Bottom row: move + variation name
            bot = tk.Frame(card, bg=card_bg)
            bot.pack(fill="x", padx=10, pady=(0, 8))
            san_color = "#E05555" if is_mistake else ACCENT
            tk.Label(bot, text=child["san"],
                     font=mf, bg=card_bg, fg=san_color,
                     width=5, anchor="w").pack(side="left")
            tk.Label(bot, text=child["name"],
                     font=nf, bg=card_bg, fg=TEXT_MAIN,
                     wraplength=270, anchor="w").pack(side="left")

            def on_select(c=child, d=dialog):
                d.destroy()
                self._play_computer_child(c)

            def _bind_all(widget, fn):
                widget.bind("<Button-1>", lambda e, f=fn: f())
                for child_widget in widget.winfo_children():
                    _bind_all(child_widget, fn)

            _bind_all(card, on_select)

    # ── Info Panel Updates ───────────────────────────────────────────────────

    def _update_info(self):
        tree = self.opening_data["tree"]
        node = get_node_for_board(tree, self.board)

        # ── Variation path ───────────────────────────────────────────────────
        path = get_variation_path(tree, self.board)
        self.variation_var.set(path[-1] if path else "—")

        # ── Next moves (Learning mode only) ──────────────────────────────────
        if self.mode == "Learning":
            for w in self.next_moves_frame.winfo_children():
                w.destroy()

            children = (node or {}).get("children", [])
            # Only show moves for the side whose turn it is
            player_children = [
                c for c in children
                if chess.Move.from_uci(c["move"]) in self.board.legal_moves
            ]

            if not player_children and not children:
                tk.Label(self.next_moves_frame,
                         text="  Opening line complete!",
                         font=tkfont.Font(family="Segoe UI", size=9),
                         bg=BG_CARD, fg=TEXT_DIM,
                         padx=8, pady=4).pack(anchor="w")
            elif player_children:
                for c in player_children:
                    is_trap = c.get("trap", False)
                    row_bg  = "#1E2A10" if is_trap else BG_CARD
                    row = tk.Frame(self.next_moves_frame, bg=row_bg)
                    row.pack(fill="x")

                    san_lbl = ("🪤 " + c["san"]) if is_trap else f"  {c['san']}"
                    san_col = "#7EC832" if is_trap else ACCENT
                    tk.Label(row, text=san_lbl,
                             font=tkfont.Font(family="Consolas", size=11, weight="bold"),
                             bg=row_bg, fg=san_col,
                             width=10, anchor="w",
                             padx=4, pady=3).pack(side="left")

                    name_text = c.get("trap_name", c["name"]) if is_trap else c["name"]
                    name_col  = "#A8D860" if is_trap else TEXT_MAIN
                    tk.Label(row, text=name_text,
                             font=tkfont.Font(family="Segoe UI", size=9),
                             bg=row_bg, fg=name_col,
                             anchor="w", wraplength=180).pack(side="left", padx=(0, 4))
            else:
                # Computer's turn — show what the computer will play
                c = children[0]
                tk.Label(self.next_moves_frame,
                         text=f"  Computer plays: {c['san']}",
                         font=tkfont.Font(family="Segoe UI", size=9),
                         bg=BG_CARD, fg=TEXT_DIM,
                         padx=8, pady=4).pack(anchor="w")

        # ── Commentary ───────────────────────────────────────────────────────
        comment = (node or {}).get("comment", "")
        if not comment and node is None:
            comment = "You've deviated from the opening. Explore freely!"
        self._set_comment(comment)

        # ── Move history (color-coded) ────────────────────────────────────────
        self.history_text.config(state="normal")
        self.history_text.delete("1.0", "end")

        temp_board = chess.Board()
        if not self.board.move_stack:
            self.history_text.insert("end", "—", "num")
        else:
            for i, move in enumerate(self.board.move_stack):
                san = temp_board.san(move)
                is_white_move = (i % 2 == 0)
                is_player_move = (
                    (is_white_move and self.player_color == chess.WHITE) or
                    (not is_white_move and self.player_color == chess.BLACK)
                )

                if is_white_move:
                    move_num = i // 2 + 1
                    if i > 0:
                        self.history_text.insert("end", "\n")
                    self.history_text.insert("end", f"{move_num}. ", "num")

                tag = "you" if is_player_move else ("white" if is_white_move else "black")
                self.history_text.insert("end", san, tag)

                if not is_white_move:
                    pass  # newline handled at next white move
                else:
                    self.history_text.insert("end", "  ")  # space before black's move

                temp_board.push(move)

        self.history_text.see("end")
        self.history_text.config(state="disabled")

        # ── Status (Practice mode) ───────────────────────────────────────────
        if self.mode == "Practice":
            if node is not None and node.get("children"):
                n = len(node["children"])
                self.status_var.set(f"{n} branch{'es' if n > 1 else ''} available")
            else:
                self.status_var.set("Opening line complete!")

    def _set_comment(self, text):
        self.comment_text.config(state="normal")
        self.comment_text.delete("1.0", "end")
        self.comment_text.insert("end", text)
        self.comment_text.config(state="disabled")

    # ── Controls ─────────────────────────────────────────────────────────────

    def _undo_move(self):
        self.hint_square = None
        if self.mode == "Learning":
            # Undo two moves (player + computer)
            for _ in range(2):
                if self.board.move_stack:
                    self.board.pop()
        else:
            if self.board.move_stack:
                self.board.pop()

        self.last_move = self.board.peek() if self.board.move_stack else None
        self.selected_square = None
        self.legal_move_squares = []
        self.awaiting_computer = False
        self.status_var.set("")
        self._draw_board()
        self._update_info()

    def _restart(self):
        self.board = chess.Board()
        self.selected_square = None
        self.legal_move_squares = []
        self.last_move = None
        self.hint_square = None
        self.awaiting_computer = False
        self.status_var.set("")
        self._draw_board()
        self._update_info()
        self._schedule_computer_move()

    def _show_hint(self):
        """Show the next book move as a hint (Practice mode only)."""
        tree = self.opening_data["tree"]
        node = get_node_for_board(tree, self.board)
        if node and node.get("children"):
            # Find book children that are legal on the current board
            valid_children = [
                c for c in node["children"]
                if chess.Move.from_uci(c["move"]) in self.board.legal_moves
            ]
            if valid_children:
                move = chess.Move.from_uci(valid_children[0]["move"])
                self.hint_square = move.from_square
                self.status_var.set(f"Hint: {chess.square_name(move.from_square)} → {chess.square_name(move.to_square)}")
                self._draw_board()
            else:
                self.status_var.set("No hint available at this position.")
        else:
            self.status_var.set("No book moves — opening is complete!")


# ── Entry Point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    app = ChessOpeningsApp()
    # Center the window
    app.update_idletasks()
    w = app.winfo_width()
    h = app.winfo_height()
    sw = app.winfo_screenwidth()
    sh = app.winfo_screenheight()
    app.geometry(f"+{(sw - w) // 2}+{(sh - h) // 2}")
    app.mainloop()
