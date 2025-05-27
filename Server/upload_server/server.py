from flask import Flask, request, send_from_directory, jsonify
from flask_cors import CORS
import os
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app = Flask(__name__)
CORS(app)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"success": False, "error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"success": False, "error": "No selected file"}), 400

    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)

    # Generate URL for download page (not direct file)
    download_page_url = f"{request.host_url}download/{filename}"
    return jsonify({"success": True, "downloadUrl": download_page_url})

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    # Send file as attachment to force download on client
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

@app.route('/download/<filename>')
def download_page(filename):
    # URL for the actual file to be downloaded
    file_url = f"{request.host_url}uploads/{filename}"
    return f'''
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="UTF-8" />
      <title>Download Your Video</title>
      <style>
        body {{ font-family: Arial, sans-serif; text-align: center; margin: 40px; }}
        button {{
          padding: 12px 24px;
          font-size: 18px;
          cursor: pointer;
          background-color: #4CAF50;
          color: white;
          border: none;
          border-radius: 6px;
          margin-top: 20px;
        }}
        video {{
          max-width: 90vw;
          max-height: 50vh;
          border: 1px solid #ccc;
          margin-top: 20px;
        }}
      </style>
    </head>
    <body>
      <h1>Your Video is Ready</h1>
      <video controls>
        <source src="{file_url}" type="video/mp4">
        Your browser does not support the video tag.
      </video>
      <br/>
      <a href="{file_url}" download>
        <button>Download Video</button>
      </a>
    </body>
    </html>
    '''

if __name__ == '__main__':
    print("Starting server on http://localhost:8000")
    app.run(host='0.0.0.0', port=8000)
