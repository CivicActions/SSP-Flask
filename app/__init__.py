import os
from datetime import datetime

from flask import Flask, abort, current_app, render_template, send_from_directory
from jinja2 import TemplateNotFound
from loguru import logger

from app.config import DevelopmentConfig, TestingConfig
from app.helpers.helpers import get_project_root
from app.routes import bp

app_path = get_project_root()

date = datetime.now().strftime("%Y")

logs_dir = app_path.joinpath("logs")
if not logs_dir.exists():
    logs_dir.mkdir()

logger.remove()

logger.add(
    logs_dir.joinpath("app.log"),
    rotation="10 MB",
    retention="1 week",
    compression="zip",
    level="DEBUG",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
)

logger.add(
    logs_dir.joinpath("error.log"),
    rotation="10 MB",
    retention="1 week",
    level="ERROR",
    backtrace=True,
    diagnose=True,
)

logger.add(
    logs_dir.joinpath("app.log"), rotation="100 MB", retention="10 days", level="DEBUG"
)


def create_app(config_name=None):
    app = Flask(__name__, instance_relative_config=False)

    if config_name is None:
        config_name = os.environ.get("FLASK_CONFIG", "development")

    config_map = {"development": DevelopmentConfig, "testing": TestingConfig}

    app.config.from_object(config_map.get(config_name, DevelopmentConfig))

    app.register_blueprint(bp)

    @app.errorhandler(404)
    def page_not_found(error):
        message: dict = {
            "date": date,
            "code": 404,
            "title": "Page not found",
            "content": error,
        }
        try:
            return render_template("pages/error.html", **message), 404
        except TemplateNotFound:
            abort(404)

    @app.errorhandler(500)
    def internal_error(error):
        message: dict = {
            "date": date,
            "code": 500,
            "title": "Page not found",
            "content": error,
        }
        return render_template("pages/error.html", **message), 500

    @app.route("/favicon.ico")
    def favicon():
        return send_from_directory(
            os.path.join(current_app.root_path, "static"),
            "favicon.ico",
            mimetype="image/vnd.microsoft.icon",
        )

    return app
