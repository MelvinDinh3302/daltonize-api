from flask import Flask, request, send_file
from PIL import Image
import numpy as np
import io
from daltonize import daltonize, gamma_correction, array_to_img

app = Flask(__name__)

@app.route('/daltonize', methods=['POST'])
def handle_image():
    if 'image' not in request.files:
        return {"error": "No image uploaded"}, 400
    
    dalton_type = request.form.get('type', 'd').lower()
    if dalton_type not in ['p', 'd', 't']:
        return {"error": "Invalid type. Use 'p', 'd', or 't'."}, 400

    image_file = request.files['image']
    img = Image.open(image_file.stream).convert("RGB")
    img_np = np.asarray(img, dtype=np.float16)
    img_np = gamma_correction(img_np)

    dalton_rgb = daltonize(img_np, dalton_type)
    dalton_img = array_to_img(dalton_rgb)

    img_io = io.BytesIO()
    dalton_img.save(img_io, 'JPEG')
    img_io.seek(0)

    return send_file(img_io, mimetype='image/jpeg')

if __name__ == '__main__':
    app.run()
