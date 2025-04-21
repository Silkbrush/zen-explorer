import customtkinter as tk
import time

from typing import Optional, Tuple

from ui import MainContent

from ui import utils
from cli import repository
from zen_explorer_core.profiles import get_profile_path, get_profiles
from zen_explorer_core import installer
from zen_explorer_core.models.theme import Theme

repo = repository.data

images = []
allow_resize_on = time.time()
resize_delay = 0.05


class ThemesApp(tk.CTk):
    def __init__(self, fg_color: Optional[str | Tuple[str, str]] = None, **kwargs):
        super().__init__(fg_color, **kwargs)
        print(self._fg_color[0].format(''))
        self.current_profile = None
        self.current: Optional[Theme] = None

        container = tk.CTkFrame(self, fg_color=self._fg_color[1])
        container.pack(side="top", fill="both", expand=True)

        # Make this container fill all available space
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        sidebar = tk.CTkFrame(container, width=200, fg_color=self._fg_color[1])
        sidebar.grid(row=0, column=2, sticky="nse")

        container2 = tk.CTkFrame(container)
        container2.grid(row=0, column=0, sticky="nsew")

        container3 = tk.CTkFrame(container)
        container3.grid(row=0, column=1, sticky="nsew")
        container3.grid_forget()

        bottombar = tk.CTkFrame(container, height=100, fg_color=self._fg_color[1])
        bottombar.grid(row=1, column=0, columnspan=3, sticky="nsew")
        
        self.profiles_display = []
        self.profiles = []
        self.display_profile_to_profile = {}
        print(get_profiles())
        for profile in get_profiles():
            profile_id, profile_name = profile.split('.', 1)
            self.profiles_display.append(f'{profile_name} ({profile_id})')
            self.profiles.append(profile)
            print(profile)
            print(get_profile_path(profile))
            self.display_profile_to_profile[f'{profile_name} ({profile_id})'] = profile
        
        optionmenu = tk.CTkOptionMenu(bottombar, values=self.profiles_display,
                                                 command=self.user_select)
        optionmenu.pack(side="right", padx=10, pady=10)
        optionmenu.place(relx=.98, rely=0.5, anchor="e")
        optionmenu.set("select profile")
        self.install_button = tk.CTkButton(bottombar, text="Install", command=self.install_profile)
        self.install_button.place(relx=.82, rely=0.5, anchor="e")
        self.install_button.pack_forget()
        self.frames = {}
        main_content = MainContent(parent=container2, controller=self, theme_container=container3, repo=repo)
        main_content.pack(side="right", fill="both", expand=True)
        main_content.update_main()
        self.frames['main'] = [container2, lambda: container2.grid(row=0, column=0, sticky="nsew")]
        self.frames['theme'] = [container3, lambda: container3.grid(row=0, column=1, sticky="nsew")]
        self.current_frame = 'main'
        self.show_frame('main')
        self.bind("<Configure>", main_content.update_images)
    
    def install_profile(self):
        zen_theme = self.current

        profile = self.current_profile
    
        if not repository.data or not repository.data.themes:
            print('No themes available.')
            return
    
        # theme_data = repository.data.get_theme(zen_theme)
        # if not theme_data:
        #     print('Theme not found.')
        #     return
    
        print(f'Installing {zen_theme.id} by {zen_theme.author}...')
        try:
            installer.install_theme(profile, zen_theme.id)
        except:
            print('Failed to install theme.')
            raise
        print('Theme installed.')
    
    def show_hide_install_button(self):
        if self.current_frame == 'theme':
            self.install_button.pack(side="right", padx=10, pady=10)
            self.install_button.place(relx=.82, rely=0.5, anchor="e")
        else:
            self.install_button.pack_forget()
            self.install_button.place_forget()

    def user_select(self, choice):
        print("optionmenu dropdown clicked:", choice)
        self.current_profile = self.display_profile_to_profile[choice]




    def show_frame(self, frame_name):  # Thank you that one dude on stackoverflow https://stackoverflow.com/questions/7546050/switch-between-two-frames-in-tkinter <3
        '''Show a frame for the given page name'''
        print(f'Showing frame: {frame_name}')
        old_frame_name = self.current_frame
        old_frame = self.frames[old_frame_name]
        old_frame[0].grid_forget()
        self.current_frame = frame_name
        frame = self.frames[frame_name]
        frame[1]()
        frame[0].tkraise()
        self.show_hide_install_button()
        