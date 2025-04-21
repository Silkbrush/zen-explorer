from PIL import Image
import customtkinter as tk
from zen_explorer_core.models.theme import Theme
from .tkmd import create_markdown_viewer_frame
from ui import utils
import markdown
from github import Github
import re
import time

class ThemeFrame(tk.CTkFrame):
    def __init__(self, theme: Theme, parent, controller):
        super().__init__(parent)
        self.github = Github()
        self.name = theme.name
        self.author = theme.author
        self.description = theme.description
        self.homepage = theme.homepage
        self.thumbnail = utils.get_image('https://raw.githubusercontent.com/greeeen-dev/natsumi-browser/refs/heads/main/images/home.png') # in the future theme.thumbnail

        self.container = tk.CTkFrame(self, fg_color='transparent')
        self.container.grid(row=0, column=0, sticky="nsew", padx=20, pady=20) # Reduced padding a bit

        self.container.grid_columnconfigure(0, weight=1)
        self.container.grid_rowconfigure(2, weight=1)

        self.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.create_widgets()
        self.controller = controller

    def create_widgets(self):
        # Create widgets for the theme frame
        self.thumbnail = utils.get_image('https://raw.githubusercontent.com/greeeen-dev/natsumi-browser/refs/heads/main/images/home.png') # PIL image

        author_name_frame = tk.CTkFrame(self.container, fg_color='transparent')
        author_name_frame.pack(anchor="s", pady=(0, 10), expand=True)

        # Create a subframe to vertically align labels at the bottom
        label_frame = tk.CTkFrame(author_name_frame, fg_color='transparent')
        label_frame.pack(anchor="s", side=tk.BOTTOM, expand=True)

        name_label = tk.CTkLabel(label_frame, text=self.name, font=("Helvetica", 40, "bold"))
        name_label.pack(anchor="s", side="left", expand=True)

        author_label = tk.CTkLabel(label_frame, text=f" by {self.author}", font=("Helvetica", 20))
        author_label.pack(anchor="s", side="left", expand=True)

        description_label = tk.CTkLabel(self.container, text=self.description)
        description_label.pack(expand=True)

        home_icon = Image.open('ui/icon/home.png')
        home_button = tk.CTkButton(self.container, text="", image=utils.to_ctkimage(home_icon, (20, 20)), command=lambda: self.controller.show_frame('main'))
        home_button.configure(width=20, height=20)
        home_button.place(anchor="nw", x=10, y=10)

    def add_readme(self):
        markdown_viewer_frame = create_markdown_viewer_frame(self.container, self.get_readme())
        markdown_viewer_frame.pack(expand=True, fill='both')
        
    def get_readme(self):
        try:
            pattern = r"^https?://github\.com/([^/]+/[^/]+)"
            match = re.search(pattern, self.homepage)
            return self.github.get_repo(match.group(1)).get_readme().decoded_content.decode('utf-8')
        except Exception as e:
            return 'No README available'