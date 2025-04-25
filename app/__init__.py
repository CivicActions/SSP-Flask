import os
from datetime import datetime

from flask import Flask
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

    return app
