"""
Copyright 2019-2025 CivicActions, Inc. See the README file at the top-level
directory of this distribution and at https://github.com/CivicActions/ssp-flask#license.
"""

from pathlib import Path

import yaml
from flask import abort, flash, redirect, render_template, request, url_for
from loguru import logger

from app.helpers.helpers import get_ssp_root
from app.routes import bp
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


@bp.route("/edit/", defaults={"subpath": ""}, methods=["GET"])
@bp.route("/edit/<path:subpath>")
def edit_file(subpath: str):
    ssp_base: Path = get_ssp_root()
    file_path: Path = ssp_base.joinpath(subpath)
    if not file_path.exists():
        with open(file_path, "w") as f:
            f.write("# New YAML file\n")

    with open(file_path, "r") as f:
        content = f.read()

    return render_template("pages/editor.html", filename=subpath, content=content)


@bp.route("/save", methods=["POST"])
def save_file():
    filename = request.form.get("filename")
    content = request.form.get("content")

    if not filename or not content:
        flash("Missing filename or content", "error")
        abort(400, description="Missing required file or content")

    try:
        yaml.safe_load(content)
    except yaml.YAMLError as e:
        abort(400, description=f"Invalid YAML: {str(e)}")

    ssp_base: Path = get_ssp_root()
    file_path: Path = ssp_base.joinpath(filename)
    with open(file_path, "w") as f:
        f.write(content)

    flash("File saved successfully", "status")
    return redirect(request.referrer or "/")


@bp.route("/new", methods=["GET", "POST"])
def new_file():
    if request.method == "POST":
        filename = request.form.get("filename")
        if not filename:
            return redirect(url_for("index"))

        if not filename.endswith((".yaml", ".yml")):
            filename += ".yaml"

        return redirect(url_for("edit_file", filename=filename))

    return render_template("pages/new_file.html")
