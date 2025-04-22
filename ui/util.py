import requests
import os
from PySide6.QtGui import QPixmap

def load_css(directory):
    with open(f"{directory}/style.css", "r") as f:
        _style = f.read()
        if os.path.isfile(f"{directory}/variables.txt"):
            with open(f"{directory}/variables.txt", "r") as f:
                _variables = f.read()
                for line in _variables.splitlines():
                    line = line.replace(' ', '')
                    var = line.split(':')[0].strip()
                    val = line.split(':')[1].strip()
                    _style = _style.replace(f"{var}", val)
        return _style


def get_pixmap_from_url(url):
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