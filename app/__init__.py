from flask import Flask
from dotenv import load_dotenv
import os

def create_app():
    app = Flask(__name__)
    app.config.from_object("config")
    app.config['MAX_CONTENT_LENGTH'] = 25 * 1024 * 1024  # 25 MB
    
    # Load environment variables from .env
    load_dotenv()

    # Get MongoDB URI from the environment
    MONGO_URI = os.getenv("MONGO_URI")


    # Register blueprints
    from .routes import main
    app.register_blueprint(main)

    # Define and register the format_number filter
    def format_number(value):
        """Format numbers with commas (e.g., 10000 → 10,000)."""
        return "{:,}".format(value)

    app.jinja_env.filters["format_number"] = format_number

    return app