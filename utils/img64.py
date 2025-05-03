def read_image_base64(image_path):
    try:
        img = Image.open(image_path)
        img.thumbnail((1024, 1024))  # Resize for faster processing
        buffered = io.BytesIO()
        img.save(buffered, format="JPEG")
        return base64.b64encode(buffered.getvalue()).decode("utf-8")
    except Exception as e:
        raise ValueError(f"Failed to read image: {e}")
