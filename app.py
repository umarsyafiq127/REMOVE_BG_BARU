from flask import Flask, render_template, request, send_file, jsonify
import requests
import io
from tools.remove import remove_background

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("upload.html")

@app.route("/remove-bg", methods=["POST"])
def remove_bg():
    file = request.files["image"]
    output_image = remove_background(file.read())
    return send_file(io.BytesIO(output_image), mimetype="image/png")

@app.route("/ocr", methods=["POST"])
def ocr():
    file = request.files["image"]
    files = {"image": (file.filename, file.stream, file.mimetype)}

    ocr_server_url = "http://localhost:5001/ocr"
    response = requests.post(ocr_server_url, files=files)
    
    if response.status_code == 200:
        text = response.json().get("text", "Tidak ada teks yang ditemukan.")
    else:
        text = "Terjadi kesalahan saat memproses OCR."

    return render_template("ocr.html", text=text)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
