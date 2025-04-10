import customtkinter as tk
from zen_explorer_core.models.theme import Theme
from ui import utils

class ThemeFrame(tk.CTkFrame):
    def __init__(self, theme: Theme, parent, controller: tk.CTk):
        super().__init__(parent)
        self.name = theme.name
        self.author = theme.author
        self.description = theme.description
        self.thumbnail = utils.get_image('https://raw.githubusercontent.com/greeeen-dev/natsumi-browser/refs/heads/main/images/home.png') # in the future theme.thumbnail
        # self.pack(fill="both", expand=True)
        self.grid(row=0, column=0, sticky="nsew")
        self.create_widgets()

    def create_widgets(self):
        # Create widgets for the theme frame
        tk.CTkLabel(self, text=self.name).pack()
        tk.CTkLabel(self, text=self.author).pack()
        tk.CTkLabel(self, text=self.description).pack()
        tk.CTkLabel(self, text='', image=utils.to_ctkimage(self.thumbnail)).pack()