import base64
from pathlib import Path

def encode_image_to_base64(image_path):
    """
    Reads the image from image_path and returns base64-encoded string.
    """
    image_path = Path(image_path)
    with open(image_path, "rb") as img_file:
        encoded_string = base64.b64encode(img_file.read()).decode()
    return encoded_string

def generate_image_html(image_path, width=400, style=None):
    """
    Returns an HTML <img> tag string with base64 encoded image embedded.
    """
    encoded = encode_image_to_base64(image_path)
    style_attr = f'style="{style}"' if style else ""
    html = f'<img src="data:image/png;base64,{encoded}" width="{width}" {style_attr} />'
    return html

def show_logo(image_path, width=400, style=None, align_center=True):
    """
    Returns a complete HTML block with optional centering div and image.
    """
    img_html = generate_image_html(image_path, width, style)
    if align_center:
        return f'<div style="text-align: center;">{img_html}</div>'
    return img_html
