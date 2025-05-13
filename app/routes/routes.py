"""
Copyright 2019-2025 CivicActions, Inc. See the README file at the top-level
directory of this distribution and at https://github.com/CivicActions/ssp-flask#license.
"""

from flask import Blueprint

bp = Blueprint(
    "routes",
    __name__,
    template_folder="templates",
)

from app.routes import page_routes  # noqa: E402, F401
from app.routes import rendered_routes  # noqa: E402, F401
from app.routes import template_routes  # noqa: E402, F401
from app.routes import toolkit_routes  # noqa: E402, F401
