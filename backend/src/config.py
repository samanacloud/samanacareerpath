# config.py
import os


class Settings:
    # Project Info
    PROJECT_NAME = os.getenv('PROJECT_NAME', 'Samana_CareerPath2.0')
    PROJECT_CODENAME = os.getenv('PROJECT_CODENAME', 'scp')
    PROJECT_VERSION = os.getenv('PROJECT_VERSION', '2.0.0.1')
    PROJECT_URL = os.getenv('PROJECT_URL', 'scp.samana.cloud')
    PROJECT_EMAIL = os.getenv('PROJECT_EMAIL', 'careerpath@samanagroup.com')

    # Ports
    BACKEND_PORT = int(os.getenv('BACKEND_PORT', 8000))
    FRONTEND_PORT = int(os.getenv('FRONTEND_PORT', 5173))
    MONGO_PORT = int(os.getenv('MONGO_PORT', 27017))

    # MongoDB Configuration
    MONGO_HOST = os.getenv('MONGO_HOST', 'mongodb')
    MONGO_INITDB_ROOT_USERNAME = os.getenv('MONGO_INITDB_ROOT_USERNAME')
    MONGO_INITDB_ROOT_PASSWORD = os.getenv('MONGO_INITDB_ROOT_PASSWORD')
    MONGO_INITDB_DATABASE = os.getenv('MONGO_INITDB_DATABASE')
    MONGO_USER = os.getenv('MONGO_USER')
    MONGO_PASSWORD = os.getenv('MONGO_PASSWORD')

    # JWT Settings
    JWT_SECRET = os.getenv('JWT_SECRET')

    # Direct MongoDB URL if provided
    MONGODB_URL = os.getenv('MONGODB_URL')

    # Google settings
    GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
    GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')
    GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
    GOOGLE_LOGIN_EMAIL = os.getenv('GOOGLE_LOGIN_EMAIL')

    # Email settings
    EMAIL_APP_PASSWORD = os.getenv('EMAIL_APP_PASSWORD')

    # Google Service Account for Sheets
    GOOGLE_SHEET_SERVICE_ACCOUNT_SHEETS = os.getenv('GOOGLE_SHEET_SERVICE_ACCOUNT_SHEETS')

    @property
    def get_mongodb_url(self):
        """Generate MongoDB connection URL if not directly provided"""
        if self.MONGODB_URL:
            return self.MONGODB_URL
        return f"mongodb://{self.MONGO_USER}:{self.MONGO_PASSWORD}@{self.MONGO_HOST}:{self.MONGO_PORT}/{self.MONGO_INITDB_DATABASE}?authSource={self.MONGO_INITDB_DATABASE}"

    class Config:
        env_file = ".env"

settings = Settings()