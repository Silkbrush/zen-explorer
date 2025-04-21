import tkinter as tk
from tkinter import Frame # Keep Frame import if users might pass it as parent
from tkinter.scrolledtext import ScrolledText # Keep if users might use it elsewhere
import markdown
from tkinterweb import HtmlFrame
# Import Pygments for code highlighting CSS
import pygments
from pygments.formatters import HtmlFormatter

# Ensure you have the necessary libraries installed:
# pip install tkinterweb markdown Pygments

# --- Core Functions ---

def convert_markdown_to_html(markdown_text):
    """
    Converts Markdown text to HTML with code highlighting.

    Args:
        markdown_text: The Markdown text to convert.

    Returns:
        The HTML representation of the Markdown text, including CSS for highlighting.
    """
    # Configure markdown extensions for fenced code blocks and code highlighting
    extensions = ['fenced_code', 'codehilite']
    md = markdown.Markdown(extensions=extensions, output_format='html5')

    # Convert the markdown text to an HTML body
    html_body = md.convert(markdown_text)
    with open("logs/html_body.html", "w", encoding="utf-8") as file:
        file.write(html_body)

    # Get CSS styles for code highlighting from Pygments
    formatter = HtmlFormatter(style='default', cssclass='codehilite')
    css_styles = formatter.get_style_defs()
    with open("logs/css_styles.css", "w", encoding="utf-8") as file:
        file.write(css_styles)
    
    # Combine CSS and HTML body into a full HTML document structure
    full_html = f"""
<!DOCTYPE html>
<html>
<head>
<style>
{css_styles}

body {{
  background-color: #00000000;
}}
body {{
    font-family: sans-serif;
    padding: 10px;
    background-color: #00000000 !important; /* Make HTML body background transparent */
    background: transparent;
}}
pre {{
    background-color: #f0f0f0; /* Keep code block background */
    padding: 10px;
    border-radius: 5px;
    overflow-x: auto;
}}
code {{
    font-family: monospace;
}}
img {{
    max-width: 100%;
    height: auto;
    border-radius: 5px;
}}
</style>
</head>
<body>
{html_body}
</body>
</html>
"""
    return full_html

def create_markdown_viewer_frame(parent_widget, markdown_content):
    """
    Creates and configures an HtmlFrame widget to display rendered Markdown.

    Args:
        parent_widget: The Tkinter parent widget for the HtmlFrame.
        markdown_content: The initial Markdown string to display.

    Returns:
        The configured tkinterweb.HtmlFrame instance.
    """
    # Convert the initial markdown to HTML
    initial_html = convert_markdown_to_html(markdown_content)

    # Create the HtmlFrame widget within the parent
    # Note: Setting bg on HtmlFrame itself might not yield true transparency
    # depending on the platform and tkinterweb's implementation.
    # Transparency is handled via the HTML body's background CSS.
    html_frame = HtmlFrame(parent_widget)

    # Load the initial HTML content
    html_frame.load_html(initial_html)

    # Return the created and configured widget
    return html_frame