import tkinter as tk

from hopfield_network.pattern_grid import PatternGrid


class PatternViewer(tk.Toplevel):
    def __init__(self, master, patterns):
        tk.Toplevel.__init__(self, master)
        self.patterns = patterns
        self.current_index = 0

        self.pattern_field = PatternGrid(self, size=len(patterns[0]), clickable=False)
        self.pattern_field.grid(row=0, column=0, padx=10, pady=10)

        self.next_button = tk.Button(self, text="Next", command=self.next_pattern)
        self.next_button.grid(row=1, column=0, padx=5, pady=5, sticky="e")

        self.prev_button = tk.Button(self, text="Previous", command=self.prev_pattern)
        self.prev_button.grid(row=1, column=0, padx=5, pady=5, sticky="w")

        self.show_pattern()

    def show_pattern(self):
        self.pattern_field.pattern = self.patterns[self.current_index]
        self.pattern_field.update_color_all()

    def next_pattern(self):
        self.current_index = (self.current_index + 1) % len(self.patterns)
        self.show_pattern()

    def prev_pattern(self):
        self.current_index = (self.current_index - 1) % len(self.patterns)
        self.show_pattern()
