class BaseConfig:
    SQLALCHEMY_DATABASE_URI = "sqlite:///event_database.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SECRET_KEY = 'your-secret-key-change-in-production'