"""
Copyright 2019-2025 CivicActions, Inc. See the README file at the top-level
directory of this distribution and at https://github.com/CivicActions/ssp-flask#license.
"""

from pathlib import Path

from flask import abort, render_template
from loguru import logger

from app.helpers.helpers import (
    create_breadcrumbs,
    file_to_html,
    get_ssp_root,
    list_directories,
    list_files,
)
from app.routes.routes import bp
from app.ssp_tools.helpers.toolkitconfig import ToolkitConfig


@bp.route("/")
def index():
    config = ToolkitConfig()
    opencontrol = config.opencontrol
    if not opencontrol:
        logger.error("File not found: opencontrol.yaml")
        abort(400, description="Missing required file: opencontrol.yaml")

    content: dict = {
        "title": "Home",
        "page_title": opencontrol.get("name", "Home"),
        "project": opencontrol,
    }
    return render_template("pages/index.html", **content)


@bp.route("/docs/", defaults={"subpath": ""}, methods=["GET"])
@bp.route("/docs/<path:subpath>")
def page_docs_view(subpath: str):
    ssp_base = get_ssp_root()
    file_path = ssp_base.joinpath(subpath)
    breadcrumbs = create_breadcrumbs(
        Path(subpath), route="routes.page_docs_view", exclude_level=["rendered"]
    )
    if file_path.is_dir():
        directory_list = list_directories(path=file_path)
        file_list = list_files(path=file_path)
        directory: dict = {
            "title": file_path.name.capitalize(),
            "page_title": file_path.name.capitalize(),
            "directories": directory_list,
            "files": file_list,
            "breadcrumbs": breadcrumbs,
        }
        return render_template("pages/docs_file_list.html", **directory)

    file_contents = file_to_html(file_path)
    files: dict = {
        "title": "File Viewer",
        "page_title": file_path.name,
        "content": file_contents,
        "file_path": subpath,
        "breadcrumbs": breadcrumbs,
    }
    return render_template("pages/file_viewer.html", **files)


@bp.route("/docx/", defaults={"subpath": ""}, methods=["GET"])
@bp.route("/docx/<path:subpath>")
def page_docx_view(subpath: str):
    ssp_base = get_ssp_root()
    file_path = ssp_base.joinpath(subpath)
    breadcrumbs = create_breadcrumbs(
        Path(subpath), route="routes.page_docx_view", exclude_level=["rendered"]
    )

    directory_list = list_directories(path=file_path)
    file_list = list_files(path=file_path)
    directory: dict = {
        "title": file_path.name.capitalize(),
        "page_title": file_path.name.capitalize(),
        "directories": directory_list,
        "files": file_list,
        "breadcrumbs": breadcrumbs,
    }
    return render_template("pages/docx_file_list.html", **directory)
