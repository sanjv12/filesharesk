from flask import Flask, render_template, request, jsonify, send_file, make_response
import os
import uuid

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Dictionary to keep track of uploaded files and their original names
uploaded_files = {}
def get_file_mimetype(file_path):
    """Determine the exact file type based on file content."""
    mime = magic.Magic()
    return mime.from_file(file_path)
def is_valid_key(key):
    """Check if the given key is valid."""
    return key in uploaded_files

def download_file(key):
    """Download the file associated with the given key."""
    if is_valid_key(key):
        file_info = uploaded_files[key]
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file_info['stored_filename'])
        
        if os.path.exists(file_path):
            # Set the Content-Type header based on the file's extension
            response = make_response(send_file(
                file_path,
                as_attachment=True,
                mimetype=file_info['file_mimetype']
            ))
            
            # Set Content-Disposition header with the original filename
            response.headers["Content-Disposition"] = f"attachment; filename={file_info['original_filename']}"
            
            return response

    return jsonify({'success': False, 'message': 'File not found'})

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    key = request.form['key']
    if key in uploaded_files:
        return jsonify({'success': False, 'message': 'Key already exists. Choose a different key.'})

    file = request.files['file']

    if file:
        original_filename, file_extension = os.path.splitext(file.filename)
        stored_filename = str(uuid.uuid4()) + file_extension
        file_mimetype = file.mimetype
        uploaded_files[key] = {'original_filename': original_filename, 'stored_filename': stored_filename,'extension':file_extension,'file_mimetype': file_mimetype}
        print(uploaded_files[key])
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], stored_filename))
        return jsonify({'success': True, 'key': key})
    
    return jsonify({'success': False, 'message': 'No file provided'})

@app.route('/check_key/<key>')
def check_key(key):
    """Check if the given key is valid."""
    return jsonify({'valid': is_valid_key(key)})

@app.route('/download/<key>')
def download(key):
    """Download the file associated with the given key if it's valid."""
    return download_file(key)

if __name__ == '__main__':
    app.run(debug=True)
