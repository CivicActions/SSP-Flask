"""
Copyright 2019-2025 CivicActions, Inc. See the README file at the top-level
directory of this distribution and at https://github.com/CivicActions/ssp-flask#license.
"""

import os
from dataclasses import dataclass, field
from pathlib import Path

import yaml
from flask import flash
from loguru import logger

from app.helpers.helpers import get_ssp_root


@dataclass
class ToolkitConfig:
    default_keys: dict = field(
        default_factory=lambda: {
            "artifacts.yaml": "artifact",
            "config-management.yaml": "cm",
            "info_system.yaml": "information_system",
            "justifications.yaml": "justify",
        }
    )
    ssp_base: Path = field(default_factory=Path)
    keys: Path = field(default_factory=Path)
    config_files: list[()] = field(default_factory=list)
    config: dict = field(default_factory=dict)

    def __post_init__(self):
        self.ssp_base = get_ssp_root()
        self.keys = self.ssp_base.joinpath("keys")
        opencontrol = self.ssp_base.joinpath("opencontrol").with_suffix(".yaml")
        try:
            with open(opencontrol, "r") as f:
                self.opencontrol = yaml.safe_load(f)
        except FileNotFoundError as oce:
            logger.error(f"OpenControl file not found: {oce}")
            flash(f"OpenControl file not found: {oce}", "error")
        finally:
            self.get_configuration()

    def get_configuration(self):
        config_file = self.ssp_base.joinpath("configuration.yaml")
        if config_file.exists():
            try:
                with open(config_file, "r") as fp:
                    self.config = yaml.safe_load(fp)
            except IOError:
                logger.error(f"Error loading {config_file.as_posix}.")
                flash(f"Error loading {config_file.as_posix}.", "error")
        else:
            flash("configuration.yaml not found in project root.", "error")
        self.load_keys()

    def load_keys(self):
        for filename in self.keys.glob("*.yaml"):
            key = self.default_keys.get(filename.name, filename.stem)
            self.config_files.append((filename.name, key))
            try:
                with open(filename, "r") as fp:
                    self.config[key] = yaml.safe_load(fp)
            except FileNotFoundError as ke:
                logger.error(f"Error loading {filename.as_posix}.", ke)
                flash(f"Error loading {filename.as_posix}.", "error")

    def check_config_values(self, file: str, key: str = "") -> str | dict:
        if key:
            values = self.config.get(file, {}).get(key, "")
        else:
            values = self.config.get(file, {})
        return values

    def get_rendered_files(self) -> dict:
        rendered = self.ssp_base.joinpath("rendered")
        if not rendered.exists():
            rendered.mkdir()
        return self.__list_files_recursively(rendered.as_posix())

    def get_template_files(self) -> dict:
        template_dir = self.ssp_base.joinpath("templates")
        return self.__list_files_recursively(template_dir)

    def __list_files_recursively(self, root_dir: Path | str) -> dict:
        result = {}
        for dir_path, dir_names, filenames in os.walk(root_dir):
            path = os.path.relpath(dir_path, self.ssp_base)
            if filenames:
                filenames.sort()
                result[path] = filenames
        return result
