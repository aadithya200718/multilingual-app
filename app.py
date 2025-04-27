
from flask import Flask, request, jsonify
import os
from model_utils import process_audio_file
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all domains
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file:
        print(f"Received file: {file.filename}")
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        transcript = process_audio_file(filepath)
        return jsonify({'transcript': transcript})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
