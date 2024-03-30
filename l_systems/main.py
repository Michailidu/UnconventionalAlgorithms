import tkinter as tk
import math


class DrawApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Draw Lines App")

        self.canvas_frame = tk.Frame(master)
        self.canvas_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.canvas = tk.Canvas(self.canvas_frame, width=400, height=400, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.canvas.bind("<Configure>", self.on_canvas_resize)

        self.inputs_frame = tk.Frame(master)
        self.inputs_frame.pack(side=tk.RIGHT, padx=10, pady=10)

        tk.Label(self.inputs_frame, text="Axiom:").pack()
        self.axiom_entry = tk.Entry(self.inputs_frame)
        self.axiom_entry.insert(0, "F+F+F+F")
        self.axiom_entry.pack()

        tk.Label(self.inputs_frame, text="Angle Delta:").pack()
        self.angle_delta_entry = tk.Entry(self.inputs_frame)
        self.angle_delta_entry.insert(0, "90")
        self.angle_delta_entry.pack()

        tk.Label(self.inputs_frame, text="Rule:").pack()
        self.rule_entry = tk.Entry(self.inputs_frame)
        self.rule_entry.insert(0, "F+F-F-FF+F+F-F")
        self.rule_entry.pack()

        tk.Label(self.inputs_frame, text="Line Length:").pack()
        self.line_length_entry = tk.Entry(self.inputs_frame)
        self.line_length_entry.insert(0, "10")
        self.line_length_entry.pack()

        tk.Label(self.inputs_frame, text="Nesting:").pack()
        self.nesting_entry = tk.Entry(self.inputs_frame)
        self.nesting_entry.insert(0, "3")
        self.nesting_entry.pack()

        self.draw_button = tk.Button(self.inputs_frame, text="Draw", command=self.on_click)
        self.draw_button.pack()

        self.axiom = self.axiom_entry.get()
        self.angle_delta = float(self.angle_delta_entry.get())
        self.rule = self.rule_entry.get()
        self.line_length = int(self.line_length_entry.get())
        self.current_position = (0, 0)
        self.reset_position()
        self.nesting = int(self.nesting_entry.get())
        self.angle = 90

    def reset_position(self):
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        self.current_position = (canvas_width // 2, canvas_height // 2)

    def on_canvas_resize(self, event):
        self.reset_position()

    def draw_line(self, x, y, length, angle) -> tuple[int, int]:
        angle_rad = math.radians(angle)

        x_end = x + length * math.cos(angle_rad)
        y_end = y - length * math.sin(angle_rad)

        self.canvas.create_line(x, y, x_end, y_end)

        return x_end, y_end

    def on_click(self):
        self.canvas.delete("all")
        self.reset_position()
        self.axiom = self.axiom_entry.get()
        self.angle_delta = float(self.angle_delta_entry.get())
        self.rule = self.rule_entry.get()
        self.line_length = int(self.line_length_entry.get())
        self.nesting = int(self.nesting_entry.get())

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
