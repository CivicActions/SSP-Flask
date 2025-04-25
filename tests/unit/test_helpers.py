from pathlib import Path

from app.helpers.helpers import file_to_html, get_project_root, get_ssp_root


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
