File Parser API
This project provides a backend API for uploading, storing, parsing, and retrieving files, with real-time progress tracking for large uploads. It's built using Flask and designed with a clear project structure for maintainability.

Table of Contents
Setup Instructions

API Documentation

1. File Upload API

2. File Upload Progress API

3. Get File Content API

4. List Files API

5. Delete File API

Sample Requests/Responses

Setup Instructions
Follow these steps to get the API running on your local machine.

Prerequisites
Python 3.8+

pip (Python package installer)

Installation
Clone the Repository (if not already done):

git clone https://github.com/MrAnmesh/file-parser-api.git
cd file-parser-api

Create and Activate a Virtual Environment:
It's highly recommended to use a virtual environment to manage project dependencies.

For Windows PowerShell:

python -m venv venv
.\venv\Scripts\activate

For macOS/Linux or Git Bash:

python3 -m venv venv
source venv/bin/activate

Install Dependencies:
Once the virtual environment is active, install the required Python packages:

pip install -r requirements.txt

Run the Flask Application:
Set the Flask environment variables and start the application:

flask run

The API will typically run on http://127.0.0.1:5000.

API Documentation
The API endpoints are prefixed with /files.

1. File Upload API
Endpoint: POST /files

Method: POST

Payload: multipart/form-data containing the file in a field named file.

Behavior:

Saves the uploaded file metadata and content (stores file path).

Assigns a unique file ID.

Supports large file uploads with asynchronous processing.

Sets initial status to uploading.

Response:

202 Accepted if upload initiated successfully.

2. File Upload Progress API
Endpoint: GET /files/{file_id}/progress

Method: GET

Path Parameter: file_id (UUID of the uploaded file)

Behavior:

Returns the current percentage of upload/processing progress.

Once file parsing is complete, returns status: "ready" and progress: 100.

Response:

200 OK with file progress.

404 Not Found if file_id does not exist.

3. Get File Content API
Endpoint: GET /files/{file_id}

Method: GET

Path Parameter: file_id (UUID of the uploaded file)

Behavior:

If file parsing is complete, returns parsed content as JSON.

If still processing, returns a message indicating progress.

Response:

200 OK with parsed content (if status is ready).

202 Accepted with a message if processing is still in progress.

404 Not Found if file_id does not exist.

4. List Files API
Endpoint: GET /files

Method: GET

Behavior: Returns a list of all uploaded files with their metadata.

Response:

200 OK with a JSON array of file metadata (id, filename, status, created_at).

5. Delete File API
Endpoint: DELETE /files/{file_id}

Method: DELETE

Path Parameter: file_id (UUID of the uploaded file)

Behavior: Removes the uploaded file and its parsed content from storage.

Response:

200 OK with a success message.

404 Not Found if file_id does not exist.

Sample Requests/Responses
These examples use curl for making API requests. Replace http://127.0.0.1:5000 with your API's base URL if it's different.

Assume you have a sample text file named my_document.txt in your current directory.

1. File Upload
Request:

curl -X POST -F "file=@./my_document.txt" http://127.0.0.1:5000/files

Example Response (202 Accepted):

{
  "file_id": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
  "filename": "my_document.txt",
  "message": "File upload initiated and processing started.",
  "status": "uploading"
}

Note: Save the file_id from the response; you'll need it for subsequent requests.

2. Get File Progress
Request:

curl http://127.0.0.1:5000/files/a1b2c3d4-e5f6-7890-1234-567890abcdef/progress

Example Response (during processing - 200 OK):

{
  "file_id": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
  "progress": 50,
  "status": "processing"
}

Example Response (after completion - 200 OK):

{
  "file_id": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
  "progress": 100,
  "status": "ready"
}

3. Get File Content
Request:

curl http://127.0.0.1:5000/files/a1b2c3d4-e5f6-7890-1234-567890abcdef

Example Response (if still processing - 202 Accepted):

{
  "message": "File upload or processing in progress. Please try again later.",
  "progress": 70,
  "status": "processing"
}

Example Response (if ready - 200 OK):

{
  "content": [
    {
      "line_number": 1,
      "text": "This is the first line."
    },
    {
      "line_number": 2,
      "text": "Second line of the document."
    },
    {
      "line_number": 3,
      "text": "And the final line here."
    }
  ],
  "file_id": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
  "status": "ready"
}

4. List Files
Request:

curl http://127.0.0.1:5000/files

Example Response (200 OK):

[
  {
    "created_at": "2024-07-20 10:30:45",
    "filename": "my_document.txt",
    "id": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
    "progress": 100,
    "status": "ready"
  },
  {
    "created_at": "2024-07-20 10:35:10",
    "filename": "another_file.log",
    "id": "b8c9d0e1-f2a3-4567-8901-23456789abcd",
    "progress": 100,
    "status": "ready"
  }
]

5. Delete File
Request:

curl -X DELETE http://127.0.0.1:5000/files/a1b2c3d4-e5f6-7890-1234-567890abcdef

Example Response (200 OK):

{
  "message": "File with ID a1b2c3d4-e5f6-7890-1234-567890abcdef deleted successfully."
}
