# api/routes.py
import os
import uuid
import threading
import time
from flask import Blueprint, request, jsonify, current_app
from models.file_model import files_db, parsed_content_db
from utils.tasks import parse_file_async

# Create a Blueprint for the API routes
api_bp = Blueprint('api', __name__, url_prefix='/files')

@api_bp.route('/', methods=['POST'])
def upload_file():
    """Endpoint for uploading a file."""
    if 'file' not in request.files:
        return jsonify({"message": "No file part in the request"}), 400

    uploaded_file = request.files['file']
    if uploaded_file.filename == '':
        return jsonify({"message": "No selected file"}), 400

    if uploaded_file:
        file_id = str(uuid.uuid4())
        original_filename = uploaded_file.filename
        file_path = os.path.join(current_app.config['UPLOADS_FOLDER'], file_id + '_' + original_filename)
        uploaded_file.save(file_path)

        # Store file metadata in the simulated database
        files_db[file_id] = {
            "id": file_id,
            "filename": original_filename,
            "status": "uploading",
            "progress": 0,
            "created_at": time.strftime("%Y-%m-%d %H:%M:%S"),
            "file_path": file_path
        }

        # Start asynchronous parsing in a new thread
        # For production, consider using a proper task queue like Celery
        threading.Thread(target=parse_file_async, args=(file_id, file_path, original_filename)).start()

        return jsonify({
            "file_id": file_id,
            "filename": original_filename,
            "status": "uploading",
            "message": "File upload initiated and processing started."
        }), 202

@api_bp.route('/<string:file_id>/progress', methods=['GET'])
def get_file_progress(file_id):
    """Endpoint to get the current progress of a file upload/processing."""
    file_info = files_db.get(file_id)
    if not file_info:
        return jsonify({"message": "File not found"}), 404
    return jsonify({
        "file_id": file_info['id'],
        "status": file_info['status'],
        "progress": file_info['progress']
    })

@api_bp.route('/<string:file_id>', methods=['GET'])
def get_file_content(file_id):
    """Endpoint to retrieve the parsed content of a file."""
    file_info = files_db.get(file_id)
    if not file_info:
        return jsonify({"message": "File not found"}), 404
    
    if file_info['status'] == 'ready':
        parsed_content = parsed_content_db.get(file_id)
        return jsonify({
            "file_id": file_id,
            "status": "ready",
            "content": parsed_content
        })
    else:
        return jsonify({
            "message": "File upload or processing in progress. Please try again later.",
            "status": file_info['status'],
            "progress": file_info['progress']
        }), 202

@api_bp.route('/', methods=['GET'])
def list_files():
    """Endpoint to list all uploaded files with their metadata."""
    all_files_metadata = []
    for file_id, info in files_db.items():
        display_info = info.copy()
        display_info.pop('file_path', None) # Remove internal path before sending to client
        all_files_metadata.append(display_info)
    return jsonify(all_files_metadata)

@api_bp.route('/<string:file_id>', methods=['DELETE'])
def delete_file(file_id):
    """Endpoint to delete an uploaded file and its parsed content."""
    file_info = files_db.get(file_id)
    if not file_info:
        return jsonify({"message": "File not found"}), 404

    # Remove from simulated databases
    files_db.pop(file_id, None)
    parsed_content_db.pop(file_id, None)
    
    # Delete the physical file from the server
    file_path = file_info.get('file_path')
    if file_path and os.path.exists(file_path):
        os.remove(file_path)

    return jsonify({"message": f"File with ID {file_id} deleted successfully."})