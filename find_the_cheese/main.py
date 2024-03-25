import tkinter as tk

from find_the_cheese.cheese_app import CheeseApp

if __name__ == "__main__":
    root = tk.Tk()
    app = CheeseApp(root)
    root.mainloop()
