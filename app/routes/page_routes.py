import os
from datetime import datetime

from flask import abort, current_app, render_template, send_from_directory
from jinja2 import TemplateNotFound
from loguru import logger

from app.routes import bp
from app.ssp_tools.helpers.toolkitconfig import ToolkitConfig

date = datetime.now().strftime("%Y")


@bp.route("/")
def index():
    config = ToolkitConfig()
    opencontrol = config.opencontrol
    if not opencontrol:
        logger.error("File not found: opencontrol.yaml")
        abort(400, description="Missing required file: opencontrol.yaml")

    content: dict = {
        "date": date,
        "title": "Home",
        "page_title": opencontrol.get("name", "Home"),
        "project": opencontrol,
    }
    return render_template("pages/index.html", **content)


@bp.errorhandler(404)
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


@bp.errorhandler(500)
def internal_error(error):
    message: dict = {
        "date": date,
        "code": 500,
        "title": "Page not found",
        "content": error,
    }
    return render_template("pages/error.html", **message), 500


@bp.route("/favicon.ico")
def favicon():
    return send_from_directory(
        os.path.join(current_app.root_path, "static"),
        "favicon.ico",
        mimetype="image/vnd.microsoft.icon",
    )
