from flask import Flask, request, send_file
from PIL import Image
import io
from chromium_daltonize import chromium_daltonize

app = Flask(__name__)

@app.route('/daltonize', methods=['POST'])
def handle_image():
    if 'image' not in request.files:
        return {"error": "No image uploaded"}, 400
    
    dalton_type = request.form.get('type', 'd').lower()
    if dalton_type not in ['p', 'd', 't']:
        return {"error": "Invalid type. Use 'p', 'd', or 't'."}, 400

    try:
        severity = float(request.form.get("severity", "1"))
    except ValueError:
        return {"error": "Severity must be a number from 0 to 1."}, 400
    if not 0 <= severity <= 1:
        return {"error": "Severity must be a number from 0 to 1."}, 400

    image_file = request.files["image"]
    img = Image.open(image_file.stream).convert("RGB")
    dalton_img = chromium_daltonize(img, dalton_type, severity)

    img_io = io.BytesIO()
    dalton_img.save(img_io, 'JPEG')
    img_io.seek(0)

    return send_file(img_io, mimetype='image/jpeg')

if __name__ == '__main__':
    app.run()
