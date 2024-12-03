import tkinter as tk
from tkinter import ttk

# Main Window
root = tk.Tk()
root.title("Custom Scrollbar Example")
root.geometry("400x300")

# Define Style
style = ttk.Style()
style.theme_use("default")  # Use the default theme

# Customizing the Scrollbar
style.configure("Custom.Vertical.TScrollbar",
                gripcount=0,
                background="blue",
                darkcolor="darkblue",
                lightcolor="lightblue",
                troughcolor="gray",
                bordercolor="black",
                arrowcolor="lightblue")

# Adding a Scrollbar
frame = tk.Frame(root)
frame.pack(fill="both", expand=True)

text = tk.Text(frame, wrap="none", height=10, width=40)
text.pack(side="left", fill="both", expand=True)

# Scrollbar with the Custom Style
scrollbar = ttk.Scrollbar(frame, orient="vertical", style="Custom.Vertical.TScrollbar", command=text.yview)
scrollbar.pack(side="right", fill="y")

text.configure(yscrollcommand=scrollbar.set)

# Add some sample text
for i in range(1, 101):
    text.insert("end", f"Line {i}\n")

# Run the Application
root.mainloop()