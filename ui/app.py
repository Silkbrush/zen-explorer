import customtkinter as tk
import time

from typing import Optional, Tuple

from ui import MainContent

from ui import utils
from cli import repository

repo = repository.data

images = []
allow_resize_on = time.time()
resize_delay = 0.05


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
        
        bottombar = tk.CTkFrame(container2, height=100)
        bottombar.pack(side="bottom", fill="x")
        
        self.frames = {}
        main_content = MainContent(parent=container2, controller=self, theme_container=container3, repo=repo)
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

            widget.configure(image=utils.to_ctkimage(image, size=(new_width, new_height)))


    def show_frame(self, frame_name):  # Thank you that one dude on stackoverflow https://stackoverflow.com/questions/7546050/switch-between-two-frames-in-tkinter <3
        '''Show a frame for the given page name'''
        print(f'Showing frame: {frame_name}')
        frame = self.frames[frame_name]
        frame.tkraise()