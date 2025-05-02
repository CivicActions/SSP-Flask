"""
Copyright 2019-2025 CivicActions, Inc. See the README file at the top-level
directory of this distribution and at https://github.com/CivicActions/ssp-flask#license.
"""

from flask import redirect, request

from app.routes import bp
from app.ssp_tools.createfiles import create_files


@bp.route("/createfiles", defaults={"subpath": ""}, methods=["GET"])
@bp.route("/createfiles/<path:subpath>")
def toolkit_render_files(subpath: str):
    to_render = subpath
    create_files(to_render=to_render)
    return redirect(request.referrer or "/")
