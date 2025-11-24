from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = "auth.login"


def create_app():
    app = Flask(
        __name__,
        template_folder="../templates",
        static_folder="../static",
    )
    app.config.from_mapping(
        SECRET_KEY="dev-insecure-change-me",
        SQLALCHEMY_DATABASE_URI="sqlite:///learnc.db",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    db.init_app(app)
    login_manager.init_app(app)

    from . import models  # noqa: F401  (ensure models register with SQLAlchemy)

    from .routes import auth_bp, main_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)

    @app.cli.command("init-db")
    def init_db_command():
        """Create database tables."""
        with app.app_context():
            db.create_all()
        print("Initialized the database.")

    return app

