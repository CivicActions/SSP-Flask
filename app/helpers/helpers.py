"""
Copyright 2019-2025 CivicActions, Inc. See the README file at the top-level
directory of this distribution and at https://github.com/CivicActions/ssp-flask#license.
"""

import json
from functools import lru_cache
from pathlib import Path
from typing import List, Optional

import markdown
from flask import current_app, flash, url_for
from loguru import logger
from ruamel.yaml import YAML


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
                yaml = YAML(typ="safe", pure=True)
                file_content = yaml_to_html_list(yaml.load(fp))
            elif file.suffix == ".md" or file.suffix == ".j2":
                file_content = markdown.markdown(fp.read())
            elif file.suffix == ".json":
                file_content = json.dumps(json.loads(fp.read()))
            else:
                file_content = fp.read()
    except FileNotFoundError:
        logger.error(f"File { file.as_posix() } not found")
        flash(f"File { file.as_posix() } not found", "error")
    finally:
        pass

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


@lru_cache(maxsize=128)
def cached_file_loader(filepath: Path | str):
    file_path = Path(filepath) if isinstance(filepath, str) else filepath
    if file_path.suffix == ".yaml" or file_path.suffix == ".yml":
        return load_yaml_files(file_path)
    elif file_path.suffix == ".json":
        import json

        with open(file_path, "r") as f:
            return json.load(f)
    else:
        with open(file_path, "r") as f:
            return f.read()


def load_yaml_files(file_path: str | Path) -> dict:
    load_file = Path(file_path) if isinstance(file_path, str) else file_path
    try:
        with open(load_file, "r") as fp:
            yaml = YAML(typ="safe", pure=True)
            project = yaml.load(fp)
            return project
    except FileNotFoundError:
        logger.error(f"No {load_file.name} found in {load_file.parent.as_posix()}.")
        flash(f"No {load_file.name} found in {load_file.parent.as_posix()}.", "error")
        return {}


def write_files(file_path: str | Path, content: str):
    write_file = Path(file_path) if isinstance(file_path, str) else file_path
    if not write_file.parent.exists():
        write_file.parent.mkdir(parents=True)
    logger.info(f"Writing {write_file.as_posix()}")
    with open(write_file, "w+") as fp:
        fp.write(content)


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


def list_directories(path: Path, exclude: Optional[List[str]] = None) -> list[str]:
    if exclude is None:
        exclude = []
    ssp_base = get_ssp_root()
    return [
        directory.relative_to(ssp_base).as_posix()
        for directory in path.iterdir()
        if directory.is_dir() and directory.name not in exclude
    ]


def list_files(path: Path) -> list[str]:
    ssp_base = get_ssp_root()
    return [
        filepath.relative_to(ssp_base).as_posix()
        for filepath in path.iterdir()
        if filepath.is_file()
    ]


def create_breadcrumbs(
    path: Path, route: str, exclude_level: Optional[List[str]] = None
) -> list[dict]:
    if exclude_level is None:
        exclude_level = []
    breadcrumbs: list = []
    path_parts = path.parts
    for i, crumb in enumerate(path_parts):
        breadcrumb_path = Path(*path.parts[: i + 1])
        if crumb not in exclude_level:
            breadcrumbs.append(
                {
                    "name": Path(crumb).name,
                    "path": url_for(route, subpath=breadcrumb_path.as_posix()),
                }
            )
    return breadcrumbs
