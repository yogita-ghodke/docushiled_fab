from flask import Flask,render_template ,request
import os
import pdfplumber
import re

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['pdf']
    if file:
        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)

        aadhaar_pattern = r'\b\d{4}[\s-]?\d{4}[\s-]?\d{4}\b'
        email_pattern = r'\b[\w\.-]+@[\w\.-]+\.\w{2,4}\b'

        full_text = ""
        with pdfplumber.open(filepath) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    full_text += text + "\n"

        aadhaar = re.findall(aadhaar_pattern, full_text)
        emails = re.findall(email_pattern, full_text)

        return render_template('index.html', aadhaar=aadhaar, emails=emails)

    return "No file uploaded"

if __name__ == '__main__':
    app.run(debug=True)