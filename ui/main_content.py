import customtkinter as tk
from customtkinter.windows.widgets.image.ctk_image import CTkImage
from zen_explorer_core.repository import RepositoryData
from zen_explorer_core.models.theme import Theme
from ui import utils
from .theme_frame import ThemeFrame
import time

RESIZE_DELAY = 0.4

class MainContent(tk.CTkScrollableFrame):
    def __init__(self, parent, controller, theme_container, repo: RepositoryData, max_col=3):
        super().__init__(parent)
        self.repo = repo
        self.theme_container = theme_container
        self.controller = controller
        self.parent = parent
        self.max_col = max_col
        self.allow_resize_on = time.time()
        for col in range(max_col):
            self.grid_columnconfigure(col, weight=1, uniform="column")

    def update_main(self):
        # Reset main content
        global allow_resize_on
        for child in self.winfo_children():
            child.destroy()
        self.images = []
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
            theme_thumbnail = tk.CTkButton(theme_frame, text="", image=utils.to_ctkimage(thumbnail), command=lambda theme_data=theme_data: self.switch_to_theme_screen(theme_data))
            theme_thumbnail.configure(fg_color='transparent', corner_radius=0)
            theme_thumbnail.pack(fill="both", expand=True)
            self.images.append({'obj': theme_thumbnail, 'img': thumbnail, 'frame': theme_frame})

            # Theme name
            theme_label = tk.CTkLabel(theme_frame, text=theme_data.name)
            theme_label.pack()

            col += 1
            if col >= self.max_col:
                col = 0
                row += 1

    def switch_to_theme_screen(self, theme: Theme):
        for child in self.theme_container.winfo_children():
            if isinstance(child, ThemeFrame):
                child.destroy()
        themescreen = ThemeFrame(theme, parent=self.theme_container, controller=self.controller)
        themescreen.pack(fill="both", expand=True)
        self.controller.show_frame('theme')
        self.controller.current = theme
        themescreen.add_readme()
        
    def update_images(self, _):
        global allow_resize_on
        
        if time.time() < self.allow_resize_on:
            return
        
        self.allow_resize_on = time.time() + RESIZE_DELAY

        for item in self.images:
            
            widget = item['obj']
            image = item['img']
            parent = item['frame']
            
            
            # if type(widget) is not tk.CTkLabel:
            #     continue

            new_width = parent.winfo_width()
            aspect_ratio = image.width / image.height
            new_height = int(new_width / aspect_ratio)
            print(f"Updating image for {item['obj']} in frame {item['frame']} with height {image.height} and new height {new_height}")
            widget.configure(image=utils.to_ctkimage(image, size=(new_width, new_height)))
