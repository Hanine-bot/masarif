from pathlib import Path

from flask import Flask

from .repositories import TransactionRepository
from .routes import main_bp
from .services import AccountingService


BASE_DIR = Path(__file__).resolve().parent.parent


def create_app() -> Flask:
    app = Flask(__name__, template_folder=str(BASE_DIR / "templates"), static_folder=str(BASE_DIR / "static"))
    app.config["SECRET_KEY"] = "accounting-mini-project-secret"
    app.config["DATABASE_PATH"] = BASE_DIR / "data" / "accounting.db"
    app.config["EXPORT_FOLDER"] = BASE_DIR / "exports"

    app.config["DATABASE_PATH"].parent.mkdir(parents=True, exist_ok=True)
    app.config["EXPORT_FOLDER"].mkdir(parents=True, exist_ok=True)

    repository = TransactionRepository(app.config["DATABASE_PATH"])
    repository.init_schema()

    app.extensions["repository"] = repository
    app.extensions["service"] = AccountingService(repository, app.config["EXPORT_FOLDER"])

    app.register_blueprint(main_bp)
    return app
