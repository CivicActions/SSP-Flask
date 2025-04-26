"""
Copyright 2019-2025 CivicActions, Inc. See the README file at the top-level
directory of this distribution and at https://github.com/CivicActions/ssp-flask#license.
"""

import json
from pathlib import Path

import markdown
import yaml
from flask import current_app, flash
from loguru import logger


def file_to_html(path: Path | str) -> str:
    ssp_dir = get_project_root()
    file_path = ssp_dir.joinpath(current_app.config.get("SSP_BASE", "ssp")).joinpath(
        path
    )
    file = Path(file_path) if isinstance(file_path, str) else file_path
    file_content: str = ""
    try:
        with open(file, "r") as fp:
            if file.suffix == ".yaml":
                file_content = yaml_to_html_list(yaml.safe_load(fp))
            elif file.suffix == ".md":
                file_content = markdown.markdown(fp.read())
            elif file.suffix == ".json":
                file_content = json.dumps(json.loads(fp.read()))
    except FileNotFoundError:
        logger.error(f"File { file.as_posix() } not found")
        flash(f"File { file.as_posix() } not found", "error")
    finally:
        return file_content


def yaml_to_html_list(data: dict | list) -> str:
    html = "<ul id='yaml-list'>"
    if isinstance(data, dict):
        for key, value in data.items():
            html += f"<li><strong>{key}:</strong> {yaml_to_html_list(value)}</li>"
    elif isinstance(data, list):
        for item in data:
            html += f"<li>{yaml_to_html_list(item)}</li>"
    else:
        html += str(data)
    html += "</ul>"
    return html


def get_project_root():
    current_file = Path(__file__).resolve()
    for parent in current_file.parents:
        if (parent / "pyproject.toml").exists():
            return parent
    logger.error("Project root (with pyproject.toml) not found.")
    raise FileNotFoundError("Project root (with pyproject.toml) not found.")


def get_ssp_root() -> Path:
    project_root = get_project_root()
    ssp_base = current_app.config.get("SSP_BASE", "ssp")
    return project_root.joinpath(ssp_base)
