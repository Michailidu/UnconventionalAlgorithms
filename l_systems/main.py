import tkinter as tk
import math


class DrawApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Draw Lines App")

        self.canvas = tk.Canvas(master, width=400, height=400, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.canvas.bind("<Button-1>", self.on_click)
        self.axiom = "F+F+F+F"
        self.angle_delta = 90
        self.rule = "F+F-F-FF+F+F-F"
        self.line_length = 10
        self.current_position = (300, 300)
        self.nesting = 3
        self.angle = 90

    def draw_line(self, x, y, length, angle) -> tuple[int, int]:
        angle_rad = math.radians(angle)

        x_end = x + length * math.cos(angle_rad)
        y_end = y - length * math.sin(angle_rad)

        self.canvas.create_line(x, y, x_end, y_end)

        return x_end, y_end

    def on_click(self, event):
        self.canvas.delete("all")

        result = self.axiom
        for _ in range(self.nesting - 1):
            result = result.replace("F", self.rule)

        stack = []
        for char in result:
            if char == "F":
                x, y = self.current_position
                self.draw_line(x, y, self.line_length, self.angle)
                self.current_position = self.draw_line(x, y, self.line_length, self.angle)
            elif char == "+":
                self.angle += self.angle_delta
            elif char == "-":
                self.angle -= self.angle_delta
            elif char == "[":
                stack.append((self.current_position, self.angle))
            elif char == "]":
                self.current_position, self.angle = stack.pop()


def main():
    root = tk.Tk()
    app = DrawApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
