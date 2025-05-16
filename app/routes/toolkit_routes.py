"""
Copyright 2019-2025 CivicActions, Inc. See the README file at the top-level
directory of this distribution and at https://github.com/CivicActions/ssp-flask#license.
"""

from pathlib import Path

from flask import redirect, request

from app.helpers.helpers import get_ssp_root
from app.routes.routes import bp
from app.ssp_tools.createfiles import create_files
from app.ssp_tools.make_families import make_families


@bp.route("/createfiles", defaults={"subpath": ""}, methods=["GET"])
@bp.route("/createfiles/<path:subpath>")
def toolkit_render_files(subpath: str):
    to_render = subpath
    create_files(to_render=to_render)
    return redirect(request.referrer or "/")


@bp.route("/makefamilies", methods=["GET"])
def toolkit_make_families():
    ssp_root: Path = get_ssp_root()
    make_families(ssp_root=ssp_root)
    return redirect(request.referrer or "/")
