"""
Copyright 2019-2025 CivicActions, Inc. See the README file at the top-level
directory of this distribution and at https://github.com/CivicActions/ssp-flask#license.
"""

from pathlib import Path
from typing import Generator

from flask import flash
from loguru import logger

from app.helpers.helpers import cached_file_loader, load_yaml_files
from app.ssp_tools.helpers.opencontrol import OpenControl
from app.ssp_tools.helpers.ssptoolkit import sortable_control_id


class Project:
    ssp_root: Path
    opencontrol: OpenControl
    config: Path
    controls: dict
    standards: dict = {}

    def __init__(self, ssp_root: str | Path):
        self.ssp_root = Path(ssp_root) if isinstance(ssp_root, str) else ssp_root
        self.__load_config()
        self.__load_opencontrol()
        self._sort_standard_controls()

    def __load_config(self):
        if self.ssp_root.joinpath("configuration.yaml").exists():
            self.config = self.ssp_root.joinpath("configuration.yaml")
        else:
            raise FileNotFoundError("configuration.yaml not found in project root.")

    def __load_opencontrol(self):
        oc_file = self.ssp_root.joinpath("opencontrol").with_suffix(".yaml")
        if oc_file.is_file():
            self.opencontrol = OpenControl.load(oc_file.as_posix())
        else:
            logger.error("Could not find opencontrol.yaml file.")
            flash("Could not find opencontrol.yaml file.", "error")

    def _sort_standard_controls(self):
        controls: dict = {}
        for certification in self.opencontrol.certifications:
            cert_path = self.ssp_root.joinpath(certification)
            cert = load_yaml_files(cert_path)

            for control in self._get_certification_controls(cert):
                family = control[:2]
                if family not in controls:
                    controls[family] = {}
                controls[family][sortable_control_id(control)] = control
                dict(sorted(controls[family].items()))
        self.controls = dict(sorted(controls.items()))

    @staticmethod
    def _get_certification_controls(cert: dict) -> Generator[str, None, None]:
        for standard in cert.get("standards", {}).values():
            for control_id, _ in standard.items():
                yield control_id

    def get_standard(self, control_id: str) -> dict:
        for standard in self.opencontrol.standards:
            self.standards.update(cached_file_loader(self.ssp_root.joinpath(standard)))
        return self.standards.get(control_id, {})

    def get_standards_control_data(self, control: str) -> dict:
        return self.standards.get(control, {})

    @staticmethod
    def _get_control_narratives(component: dict) -> Generator[tuple, None, None]:
        for satisfies in component.get("satisfies", []):
            scid = sortable_control_id(satisfies.get("control_key"))
            yield scid, satisfies

    def get_certification_baseline(self) -> list:
        certifications: list = []
        for certs in self.opencontrol.certifications:
            certification = load_yaml_files(self.ssp_root.joinpath(certs))
            certifications.append(certification)

        controls: list = []
        for standards in certifications:
            for _, control_ids in standards.get("standards").items():
                controls.extend(control_ids.keys())

        return list(dict.fromkeys(controls))
