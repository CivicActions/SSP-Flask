"""
Copyright 2019-2025 CivicActions, Inc. See the README file at the top-level
directory of this distribution and at https://github.com/CivicActions/ssp-flask#license.
"""

from datetime import datetime
from pathlib import Path

from flask import render_template

from app.helpers.helpers import file_to_html
from app.routes import bp
from app.ssp_tools.helpers.toolkitconfig import ToolkitConfig


@bp.route("/rendered", methods=["GET"])
def rendered_files():
    config = ToolkitConfig()
    content: dict = {
        "title": "Rendered Files",
        "page_title": "Rendered Files",
        "files": config.get_rendered_files(),
    }
    return render_template("rendered/rendered_file_list.html", **content)


@bp.route("/rendered/", defaults={"subpath": ""}, methods=["GET"])
@bp.route("/rendered/<path:subpath>")
def rendered_view_file(subpath: str):
    file_path = Path(subpath)
    file_contents = file_to_html(file_path)
    content: dict = {
        "title": "Rendered Files",
        "page_title": file_path.name,
        "content": file_contents,
        "file_path": subpath.replace("rendered", "templates"),
    }
    return render_template("rendered/rendered_file.html", **content)
