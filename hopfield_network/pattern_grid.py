import tkinter as tk


class PatternGrid(tk.Canvas):
    """
    A grid of fields to represent a pattern
    """
    def __init__(self, master, size: int, clickable: bool = True, *args, **kwargs):
        self.size = size
        self.field_width = 50
        self.clickable = clickable
        width = self.size * self.field_width
        tk.Canvas.__init__(self, master, width=width, height=width, *args, **kwargs)
        self.pattern = [[0 for _ in range(self.size)] for _ in range(self.size)]
        self.create_grid()

    def create_grid(self) -> None:
        """
        Create grid of fields in the canvas
        :return: None
        """
        for row in range(self.size):
            for col in range(self.size):
                x1 = col * self.field_width
                y1 = row * self.field_width
                x2 = x1 + self.field_width
                y2 = y1 + self.field_width
                rect = self.create_rectangle(x1, y1, x2, y2, fill="white", width=1)
                if self.clickable:
                    self.tag_bind(rect, "<Button-1>", lambda event, row=row, col=col: self.on_click_field(row, col))

    def on_click_field(self, row: int, col: int) -> None:
        """
        Change color and value of the field
        :param row: index of row
        :param col: index of column
        :return: None
        """
        self.pattern[row][col] = int(not self.pattern[row][col])
        self.update_color(row, col)

    def update_color(self, row: int, col: int) -> None:
        """
        Update color of the field
        :param row: index of row
        :param col: index of column
        :return: None
        """
        color = "white" if self.pattern[row][col] == 0 else "black"
        self.itemconfig(row * self.size + col + 1, fill=color)

    def update_color_all(self) -> None:
        """
        Update color of all fields in the grid
        :return: None
        """
        for row in range(self.size):
            for col in range(self.size):
                self.update_color(row, col)
