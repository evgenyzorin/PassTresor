from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from cryptography.fernet import Fernet
from app.config import Config


db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = "users.signin"
login_manager.login_message_category = "danger"
fernet = Fernet(Config.FERNET_KEY.encode("utf-8"))


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    from app.main.routes import main
    from app.users.routes import users
    from app.entries.routes import entries
    from app.errors.handlers import errors

    app.register_blueprint(main)
    app.register_blueprint(users)
    app.register_blueprint(entries)
    app.register_blueprint(errors)

    return app
