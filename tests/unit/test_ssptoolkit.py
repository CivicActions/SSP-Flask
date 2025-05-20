import pytest
from flask import current_app

from app.ssp_tools.helpers import ssptoolkit
from app.ssp_tools.helpers.opencontrol import OpenControl
from app.ssp_tools.helpers.project import Project
from app.ssp_tools.helpers.toolkitconfig import ToolkitConfig


class TestSSPToolkit:

    @pytest.fixture(autouse=True)
    def setup_project(self, app_context):
        self.project = Project(ssp_root=current_app.config["SSP_BASE"])

    def test_sortable_control_id(self):
        test_cid = ssptoolkit.sortable_control_id("AC-1")
        test_cid_extended = ssptoolkit.sortable_control_id("AC-3 (9)")

        assert test_cid == "AC-01"
        assert test_cid_extended == "AC-03 (09)"

    def test_to_oc_control_id(self):
        oc_simple = ssptoolkit.to_oc_control_id("AC-01")
        oc_extended = ssptoolkit.to_oc_control_id("AC-02 (02)")
        assert oc_simple == "AC-1"
        assert oc_extended == "AC-2 (2)"

    def test_get_project(self, app_context):
        assert isinstance(self.project.opencontrol, OpenControl)

    def test_get_standards(self, app_context):
        assert self.project.get_standard("AC-1").get("name") == "Policy and Procedures"

    def test_get_certification_baseline(self, app_context):
        baseline = self.project.get_certification_baseline()
        assert len(baseline) == 194

    def test_get_standards_control_data(self, app_context):
        control_data = self.project.get_standards_control_data(control="AC-2")
        assert str(control_data.get("description")).find(
            "a. Identifies and selects the following"
        )

    def test_get_standards_family_name(self, app_context):
        ac = self.project.get_standard(
            "AC",
        )
        assert ac.get("name") == "Access Control"

    def test_get_component_files(self, app_context):
        components = ssptoolkit.get_component_files(self.project.opencontrol.components)
        assert len(components) == 14
        assert "SA-SYSTEM_AND_SERVICES_ACQUISITION" in components

    def test_load_controls_by_id(self, app_context):
        controls = ssptoolkit.load_controls_by_id(
            self.project.opencontrol.get_components()
        )
        assert "AC-2" in controls

    def test_config_keys(app_context):
        config = ToolkitConfig()
        assert len(config.config_files) == 15
        assert "sop" in config.config

    def test_config_values(app_context):
        config = ToolkitConfig()
        contractor = config.check_config_values(file="contractor", key="name_short")
        assert contractor == "CivicActions"
