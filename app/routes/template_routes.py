"""
Copyright 2019-2025 CivicActions, Inc. See the README file at the top-level
directory of this distribution and at https://github.com/CivicActions/ssp-flask#license.
"""

from flask import render_template

from app.helpers.helpers import file_to_html, get_ssp_root, list_directories, list_files
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
    }
    return render_template("templates/template_file_list.html", **templates)


@bp.route("/templates/", defaults={"subpath": ""}, methods=["GET"])
@bp.route("/templates/<path:subpath>")
def template_path_view(subpath: str):
    ssp_base = get_ssp_root()
    file_path = ssp_base.joinpath(subpath)
    if file_path.is_dir():
        directory_list = list_directories(path=file_path)
        file_list = list_files(path=file_path)
        directory: dict = {
            "title": file_path.name.capitalize(),
            "page_title": file_path.name.capitalize(),
            "directories": directory_list,
            "files": file_list,
        }
        return render_template("templates/template_file_list.html", **directory)

    file_contents = file_to_html(file_path)
    files: dict = {
        "title": "Template Files",
        "page_title": file_path.name,
        "content": file_contents,
        "file_path": subpath.replace("rendered", "templates"),
    }
    return render_template("templates/template_file.html", **files)
