import customtkinter as tk
from zen_explorer_core.repository import RepositoryData
from zen_explorer_core.models.theme import Theme
from ui import utils
from .theme_frame import ThemeFrame
import time

class MainContent(tk.CTkFrame):
    def __init__(self, parent, controller, theme_container, repo: RepositoryData, max_col=3):
        super().__init__(parent)
        self.repo = repo
        self.theme_container = theme_container
        self.controller = controller
        self.parent = parent
        self.max_col = max_col
        for col in range(max_col):
            self.grid_columnconfigure(col, weight=1, uniform="column")

    def update_main(self):
        # Reset main content
        global allow_resize_on
        for child in self.winfo_children():
            child.destroy()
        images = []
        allow_resize_on = time.time()

        row = 0
        col = 0

        thumbnail = utils.get_image('https://raw.githubusercontent.com/greeeen-dev/natsumi-browser/refs/heads/main/images/home.png')

        for theme in self.repo.themes:
            theme_data = self.repo.get_theme(theme)

            # Main frame
            theme_frame = tk.CTkFrame(self)
            theme_frame.configure(fg_color='transparent', corner_radius=0)
            theme_frame.grid(row=row, column=col, padx=10, pady=10, sticky="ew")

            # Thumbnail (PLEASE LET THIS FUCKING WORK) :)
            theme_thumbnail = tk.CTkButton(theme_frame, text="", image=utils.to_ctkimage(thumbnail), command=lambda: self.switch_to_theme_screen(theme_data))
            theme_thumbnail.configure(fg_color='transparent', corner_radius=0)
            theme_thumbnail.pack(fill="both", expand=True)
            images.append({'obj': theme_thumbnail, 'img': thumbnail, 'frame': theme_frame})

            # Theme name
            theme_label = tk.CTkLabel(theme_frame, text=theme_data.name)
            theme_label.pack()

            col += 1
            if col >= self.max_col:
                col = 0
                row += 1

    def switch_to_theme_screen(self, theme: Theme):
        try:
            for child in self.theme_container.winfo_children():
                child.destroy()
            themescreen = ThemeFrame(theme, parent=self.theme_container, controller=self.controller)
            themescreen.pack(fill="both", expand=True)
            self.controller.show_frame('theme')
        except Exception as e:
            print(f"Error switching to theme screen: {e}")