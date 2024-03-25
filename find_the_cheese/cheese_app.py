import tkinter as tk
import random
from typing import Tuple

from find_the_cheese.pattern_grid import GridObject
from find_the_cheese.pattern_grid import PatternGrid
from find_the_cheese.qmatrix import QMatrix
from find_the_cheese.rmatirx import RMatrix


class CheeseApp:
    def __init__(self, root: tk.Tk):
        self.learning_rate = 0.1

        self.size = 4
        self.q_matrix = QMatrix(self.size)
        self.r_matrix = RMatrix(self.size)
        self.root = root
        self.root.geometry("800x800")
        self.root.title("Hopfield")

        self.current_object = GridObject.LAND

        self.pattern_field = PatternGrid(self.root, size=self.size, current_object=self.current_object)
        self.pattern_field.grid(row=0, column=0, padx=10, pady=10)

        self.button_frame = tk.Frame(self.root)
        self.button_frame.grid(row=0, column=1, padx=10, pady=10)

        self.objects = [obj.value for obj in GridObject]
        self.current_object_label = tk.Label(self.root, text=f"Current object: {self.objects[0]}")
        self.current_object_label.grid(row=1, column=0, columnspan=2)

        self.object_button = tk.Button(self.button_frame, text=f"Change Object to {self.objects[1]}",
                                       command=self.change_object)
        self.object_button.grid(row=0, column=0, pady=5)

        self.start_learning_button = tk.Button(self.button_frame, text="Learn", command=self.start_learning)
        self.start_learning_button.grid(row=1, column=0, pady=5)

        self.find_cheese_button = tk.Button(self.button_frame, text="Find Cheese", command=self.find_cheese)
        self.find_cheese_button.grid(row=2, column=0, pady=5)

        self.show_matrix_button = tk.Button(self.button_frame, text="Show R Matrix", command=self.show_r_matrix)
        self.show_matrix_button.grid(row=3, column=0, pady=5)

        self.show_memory_matrix_button = tk.Button(self.button_frame, text="Show Q Matrix", command=self.show_q_matrix)
        self.show_memory_matrix_button.grid(row=4, column=0, pady=5)

        self.output_text = tk.Label(self.root, text="")
        self.output_text.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

    def change_object(self):
        current_index = self.objects.index(self.current_object.value)
        next_index = (current_index + 1) % len(self.objects)
        self.current_object = GridObject(self.objects[next_index])
        self.pattern_field.change_object_placement(self.current_object)
        self.current_object_label.config(text=f"Current object: {self.current_object.value}")
        next_index = (next_index + 1) % len(self.objects)
        self.object_button.config(text=f"Change Object to {self.objects[next_index]}")

    def start_learning(self):
        self.r_matrix.set_pattern(self.pattern_field)
        self.q_matrix.reset()

        max_epochs = 1000
        for _ in range(max_epochs):
            position = random.randint(0, self.size - 1), random.randint(0, self.size - 1)
            for step in range(100):
                new_position = self.r_matrix.choose_new_position(position)

                reward = self.pattern_field.move_object(position, new_position)

                best_next = self.q_matrix.get_best_q_value(new_position)
                new_value = reward + self.learning_rate * best_next
                self.q_matrix.set_q_value(position, new_position, new_value)

                position = new_position

                if self.pattern_field.is_cheese(*new_position) or self.pattern_field.is_trap(*new_position):
                    break

        print("Learning finished.")

    def find_cheese(self):
        mouse_position = self.pattern_field.get_mouse_position()
        if mouse_position is None:
            print("Mouse not placed in the grid.")
            return

        self.find_cheese_step(mouse_position, 0, 100)

    def find_cheese_step(self, position: Tuple[int, int], step_count: int, max_steps: int):
        if step_count >= max_steps:
            print("Reached maximum number of steps without finding the cheese.")
            return

        step_count += 1
        new_position = self.q_matrix.get_best_new_position(position)

        finished = False
        if self.pattern_field.is_cheese(*new_position):
            print(f"Found cheese in {step_count} steps.")
            finished = True

        if self.pattern_field.is_trap(*new_position):
            print("Mouse got trapped.")
            finished = True

        self.pattern_field.move_object(position, new_position, True)

        if not finished:
            self.root.after(300, self.find_cheese_step, new_position, step_count, max_steps)

    def show_q_matrix(self):
        self.pattern_field.toggle_values_display(self.q_matrix)

    def show_r_matrix(self):
        self.pattern_field.toggle_values_display(self.r_matrix)


if __name__ == "__main__":
    root = tk.Tk()
    app = CheeseApp(root)
    root.mainloop()
