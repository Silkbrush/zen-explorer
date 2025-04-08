import customtkinter as tk
import requests
import time
import sys
from cli import repository
from zen_explorer_core.repository import update_repository
from PIL import Image
from io import BytesIO
# Ensure repository is updated/cloned before accessing data
try:
    update_repository()
except Exception as e:
    print(f"Failed to update repository: {e}", file=sys.stderr)
    # Optionally exit if repository is essential
    # sys.exit(1) 

repo = repository.data

# Check if repo is still None after update attempt (e.g., git failed)
if repo is None:
    print("Repository data could not be loaded. Exiting.", file=sys.stderr)
    sys.exit(1)

images = []
allow_resize_on = time.time()
resize_delay = 0.05

# Root
root = tk.CTk()
root.geometry("800x600")

# Sidebar
sidebar = tk.CTkFrame(root, width=200)
sidebar.configure(fg_color="#dddddd", corner_radius=0)
sidebar.pack_propagate(False)
sidebar.pack(side="left", fill="y")

# Main content
main_content = tk.CTkFrame(root)
main_content.configure(fg_color="white")
main_content.pack(side="right", fill="both", expand=True)
max_col = 3

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

def update_main():
    # Reset main content
    global allow_resize_on
    for child in main_content.winfo_children():
        child.destroy()
    images = []
    allow_resize_on = time.time()

    row = 0
    col = 0

    thumbnail = get_image('https://raw.githubusercontent.com/greeeen-dev/natsumi-browser/refs/heads/main/images/home.png')

    for theme in repo.themes:
        theme_data = repo.get_theme(theme)

        # Main frame
        theme_frame = tk.CTkFrame(main_content)
        theme_frame.configure(fg_color='transparent', corner_radius=0)
        theme_frame.grid(row=row, column=col, padx=10, pady=10, sticky="ew")

        # Thumbnail (PLEASE LET THIS FUCKING WORK)
        theme_thumbnail = tk.CTkLabel(theme_frame, text="", image=to_ctkimage(thumbnail))
        theme_thumbnail.pack(fill="both", expand=True)
        images.append({'obj': theme_thumbnail, 'img': thumbnail, 'frame': theme_frame})

        # Theme name
        theme_label = tk.CTkLabel(theme_frame, text=theme_data.name)
        theme_label.pack()

        col += 1
        if col >= max_col:
            col = 0
            row += 1

def update_images(_):
    global allow_resize_on

    if time.time() < allow_resize_on:
        return

    allow_resize_on = time.time() + resize_delay

    for item in images:
        widget = item['obj']
        image = item['img']
        parent = item['frame']

        if not type(widget) is tk.CTkLabel:
            continue

        new_width = parent.winfo_width()
        aspect_ratio = image.width / image.height
        new_height = int(new_width / aspect_ratio)

        widget.configure(image=to_ctkimage(image, size=(new_width, new_height)))


update_main()

for col in range(max_col):
    main_content.grid_columnconfigure(col, weight=1, uniform="column")

root.update()
root.bind("<Configure>", update_images)
root.mainloop()
