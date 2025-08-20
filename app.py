# app.py
import os
from flask import Flask

def create_app():
    """Application factory function to create and configure the Flask app."""
    app = Flask(__name__)

    # Create the 'uploads' directory if it doesn't exist
    app.config['UPLOADS_FOLDER'] = 'uploads'
    os.makedirs(app.config['UPLOADS_FOLDER'], exist_ok=True)
    
    # Import and register the API blueprint
    from api.routes import api_bp
    app.register_blueprint(api_bp)

    return app

# Main entry point to run the application directly
if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)