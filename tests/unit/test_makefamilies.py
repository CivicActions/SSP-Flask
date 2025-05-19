from pathlib import Path

import pytest
from flask import current_app

from app.ssp_tools.family import Control
from app.ssp_tools.helpers.project import Project
from app.ssp_tools.make_families import add_controls


class TestMakeFamilies:

    @pytest.fixture(autouse=True)
    def setup_method(self, app_context):
        self.project = Project(ssp_root=current_app.config["SSP_BASE"])
        self.ssp_base = Path(current_app.config["SSP_BASE"])

    def test_make_families(self):
        assert isinstance(self.project.controls.get("AC"), dict)

    def test_family_name(self):
        family_name = self.project.get_standard("AC")
        assert family_name.get("name") == "Access Control"

    def test_add_controls(self):
        controls = add_controls(
            family_controls=self.project.controls.get("AC", {}),
            project=self.project,
            ssp_base=self.ssp_base,
        )
        assert isinstance(controls.get("AC-01"), Control)
