"""
Copyright 2019-2025 CivicActions, Inc. See the README file at the top-level
directory of this distribution and at https://github.com/CivicActions/ssp-flask#license.
"""

from pathlib import Path

from flask import flash
from loguru import logger

from app.helpers.helpers import cached_file_loader, write_files
from app.ssp_tools.family import Control
from app.ssp_tools.helpers.project import Project
from app.ssp_tools.helpers.ssp import Ssp
from app.ssp_tools.helpers.ssptoolkit import find_toc_tag
from app.ssp_tools.make_families import make_families


def get_family_data(families: list, project: Project) -> Ssp:
    return Ssp(
        name=project.opencontrol.name,
        standards=project.opencontrol.standards,
        families=families,
    )


def get_standards(project: Project, ssp_base: Path) -> list:
    standards: list = []
    for std in project.opencontrol.standards:
        std_data = cached_file_loader(ssp_base.joinpath(std))
        standards.append(std_data.get("name"))
    return standards


def get_controls(control: Control) -> list:
    control_text: list = [
        f"#### {control.control_id}: {control.control_name}",
        "```text",
        control.description,
        "```",
        f"**Status:** {control.status}",
    ]
    if control.parts:
        for key, part in control.parts.items():
            if key != "_default":
                control_text.append(f"#### {key}")
            for control_part in part:
                control_text.append(f"##### {control_part.party}")
                control_text.append(control_part.narrative)

    return control_text


def write_ssp(ssp_data: Ssp, project: Project, ssp_base: Path):
    text_output: list = [
        "<!--TOC-->",
        "<!--TOC-->",
        "",
        f"# {project.opencontrol.name} System Security Plan",
        "",
    ]
    standards = get_standards(project=project, ssp_base=ssp_base)
    for standard in standards:
        text_output.append(f"## {standard}")
    text_output.append("\n")

    for family in ssp_data.families:
        text_output.append(f"### {family.family_id}: {family.family_name}\n\n")
        controls = dict(sorted(family.controls.items()))
        for _, control in controls.items():
            control_text = get_controls(control)
            text_output.extend(control_text)
    ssp_file = ssp_base.joinpath("rendered", "docs", "ssp").with_suffix(".md")
    write_files(ssp_file, "\n".join(text_output))
    find_toc_tag(file=str(ssp_file.as_posix()), levels=3)
    flash(f"{ssp_file.name} written to {ssp_file.parent.as_posix()}", "success")
    logger.info(f"{ssp_file.name} written to {ssp_file.parent.as_posix()}")


def make_ssp(ssp_root: str | Path):
    ssp_base = Path(ssp_root) if isinstance(ssp_root, str) else ssp_root
    project = Project(ssp_root=ssp_base)
    families = make_families(ssp_root=ssp_base)
    ssp_data = get_family_data(families=families, project=project)
    write_ssp(ssp_data=ssp_data, project=project, ssp_base=ssp_base)
