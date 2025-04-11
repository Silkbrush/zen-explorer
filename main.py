import customtkinter as tk
import time

from typing import Optional, Tuple

from ui import MainContent, ThemesApp

from ui import utils
from cli import repository


repo = repository.data

# Check if repository is available
if repo is None:
    print("WARNING: Repository data could not be loaded. Some features may not be available.", file=sys.stderr)
    print("Use the 'update' command to fetch the repository data.", file=sys.stderr)

images = []
allow_resize_on = time.time()
resize_delay = 0.05

# config
tk.set_appearance_mode("System") # Light or Dark

# running the app
root = ThemesApp()
root.geometry("800x600")
root.update()
root.mainloop()
