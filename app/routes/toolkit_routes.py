from datetime import datetime

from flask import redirect, request

from app.routes import bp
from app.ssp_tools.createfiles import create_files
from app.ssp_tools.helpers.toolkitconfig import ToolkitConfig

date = datetime.now().strftime("%Y")


@bp.route("/createfiles", defaults={"subpath": ""}, methods=["GET"])
@bp.route("/createfiles/<path:subpath>")
def toolkit_render_files(subpath: str):
    config = ToolkitConfig()
    to_render = subpath
    create_files(ssp_base=config.ssp_base, to_render=to_render)
    return redirect(request.referrer or "/")
