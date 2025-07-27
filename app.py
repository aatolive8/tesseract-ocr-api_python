from flask import Flask, request, jsonify
from PIL import Image
import pytesseract

app = Flask(__name__)

@app.route('/')
def index():
    return "Tesseract OCR API is running."

@app.route('/ocr', methods=['POST'])
def ocr_image():
    try:
        if 'image' not in request.files:
            return jsonify({"success": False, "error": "No image uploaded"}), 400

        image_file = request.files['image']
        image = Image.open(image_file.stream)

        # Basic Preprocessing
        image = image.convert("L")  # Grayscale
        image = image.resize((image.width * 2, image.height * 2))

        # Configurable OCR params
        psm = request.args.get("psm", "6")
        oem = request.args.get("oem", "1")
        lang = request.args.get("lang", "eng")

        config = f'--oem {oem} --psm {psm}'
        text = pytesseract.image_to_string(image, lang=lang, config=config)

        return jsonify({"success": True, "text": text.strip()})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
