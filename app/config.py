from datetime import timedelta


class Config:
    SECRET_KEY = "2b518e810ee6f1bdcc8edacffcd09277"
    FERNET_KEY = "nQjLLEDZwf_dmoOEEIIs4IVkBD7xXUbkzqkrejchUxA="
    SQLALCHEMY_DATABASE_URI = "sqlite:///site.db"
    SESSION_PROTECTION = "strong"
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=15)
    REMEMBER_COOKIE_DURATION = timedelta(days=7)
