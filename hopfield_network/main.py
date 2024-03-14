import tkinter as tk

from hopfield_network.hopfield_app import HopfieldApp

if __name__ == "__main__":
    root = tk.Tk()
    app = HopfieldApp(root)
    root.mainloop()
