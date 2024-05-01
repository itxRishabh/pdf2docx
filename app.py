from flask import Flask, render_template, request, send_file
from pdf2docx import Converter
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['OUTPUT_FOLDER'] = 'outputs/'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    if file:
        # Save the uploaded file
        input_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        output_path = os.path.join(app.config['OUTPUT_FOLDER'], file.filename.replace('.pdf', '.docx'))
        file.save(input_path)

        # Convert PDF to DOCX
        cv = Converter(input_path)
        cv.convert(output_path, start=0, end=None)
        cv.close()

        # Provide the file for download
        return send_file(output_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
