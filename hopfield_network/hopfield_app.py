import tkinter as tk

import numpy as np

from hopfield_network.network import HopfieldNetwork
from hopfield_network.pattern_grid import PatternGrid
from hopfield_network.pattern_viewer import PatternViewer


class HopfieldApp:
    """
    Main application window for Hopfield network app
    """
    def __init__(self, root: tk.Tk):
        size = 4
        self.hopfield_network = HopfieldNetwork(size)
        self.root = root
        self.root.geometry("800x800")
        self.root.title("Hopfield")

        self.pattern_field = PatternGrid(self.root, size=size)
        self.pattern_field.grid(row=0, column=0, padx=10, pady=10)

        self.button_frame = tk.Frame(self.root)
        self.button_frame.grid(row=0, column=1, padx=10, pady=10)

        buttons = ["Save Pattern", "Recover Pattern Sync", "Recover Pattern Async", "Remove Pattern",
                   "Remove All Patterns", "View All Patterns"]
        commands = [self.save_pattern, self.recover_pattern_sync, self.recover_pattern_async, self.remove_pattern,
                    self.remove_all_patterns, self.view_all_patterns]
        idx = 0
        for _, button_text in enumerate(buttons):
            button = tk.Button(self.button_frame, text=buttons[idx], command=lambda cmd=commands[idx]: cmd())
            button.grid(row=idx, column=0, pady=5)
            idx += 1

        self.output_text = tk.Label(self.root, text="")
        self.output_text.grid(row=idx, column=0, columnspan=2, padx=10, pady=10)

    def get_current_pattern(self) -> np.ndarray:
        pattern = self.pattern_field.pattern
        pattern = np.array(pattern)
        return pattern

    def perform_action_with_pattern(self, action: callable, action_text: str) -> None:
        pattern = self.get_current_pattern()
        self.pattern_field.pattern = action(pattern)
        self.output_text.config(text=action_text)
        self.pattern_field.update_color_all()

    def save_pattern(self) -> None:
        self.perform_action_with_pattern(self.hopfield_network.add_pattern, "Pattern saved")

    def recover_pattern_sync(self) -> None:
        self.perform_action_with_pattern(self.hopfield_network.recover_sync, "Pattern recovered sync")

    def recover_pattern_async(self) -> None:
        self.perform_action_with_pattern(self.hopfield_network.recover_async, "Pattern recovered async")

    def remove_pattern(self) -> None:
        self.perform_action_with_pattern(self.hopfield_network.remove_pattern, "Pattern removed")

    def remove_all_patterns(self) -> None:
        self.hopfield_network.remove_all_patterns()
        self.output_text.config(text="All patterns removed")

    def view_all_patterns(self) -> None:
        patterns = self.hopfield_network.get_all_patterns()
        if patterns:
            pattern_viewer = PatternViewer(self.root, patterns)
            pattern_viewer.title("All Patterns")
        else:
            self.output_text.config(text="No patterns saved yet")