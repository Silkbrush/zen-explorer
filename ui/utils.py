import requests
from PIL import Image
from io import BytesIO
import customtkinter as tk

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
    if size is not None:
        print("Resizing image...")
        resized_image = image.resize(size)
        return tk.CTkImage(resized_image, size=size)
    return tk.CTkImage(image, size=(image.width, image.height))