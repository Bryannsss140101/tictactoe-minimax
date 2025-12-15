import tkinter as tk
from .ui_app import TicTacToeApp


def main():
    root = tk.Tk()
    TicTacToeApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
