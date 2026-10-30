import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Config:
    # Flask secret key
    SECRET_KEY = os.getenv(
        "SECRET_KEY",
        "govverify-development-secret-key"
    )

    # Database configuration
    SQLALCHEMY_DATABASE_URI = os.getenv(
    "DATABASE_URL",
    "mysql+pymysql://root:@localhost:3306/govverify"
)

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Upload configuration
    UPLOAD_FOLDER = os.path.join(
        os.getcwd(),
        "uploads"
    )

    MAX_CONTENT_LENGTH = 10 * 1024 * 1024  # 10 MB

    # Allowed document extensions
    ALLOWED_EXTENSIONS = {
        "pdf",
        "jpg",
        "jpeg",
        "png"
    }