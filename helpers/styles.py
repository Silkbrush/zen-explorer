from tkinter import ttk

class AppStyles(ttk.Style):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Sidebar
        self.configure(
            'Sidebar.TFrame',
            background="#00000055",
            width=150
        )

        # Sidebar buttons
        self.configure(
            'Sidebar.TButton',
            foreground="white",
            background="#34495E",
            relief="flat",
            activebackground="#1F2C38",
            activeforeground="white",
            border_radius=0
        )
