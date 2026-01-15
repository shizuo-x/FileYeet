import os
import shutil
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/browse', methods=['GET'])
def browse():
    path = request.args.get('path', '/mnt')
    try:
        # Ensure we are browsing within mounted directories or safe zones if needed
        # For this local tool, we'll allow browsing anywhere the container can see
        
        items = []
        if os.path.isdir(path):
            for entry in os.scandir(path):
                if entry.is_dir():
                    items.append({
                        'name': entry.name,
                        'path': entry.path,
                        'type': 'dir'
                    })
        
        # Sort directories alphabetically
        items.sort(key=lambda x: x['name'].lower())
        
        # Add parent directory option if not at root
        parent = os.path.dirname(path)
        if parent and parent != path:
             items.insert(0, {
                'name': '..',
                'path': parent,
                'type': 'dir'
            })

        return jsonify({'current_path': path, 'items': items})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/scan', methods=['POST'])
def scan_and_copy():
    data = request.json
    input_dir = data.get('input_path', '/data/input')
    output_dir = data.get('output_path', '/data/output')
    extension = data.get('extension', 'mp3').lower()
    if not extension.startswith('.'):
        extension = f'.{extension}'

    if not os.path.exists(input_dir):
        return jsonify({'status': 'error', 'message': f'Input directory not found: {input_dir}'}), 400
    
    if not os.path.exists(output_dir):
        try:
            os.makedirs(output_dir)
        except Exception as e:
            return jsonify({'status': 'error', 'message': f'Could not create output directory: {str(e)}'}), 400

    copied_count = 0
    dirs_scanned = 0
    files_found = 0
    errors = []

    try:
        print(f"Scanning directory: {input_dir}")
        for root, dirs, files in os.walk(input_dir):
            dirs_scanned += 1
            for file in files:
                if file.lower().endswith(extension):
                    files_found += 1
                    src_path = os.path.join(root, file)
                    dst_path = os.path.join(output_dir, file)
                    
                    # Handle duplicate filenames
                    if os.path.exists(dst_path):
                        base, ext = os.path.splitext(file)
                        counter = 1
                        while os.path.exists(os.path.join(output_dir, f"{base}_{counter}{ext}")):
                            counter += 1
                        dst_path = os.path.join(output_dir, f"{base}_{counter}{ext}")

                    try:
                        shutil.copy2(src_path, dst_path)
                        copied_count += 1
                    except Exception as e:
                        errors.append(f"Failed to copy {file}: {str(e)}")

    except Exception as e:
        return jsonify({'status': 'error', 'message': f'System error: {str(e)}'}), 500

    return jsonify({
        'status': 'success',
        'message': f'Operation complete. Scanned {dirs_scanned} directories. Found {files_found} files with extension "{extension}". Copied {copied_count} files.',
        'errors': errors
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8336)