# app.py

from flask import Flask, render_template, request, send_from_directory
import os
from cartoonify import cartoonify_video

UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'static'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'video' not in request.files:
        return 'No video uploaded', 400
    file = request.files['video']
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    outputpath = os.path.join(app.config['OUTPUT_FOLDER'], 'cartoon_output.avi')

    file.save(filepath)
    cartoonify_video(filepath, outputpath)

    return render_template('index.html', processed=True, filename='cartoon_output.avi')

@app.route('/download/<filename>')
def download(filename):
    return send_from_directory(app.config['OUTPUT_FOLDER'], filename, as_attachment=True)

if __name__ == '__main__':
    os.makedirs('uploads', exist_ok=True)
    os.makedirs('static', exist_ok=True)
    app.run(debug=True)
