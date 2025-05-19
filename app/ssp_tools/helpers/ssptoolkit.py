"""
Copyright 2019-2025 CivicActions, Inc. See the README file at the top-level
directory of this distribution and at https://github.com/CivicActions/ssp-flask#license.
"""

import mmap
import re
from collections import defaultdict
from pathlib import Path

import md_toc
import yaml

from app.helpers.helpers import get_ssp_root
from app.ssp_tools.helpers import secrender
from app.ssp_tools.helpers.toolkitconfig import ToolkitConfig


class ControlRegExps:
    oc_simple = re.compile(r"^([A-Z]{2})-(0\d+)$")
    oc_extended = re.compile(r"^([A-Z]{2})-(0\d+)\s*\((0\d+)\)$")


def sortable_control_id(control_id: str) -> str:
    return re.sub(r"(\d+)", lambda m: m.group(1).zfill(2), control_id)


def to_oc_control_id(control_id: str) -> str:
    match = re.match(ControlRegExps.oc_simple, control_id)
    if match:
        family = match.group(1)
        number = int(match.group(2))
        return f"{family}-{number}"

    # AC-2(1)
    match = re.match(ControlRegExps.oc_extended, control_id)
    if match:
        family = match.group(1)
        number = int(match.group(2))
        extension = int(match.group(3))
        return f"{family}-{number} ({extension})"

    return control_id


def get_component_files(components: list) -> dict:
    component_files: defaultdict = defaultdict()
    ssp_root = get_ssp_root()
    rendered = ssp_root.joinpath("rendered")
    for component_dir in components:
        with rendered.joinpath(component_dir, "component.yaml").open("r") as cfp:
            component = yaml.load(cfp, Loader=yaml.SafeLoader)
        for family in component.get("satisfies"):
            component_file = rendered.joinpath(component_dir, family)
            family_name = component_file.stem
            if family_name not in component_files:
                component_files[family_name] = []
            component_files[family_name].append(component_file.as_posix())

    return dict(sorted(component_files.items()))


def load_controls_by_id(component_list: list) -> dict:
    component_files = get_component_files(components=component_list)
    controls: dict = {}
    for _, components in component_files.items():
        for component in components:
            component_path = Path(component)
            try:
                with open(component_path, "r") as fp:
                    component_data = yaml.load(fp, Loader=yaml.SafeLoader)
            except FileNotFoundError as error:
                raise error
            parent = component_path.parents[0].name
            for satisfies in component_data.get("satisfies"):
                control_id = satisfies.get("control_key")
                cid = control_id
                if cid not in controls:
                    controls[cid] = []
                controls[cid].append({parent: satisfies})

    return dict(sorted(controls.items()))


def load_template_args() -> dict:
    config = ToolkitConfig()
    return secrender.get_template_args(yaml=config.config, set_={}, root="")


def get_control_statuses() -> dict:
    config = ToolkitConfig()
    statuses = config.config.get("status", {})
    return statuses


def find_toc_tag(file: str, levels: int = 3):
    with (
        open(file, "rb", 0) as f,
        mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ) as s,
    ):
        if s.find(b"<!--TOC-->") != -1:
            write_toc(file, levels=levels)


def write_toc(file: str | Path, levels: int):
    toc = md_toc.api.build_toc(filename=file, keep_header_levels=levels, skip_lines=5)
    md_toc.api.write_string_on_file_between_markers(
        filename=file,
        string=toc,
        marker="<!--TOC-->",
    )


def load_yaml_files(file_path: str | Path) -> dict:
    load_file = Path(file_path) if isinstance(file_path, str) else file_path
    try:
        with open(load_file, "r") as fp:
            project = yaml.safe_load(fp)
            return project
    except FileNotFoundError:
        raise FileNotFoundError(
            f"No {load_file.name} found in {load_file.parent.as_posix()}."
        )
