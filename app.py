from flask import Flask, request, jsonify
from PIL import Image
import pytesseract
import io

app = Flask(__name__)

@app.route('/')
def home():
    return '✔️ Tesseract OCR API is running.'

@app.route('/ocr', methods=['POST'])
def ocr():
    if 'image' not in request.files:
        return jsonify({"success": False, "error": "Missing image"}), 400

    image = Image.open(request.files['image'].stream)

    oem = request.args.get("oem", "1")
    psm = request.args.get("psm", "6")
    lang = request.args.get("lang", "eng")
    config = f'--oem {oem} --psm {psm}'

    try:
        text = pytesseract.image_to_string(image, lang=lang, config=config)
        return jsonify({"success": True, "text": text})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})
