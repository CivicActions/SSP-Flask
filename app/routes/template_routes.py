"""
Copyright 2019-2025 CivicActions, Inc. See the README file at the top-level
directory of this distribution and at https://github.com/CivicActions/ssp-flask#license.
"""

from flask import render_template

from app.routes import bp
from app.ssp_tools.helpers.toolkitconfig import ToolkitConfig


@bp.route("/templates")
def template_files():
    config = ToolkitConfig()
    content: dict = {
        "title": "Templates",
        "page_title": "Templates",
        "files": config.get_template_files(),
    }
    return render_template("pages/templates.html", **content)
