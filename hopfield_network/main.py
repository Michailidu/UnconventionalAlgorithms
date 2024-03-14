import tkinter as tk

import numpy as np

from hopfield_network.network import HopfieldNetwork


class PatternGrid(tk.Canvas):
    def __init__(self, master, size, *args, **kwargs):
        self.size = size
        self.field_width = 50
        width = self.size * self.field_width
        tk.Canvas.__init__(self, master, width=width, height=width, *args, **kwargs)
        self.pattern = [[0 for _ in range(self.size)] for _ in range(self.size)]
        self.create_grid()

    def create_grid(self):
        for row in range(self.size):
            for col in range(self.size):
                x1 = col * self.field_width
                y1 = row * self.field_width
                x2 = x1 + self.field_width
                y2 = y1 + self.field_width
                rect = self.create_rectangle(x1, y1, x2, y2, fill="white", width=1)
                self.tag_bind(rect, "<Button-1>", lambda event, row=row, col=col: self.on_click_field(row, col))

    def on_click_field(self, row, col):
        self.pattern[row][col] = int(not self.pattern[row][col])
        self.update_color(row, col)

    def update_color(self, row, col):
        color = "white" if self.pattern[row][col] == 0 else "black"
        self.itemconfig(row * self.size + col + 1, fill=color)

    def update_color_all(self):
        for row in range(self.size):
            for col in range(self.size):
                self.update_color(row, col)


class MyApp:
    def __init__(self, root):
        size = 4
        self.hopfield_network = HopfieldNetwork(size)
        self.root = root
        self.root.geometry("800x800")
        self.root.title("Hopfield")

        self.pattern_field = PatternGrid(self.root, size=size)
        self.pattern_field.grid(row=0, column=0, padx=10, pady=10)

        self.button_frame = tk.Frame(self.root)
        self.button_frame.grid(row=0, column=1, padx=10, pady=10)

        buttons = ["Save Pattern", "Recover Pattern Sync", "Recover Pattern Async", "Remove Pattern", "Remove All Patterns"]
        commands = [self.save_pattern, self.recover_pattern_sync, self.recover_pattern_async, self.remove_pattern, self.remove_all_patterns]
        idx = 0
        for _, button_text in enumerate(buttons):
            button = tk.Button(self.button_frame, text=buttons[idx], command=lambda cmd=commands[idx]: cmd())
            button.grid(row=idx, column=0, pady=5)
            idx += 1

        self.output_text = tk.Label(self.root, text="")
        self.output_text.grid(row=idx, column=0, columnspan=2, padx=10, pady=10)

    def get_current_pattern(self):
        pattern = self.pattern_field.pattern
        pattern = np.array(pattern)
        return pattern

    def perform_action_with_pattern(self, action, action_text):
        pattern = self.get_current_pattern()
        self.pattern_field.pattern = action(pattern)
        self.output_text.config(text=action_text)
        self.pattern_field.update_color_all()

    def save_pattern(self):
        self.perform_action_with_pattern(self.hopfield_network.add_pattern, "Pattern saved")

    def recover_pattern_sync(self):
        self.perform_action_with_pattern(self.hopfield_network.recover_sync, "Pattern recovered sync")

    def recover_pattern_async(self):
        self.perform_action_with_pattern(self.hopfield_network.recover_async, "Pattern recovered async")

    def remove_pattern(self):
        self.perform_action_with_pattern(self.hopfield_network.remove_pattern, "Pattern removed")

    def remove_all_patterns(self):
        self.hopfield_network.remove_all_patterns()
        self.output_text.config(text="All patterns removed")


if __name__ == "__main__":
    root = tk.Tk()
    app = MyApp(root)
    root.mainloop()
