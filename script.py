from cx_Freeze import setup, Executable

setup(
    name="Finance Tracker",
    version="1.12.10",
    description="Basic yet powerful Finance tracking system",
    executables=[Executable("main.py")],  # Replace with your script
)