import requests
from PySide6.QtGui import QPixmap

def get_pixmap(url):
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Check for HTTP errors
        image_data = response.content
        pixmap = QPixmap()
        if pixmap.loadFromData(image_data):
            return pixmap
        else:
            print("Failed to load image from data.")
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch image: {e}")