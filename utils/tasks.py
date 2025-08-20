# utils/tasks.py
import time
from models.file_model import files_db, parsed_content_db

def parse_file_async(file_id, file_path, filename):
    """Simulates asynchronous file parsing and updates progress."""
    print(f"Starting parsing for file_id: {file_id}")

    # Simulate parsing progress
    total_steps = 10
    for i in range(1, total_steps + 1):
        time.sleep(0.5) # Simulate work
        progress = int((i / total_steps) * 100)
        files_db[file_id]['progress'] = progress
        print(f"File {file_id} progress: {progress}%")

    try:
        # Simple parsing: read content of the file
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            # Store each line as an item in a list for demonstration
            parsed_content = [{"line_number": i + 1, "text": line.strip()} for i, line in enumerate(lines)]

        parsed_content_db[file_id] = parsed_content
        files_db[file_id]['status'] = 'ready'
        files_db[file_id]['progress'] = 100
        print(f"Parsing complete for file_id: {file_id}")
    except Exception as e:
        files_db[file_id]['status'] = 'failed'
        files_db[file_id]['progress'] = 0
        print(f"Parsing failed for file_id: {file_id}. Error: {e}")