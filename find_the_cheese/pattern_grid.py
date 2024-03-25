import tkinter as tk
from PIL import Image, ImageTk
from enum import Enum
from typing import Optional


class GridObject(Enum):
    LAND = "land"
    WALL = "wall"
    MOUSE = "mouse"
    TRAP = "trap"
    CHEESE = "cheese"


rewards = {
    GridObject.LAND: 0,
    GridObject.WALL: -1,
    GridObject.TRAP: -1000,
    GridObject.CHEESE: 100,
    GridObject.MOUSE: 0
}


def resize_image(filename: str, size: int) -> ImageTk.PhotoImage:
    original_image = Image.open(filename)
    original_image = original_image.resize((size, size))
    return ImageTk.PhotoImage(original_image)


class PatternGrid(tk.Canvas):
    def __init__(self, master, size: int, current_object: GridObject, clickable: bool = True, *args, **kwargs):
        self.size = size
        self.field_width = 70
        self.clickable = clickable
        self.current_object = current_object
        self.image_mapping = {
            GridObject.LAND: resize_image("images/land.png", self.field_width),
            GridObject.WALL: resize_image("images/wall.png", self.field_width),
            GridObject.MOUSE: resize_image("images/mouse.png", self.field_width),
            GridObject.TRAP: resize_image("images/trap.png", self.field_width),
            GridObject.CHEESE: resize_image("images/cheese.png", self.field_width)
        }
        width = self.size * self.field_width
        tk.Canvas.__init__(self, master, width=width, height=width, *args, **kwargs)
        self.pattern = [[GridObject.LAND for _ in range(self.size)] for _ in range(self.size)]
        self.create_grid()
        self.showing_values = False

    def create_grid(self) -> None:
        for row in range(self.size):
            for col in range(self.size):
                x1 = col * self.field_width
                y1 = row * self.field_width
                image = self.image_mapping[GridObject.LAND]
                rect = self.create_image(x1, y1, anchor=tk.NW, image=image)
                if self.clickable:
                    self.tag_bind(rect, "<Button-1>", lambda event, row=row, col=col: self.on_click_field(row, col))

    def on_click_field(self, row: int, col: int) -> None:
        self.pattern[row][col] = self.current_object
        self.update_image(row, col)

    def update_image(self, row: int, col: int) -> None:
        image = self.image_mapping[self.pattern[row][col]]
        self.itemconfig(row * self.size + col + 1, image=image)

    def update_image_all(self) -> None:
        for row in range(self.size):
            for col in range(self.size):
                self.update_image(row, col)

    def change_object_placement(self, object_type: GridObject) -> None:
        self.current_object = object_type

    def move_object(self, old_position: tuple[int, int], new_position: tuple[int, int], visualize: bool = False) -> int:
        old_row, old_col = old_position
        new_row, new_col = new_position
        reward = rewards[self.pattern[new_row][new_col]]
        if visualize:
            self.pattern[old_row][old_col] = GridObject.LAND
            self.pattern[new_row][new_col] = GridObject.MOUSE
            self.update_image(old_row, old_col)
            self.update_image(new_row, new_col)
        return reward

    def is_trap(self, row: int, col: int) -> bool:
        return self.pattern[row][col] == GridObject.TRAP

    def is_cheese(self, row: int, col: int) -> bool:
        return self.pattern[row][col] == GridObject.CHEESE

    def get_mouse_position(self) -> Optional[tuple[int, int]]:
        for row in range(self.size):
            for col in range(self.size):
                if self.pattern[row][col] == GridObject.MOUSE:
                    return row, col
        return None

    def get_reward(self, row: int, col: int) -> int:
        return rewards[self.pattern[row][col]]

    def toggle_values_display(self, matrix) -> None:
        if self.showing_values:
            for row in range(self.size):
                for col in range(self.size):
                    self.delete(f"value_{row}_{col}")
            self.showing_values = False
        else:
            for row in range(self.size):
                for col in range(self.size):
                    values = matrix.get_neighbor_values((row, col))
                    max_value = max([v for v in values if v is not None])

                    pad = 12
                    positions = [(self.field_width - pad, self.field_width // 2),
                                 (self.field_width // 2, self.field_width - pad),
                                 (pad, self.field_width // 2),
                                 (self.field_width // 2, pad)]

                    positions = [(x + col * self.field_width, y + row * self.field_width) for x, y in positions]

                    for value, position in zip(values, positions):
                        if value is not None:
                            color = 'green' if value == max_value else 'red'
                            tag = f"value_{row}_{col}"
                            self.create_text(position,
                                             text=f"{value:.2f}",
                                             fill=color,
                                             font=('Helvetica', 8, 'bold'),
                                             anchor='center',
                                             tags=tag)
            self.showing_values = True
