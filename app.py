from flask import Flask, render_template, request, jsonify, send_file, redirect, url_for
from flask_cors import CORS
import os
import analyzer
import pandas as pd
from werkzeug.utils import secure_filename

app = Flask(__name__, template_folder='.', static_folder='.')
CORS(app)  # Enable CORS for API requests

app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['OUTPUT_FOLDER'] = 'outputs'
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max file size

# Allowed file extensions
ALLOWED_EXTENSIONS = {'csv', 'xlsx', 'xls', 'pdf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Ensure directories exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)

@app.route('/')
def home():
    return send_file('homePage.html')

@app.route('/styles.css')
def styles():
    return send_file('styles.css')

@app.route('/login.html')
def login_page():
    return send_file('login.html')

@app.route('/auth/login/<provider>')
def auth_login(provider):
    # Mock authentication - in real app, this would redirect to OAuth provider
    # For now, we simulate a successful login and redirect home with a user param
    print(f"Simulating login with {provider}")
    provider_name = provider.capitalize()
    return redirect(url_for('home', user=f"{provider_name} User"))

# New API endpoint that handles multiple files
@app.route('/api/analyze', methods=['POST'])
def api_analyze():
    """
    API endpoint to receive multiple files and send them to the backend analyzer.
    Returns analysis results to the frontend.
    """
    if 'files' not in request.files:
        return jsonify({'error': 'No files uploaded'}), 400
    
    files = request.files.getlist('files')
    
    if not files or all(f.filename == '' for f in files):
        return jsonify({'error': 'No files selected'}), 400
    
    context = request.form.get('context', '')
    
    # Save all uploaded files
    saved_files = []
    for file in files:
        if file and file.filename != '':
            if allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                saved_files.append({
                    'filename': filename,
                    'filepath': filepath,
                    'original_name': file.filename
                })
            else:
                return jsonify({'error': f'File type not allowed: {file.filename}'}), 400
    
    if not saved_files:
        return jsonify({'error': 'No valid files to process'}), 400
    
    try:
        # Call the analysis logic with all files
        result = analyzer.process_multiple_files(saved_files, context, app.config['OUTPUT_FOLDER'])
        return jsonify(result)
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

# Keep the old single-file endpoint for backward compatibility
@app.route('/analyze', methods=['POST'])
def analyze():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
        
    context = request.form.get('context', '')
    
    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        try:
            # Call the analysis logic (customizable by user)
            result = analyzer.process_data(filepath, context, app.config['OUTPUT_FOLDER'])
            return jsonify(result)
        except Exception as e:
            return jsonify({'error': str(e)}), 500

@app.route('/download/<filename>')
def download_file(filename):
    return send_file(os.path.join(app.config['OUTPUT_FOLDER'], filename), as_attachment=True)

# Endpoint to preview uploaded files
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_file(os.path.join(app.config['UPLOAD_FOLDER'], filename))

if __name__ == '__main__':
    app.run(debug=True, port=5000)
