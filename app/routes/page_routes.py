"""
Copyright 2019-2025 CivicActions, Inc. See the README file at the top-level
directory of this distribution and at https://github.com/CivicActions/ssp-flask#license.
"""

import os
from datetime import datetime

from flask import abort, render_template
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
