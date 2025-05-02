"""
Copyright 2019-2025 CivicActions, Inc. See the README file at the top-level
directory of this distribution and at https://github.com/CivicActions/ssp-flask#license.
"""

from flask import render_template

from app.helpers.helpers import file_to_html, get_ssp_root, list_directories, list_files
from app.routes import bp
from app.ssp_tools.helpers.toolkitconfig import ToolkitConfig


@bp.route("/rendered", methods=["GET"])
def rendered_view():
    config = ToolkitConfig()
    rendered_base = config.ssp_base.joinpath("rendered")
    rendered_dirs = list_directories(path=rendered_base)
    rendered_files = list_files(path=rendered_base)
    content: dict = {
        "title": "Rendered Files",
        "page_title": "Rendered Files",
        "directories": rendered_dirs,
        "files": rendered_files,
    }
    return render_template("rendered/rendered_directory_list.html", **content)


@bp.route("/rendered/", defaults={"subpath": ""}, methods=["GET"])
@bp.route("/rendered/<path:subpath>")
def rendered_path_view(subpath: str):
    ssp_base = get_ssp_root()
    file_path = ssp_base.joinpath(subpath)
    if file_path.is_dir():
        rendered_dirs = list_directories(path=file_path)
        rendered_files = list_files(path=file_path)
        directory: dict = {
            "title": file_path.name.capitalize(),
            "page_title": file_path.name.capitalize(),
            "directories": rendered_dirs,
            "files": rendered_files,
        }
        return render_template("rendered/rendered_directory_list.html", **directory)

    file_contents = file_to_html(file_path)
    files: dict = {
        "title": "Rendered Files",
        "page_title": file_path.name,
        "content": file_contents,
        "file_path": subpath.replace("rendered", "templates"),
    }
    return render_template("rendered/rendered_file.html", **files)
