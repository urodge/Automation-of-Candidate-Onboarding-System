from flask import Flask, render_template, request, redirect, url_for
import os
from extract_data import extract_form_data, insert_data
from ocr import extract_table_data, save_tables
from database import fetch_all_records
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            filename = file.filename
            # create a directory to store the uploaded files
            if not os.path.exists('uploads'):
                os.makedirs('uploads')
            file_path = 'uploads/' + filename
            file.save(file_path)
            # the file extension
            extension = filename.split('.')[-1]
            if extension == 'pdf':
                # extract text from PDF
                extracted_tables = extract_table_data(pdf_path=file_path)
                save_tables(extracted_tables)
                
                form_data = extract_form_data(file_path)
                insert_data(form_data)
            else:
                # unsupported file type
                return "Unsupported file type"
            
            return "Successfully data saved in the database and uploaded file"


if __name__ == '__main__':
    app.run(debug=True)