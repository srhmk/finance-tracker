import tkinter as tk
from tkinter import Canvas

def round_rectangle(canvas, x1, y1, x2, y2, radius=25, **kwargs):
    points = [
        x1 + radius, y1,
        x1 + radius, y1,
        x2 - radius, y1,
        x2 - radius, y1,
        x2, y1,
        x2, y1 + radius,
        x2, y1 + radius,
        x2, y2 - radius,
        x2, y2 - radius,
        x2, y2,
        x2 - radius, y2,
        x2 - radius, y2,
        x1 + radius, y2,
        x1 + radius, y2,
        x1, y2,
        x1, y2 - radius,
        x1, y2 - radius,
        x1, y1 + radius,
        x1, y1 + radius,
        x1, y1
    ]
    return canvas.create_polygon(points, smooth=True, **kwargs)

def create_rounded_entry(parent, x, y, width, height, radius, **entry_options):
    canvas = Canvas(parent, width=width, height=height, highlightthickness=0, bg=parent['bg'])
    canvas.place(x=x, y=y)

    # Draw a rounded rectangle
    round_rectangle(canvas, 0, 0, width, height, radius=radius, fill="white", outline="#cccccc")

    # Create an Entry widget
    entry = tk.Entry(parent, **entry_options)
    entry.place(x=x + radius // 2, y=y + radius // 2, width=width - radius, height=height - radius)

    return entry

# Example Usage
root = tk.Tk()
root.geometry("400x300")
root.configure(bg="lightblue")

# Create a rounded Entry widget
rounded_entry = create_rounded_entry(root, x=50, y=50, width=300, height=50, radius=20, font=("Helvetica", 14))
rounded_entry.insert(0, "Rounded Entry")

root.mainloop()
