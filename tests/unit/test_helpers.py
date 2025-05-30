"""
Copyright 2019-2025 CivicActions, Inc. See the README file at the top-level
directory of this distribution and at https://github.com/CivicActions/ssp-flask#license.
"""

from pathlib import Path

from app.helpers.helpers import (
    create_breadcrumbs,
    file_to_html,
    get_project_root,
    get_ssp_root,
)


def test_get_project_root():
    project_root = get_project_root()
    assert project_root == Path(__file__).parent.parent.parent


def test_get_ssp_root(app_context):
    ssp_root = get_ssp_root()
    assert ssp_root == Path(__file__).parent.parent.parent.joinpath("tests/testssp")


def test_file_to_html_json(app_context):
    json_file = file_to_html("assets/test_json.json")
    assert json_file is not None


def test_file_to_html_md(app_context):
    md_file = file_to_html("assets/test_md.md")
    assert "<h1>Test Data</h1>" in md_file


def test_yaml_to_html_list(app_context):
    yaml_file = file_to_html("assets/test_yaml.yaml")
    assert "<ul id='yaml-list'>" in yaml_file


def test_create_breadcrumbs(app_context):
    file_path = Path("test/breadcrumbs/links")
    breadcrumbs = create_breadcrumbs(file_path, "routes.rendered_path_view")
    assert isinstance(breadcrumbs, list)


def test_create_breadcrumb_routes(app_context, client):
    file_path = Path("test/breadcrumbs/links")
    breadcrumbs = create_breadcrumbs(file_path, "routes.rendered_path_view")
    assert (
        breadcrumbs[1].get("path") == "http://127.0.0.1:5000/rendered/test/breadcrumbs"
    )
