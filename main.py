import customtkinter as tk
import requests
import time

from typing import Optional, Tuple

from zen_explorer_core.models.theme import Theme
from cli import repository
from PIL import Image
from io import BytesIO

repo = repository.data

images = []
allow_resize_on = time.time()
resize_delay = 0.05

# Root
tk.set_appearance_mode("System")


# Main content
# main_content = tk.CTkFrame(root)
# main_content.pack(side="right", fill="both", expand=True)
# max_col = 3

class MainContent(tk.CTkFrame):
    def __init__(self, parent, controller, theme_container, max_col=3):
        super().__init__(parent)
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
    
        thumbnail = get_image('https://raw.githubusercontent.com/greeeen-dev/natsumi-browser/refs/heads/main/images/home.png')
    
        for theme in repo.themes:
            theme_data = repo.get_theme(theme)
    
            # Main frame
            theme_frame = tk.CTkFrame(self)
            theme_frame.configure(fg_color='transparent', corner_radius=0)
            theme_frame.grid(row=row, column=col, padx=10, pady=10, sticky="ew")
    
            # Thumbnail (PLEASE LET THIS FUCKING WORK) :)
            theme_thumbnail = tk.CTkButton(theme_frame, text="", image=to_ctkimage(thumbnail), command=lambda: self.switch_to_theme_screen(theme_data))
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

class ThemeFrame(tk.CTkFrame):
    def __init__(self, theme: Theme, parent, controller: tk.CTk):
        super().__init__(parent)
        self.name = theme.name
        self.author = theme.author
        self.description = theme.description
        self.thumbnail = get_image('https://raw.githubusercontent.com/greeeen-dev/natsumi-browser/refs/heads/main/images/home.png') # in the future theme.thumbnail 
        # self.pack(fill="both", expand=True)
        self.grid(row=0, column=0, sticky="nsew")
        self.create_widgets()

    def create_widgets(self):
        # Create widgets for the theme frame
        tk.CTkLabel(self, text=self.name).pack()
        tk.CTkLabel(self, text=self.author).pack()
        tk.CTkLabel(self, text=self.description).pack()
        tk.CTkLabel(self, image=to_ctkimage(self.thumbnail)).pack()

def get_image(url):
    response = requests.get(url)
    img_data = response.content

    # Open image
    img = Image.open(BytesIO(img_data))

    # Set a maximum height
    max_height = 150
    # Calculate the new width maintaining the aspect ratio
    aspect_ratio = img.width / img.height
    new_height = max_height
    new_width = int(aspect_ratio * new_height)

    # Resize image
    resized = img.resize((new_width, new_height))
    return resized

def to_ctkimage(image, size=None):
    # Convert PIL image to CTkImage
    return tk.CTkImage(image, size=size or (image.width, image.height))


class ThemesApp(tk.CTk):
    def __init__(self, fg_color: Optional[str | Tuple[str, str]] = None, **kwargs):
        super().__init__(fg_color, **kwargs)
        # This will be our main container where we switch frames yes this is vibe coded cause I don't know my way around Tkinter
        container = tk.CTkFrame(self, width=800, height=600)
        container.pack(side="top", fill="both", expand=True)
    
        # Make this container fill all available space
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
    
        # container2 will hold the sidebar and MainContent
        container2 = tk.CTkFrame(container)
        # Place container2 in row=0,column=0, but it’s on the same “layer” as container3
        container2.grid(row=0, column=0, sticky="nsew")
    
        # container3 will hold your ThemeFrame
        container3 = tk.CTkFrame(container)
        container3.grid(row=0, column=0, sticky="nsew")
    
        # Sidebar in container2. Notice we can pack the sidebar here
        sidebar = tk.CTkFrame(container2, width=200)
        sidebar.pack(side="left", fill="y")
        
        self.frames = {}
        main_content = MainContent(parent=container2, controller=self, theme_container=container3)
        main_content.pack(side="right", fill="both", expand=True)
        main_content.update_main()
        self.frames['main'] = container2
        self.frames['theme'] = container3

        # put all of the pages in the same location;
        # the one on the top of the stacking order
        # will be the one that is visible.
        # frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame('main')
        
    def update_images(self, _):
        global allow_resize_on
    
        if time.time() < allow_resize_on:
            return
    
        allow_resize_on = time.time() + resize_delay
    
        for item in images:
            widget = item['obj']
            image = item['img']
            parent = item['frame']
    
            if type(widget) is not tk.CTkLabel:
                continue
    
            new_width = parent.winfo_width()
            aspect_ratio = image.width / image.height
            new_height = int(new_width / aspect_ratio)
    
            widget.configure(image=to_ctkimage(image, size=(new_width, new_height)))
    
    
    def show_frame(self, frame_name):  # Thank you that one dude on stackoverflow https://stackoverflow.com/questions/7546050/switch-between-two-frames-in-tkinter <3
        '''Show a frame for the given page name'''
        print(f'Showing frame: {frame_name}')
        frame = self.frames[frame_name]
        frame.tkraise()
        

root = ThemesApp()
root.geometry("800x600")
root.update()
root.mainloop()
