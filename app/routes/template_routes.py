"""
Copyright 2019-2025 CivicActions, Inc. See the README file at the top-level
directory of this distribution and at https://github.com/CivicActions/ssp-flask#license.
"""

from pathlib import Path

from flask import abort, flash, redirect, render_template, request, url_for
from loguru import logger
from ruamel.yaml import YAML, YAMLError

from app.helpers.helpers import (
    create_breadcrumbs,
    get_ssp_root,
    list_directories,
    list_files,
)
from app.routes import bp
from app.ssp_tools.helpers.toolkitconfig import ToolkitConfig


@bp.route("/templates")
def template_files():
    config = ToolkitConfig()
    template_path = config.ssp_base.joinpath("templates")
    directory_list = list_directories(path=template_path)
    file_list = list_files(path=template_path)
    templates: dict = {
        "title": "Templates",
        "page_title": "Templates",
        "directories": directory_list,
        "files": file_list,
        "breadcrumbs": create_breadcrumbs(Path("templates"), "routes.template_files"),
    }
    return render_template("templates/template_file_list.html", **templates)


@bp.route("/templates/", defaults={"subpath": ""}, methods=["GET"])
@bp.route("/templates/<path:subpath>")
def template_path_view(subpath: str):
    ssp_base = get_ssp_root()
    file_path = ssp_base.joinpath(subpath)
    breadcrumbs = create_breadcrumbs(Path(subpath), "routes.template_path_view")
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
        return render_template("templates/template_file_list.html", **directory)

    return redirect(url_for("routes.template_edit_file", subpath=subpath))


@bp.route("/templates/edit/", defaults={"subpath": ""}, methods=["GET"])
@bp.route("/templates/edit/<path:subpath>")
def template_edit_file(subpath: str):
    ssp_base: Path = get_ssp_root()
    crumb_path: Path = Path(subpath)
    file_path: Path = ssp_base.joinpath(subpath)
    breadcrumbs = create_breadcrumbs(
        Path(*crumb_path.parts), "routes.template_path_view"
    )
    if not file_path.exists():
        with open(file_path, "w") as f:
            f.write("# New YAML file\n")

    with open(file_path, "r") as f:
        content = f.read()

    page_data: dict = {
        "title": "Edit Template",
        "content": content,
        "filename": subpath,
        "breadcrumbs": breadcrumbs,
    }

    return render_template("templates/template_editor.html", **page_data)


@bp.route("/templates/save", methods=["POST"])
def template_save_file():
    filename = request.form.get("filename")
    content = request.form.get("content")

    if not filename or not content:
        flash("Missing filename or content", "error")
        abort(400, description="Missing required file or content")

    if filename.endswith((".yaml", ".yml")):
        try:
            yaml = YAML(typ="safe", pure=True)
            yaml.load(content)
        except YAMLError as e:
            flash("Invalid YAML", "error")
            logger.error(f"Invalid YAML: {str(e)}")
            abort(400, description=f"Invalid YAML: {str(e)}")

    ssp_base: Path = get_ssp_root()
    file_path: Path = ssp_base.joinpath(filename)
    with open(file_path, "w") as f:
        f.write(content)

    flash("File saved successfully", "status")
    return redirect(request.referrer or "/")


@bp.route("/templates/create", methods=["GET", "POST"])
def template_new_file():
    if request.method == "POST":
        filename = request.form.get("filename")
        if not filename:
            return redirect(url_for("index"))

        if not filename.endswith((".yaml", ".yml")):
            filename += ".yaml"

        return redirect(url_for("edit_file", filename=filename))

    return render_template("templates/new_file.html")
