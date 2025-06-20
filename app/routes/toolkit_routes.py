"""
Copyright 2019-2025 CivicActions, Inc. See the README file at the top-level
directory of this distribution and at https://github.com/CivicActions/ssp-flask#license.
"""

from pathlib import Path

from flask import redirect, request

from app.helpers.helpers import get_ssp_root
from app.routes import bp
from app.ssp_tools.createfiles import create_files
from app.ssp_tools.exportto import export_to
from app.ssp_tools.make_families import make_families
from app.ssp_tools.make_ssp import make_ssp


@bp.route("/createfiles", defaults={"subpath": ""}, methods=["GET"])
@bp.route("/createfiles/<path:subpath>")
def toolkit_render_files(subpath: str):
    to_render = subpath
    create_files(to_render=to_render)
    return redirect(request.referrer or "/")


@bp.route("/exportto", defaults={"subpath": ""}, methods=["GET"])
@bp.route("/exportto/<path:subpath>")
def toolkit_export_files(subpath: str):
    file_to_export = subpath
    export_to(to_export=file_to_export)
    return redirect(request.referrer or "/")


@bp.route("/makefamilies", methods=["GET"])
def toolkit_make_families():
    ssp_root: Path = get_ssp_root()
    make_families(ssp_root=ssp_root)
    return redirect(request.referrer or "/")


@bp.route("/makessp", methods=["GET"])
def toolkit_make_ssp():
    ssp_root: Path = get_ssp_root()
    make_ssp(ssp_root=ssp_root)
    return redirect(request.referrer or "/")
