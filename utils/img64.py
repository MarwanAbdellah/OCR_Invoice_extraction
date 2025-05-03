import base64

def read_image_base64(img_path):
    with open(img_path, "rb") as image_data:
        return base64.b64encode(image_data.read()).decode("utf-8")