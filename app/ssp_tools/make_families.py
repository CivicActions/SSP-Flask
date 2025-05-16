"""
Copyright 2019-2025 CivicActions, Inc. See the README file at the top-level
directory of this distribution and at https://github.com/CivicActions/ssp-flask#license.
"""

from collections import defaultdict
from pathlib import Path

from flask import flash
from loguru import logger

from app.helpers.helpers import cached_file_loader
from app.ssp_tools.family import Control, Family, Part
from app.ssp_tools.helpers.project import Project
from app.ssp_tools.helpers.ssptoolkit import sortable_control_id

ssp_base: Path
project: Project
output_dir: Path
statuses: dict


def get_components(family: str):
    for component in sorted(
        ssp_base.joinpath("rendered", "components").rglob(f"**/{family}-*.yaml")
    ):
        yield component.parent.name, cached_file_loader(component)


def get_statements(family: Family):
    for name, component in get_components(family=family.family_id):
        for narrative in component.get("satisfies", []):
            key = sortable_control_id(narrative.get("control_key", ""))
            if key in family.controls:
                family.controls[key] = get_control_parts(
                    parts=narrative.get("narrative"),
                    control=family.controls[key],
                    component=name,
                )


def get_control_parts(parts: list, control, component: str) -> Control:
    for p in parts:
        part_id = p.get("key", "_default")
        control.add_part(
            part_id,
            Part(
                key=part_id,
                party=component,
                narrative=p.get("text"),
            ),
        )
    return control


def add_controls(family: dict) -> dict:
    controls: dict = {}
    for control_id, control in family.items():
        control_data = project.get_standard(control)
        controls[control_id] = Control(
            control_id=control,
            control_name=control_data.get("name", ""),
            description=control_data.get("description", ""),
            status=statuses.get(control, "incomplete"),
            parts=defaultdict(),
        )
    return controls


def create_families():
    for family_id, family in project.controls.items():
        controls = add_controls(family)
        family_name = project.get_standard(family_id)
        family_object = Family(
            title=f"{family_id}: {family_name.get('name', '')}",
            family_id=family_id,
            family_name=family_name.get("name", ""),
            controls=controls,
        )
        get_statements(family_object)
        family_object.print_family_file(out_path=output_dir)

    logger.info(f"Families files written to {output_dir.as_posix()}.")
    flash(f"Families files written to {output_dir.as_posix()}.", "success")


def make_families(ssp_root: str | Path):
    global ssp_base
    ssp_base = Path(ssp_root) if isinstance(ssp_root, str) else ssp_root

    global project
    project = Project(ssp_root=ssp_root)

    global statuses
    statuses = cached_file_loader(ssp_base.joinpath("keys", "status.yaml"))

    global output_dir
    output_dir = ssp_base.joinpath("rendered", "docs", "controls")
    if not output_dir.exists():
        output_dir.mkdir(parents=True, exist_ok=True)

    create_families()
