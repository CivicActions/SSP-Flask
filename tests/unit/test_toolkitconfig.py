from app.ssp_tools.helpers.toolkitconfig import ToolkitConfig


def test_toolkitconfig_ssp_base(app_context):
    config: ToolkitConfig = ToolkitConfig()
    assert config.ssp_base.parts[-1] == "testssp"


def test_toolkitconfig_default_keys(app_context):
    config: ToolkitConfig = ToolkitConfig()
    assert config.default_keys.get("config-management.yaml", "") == "cm"


def test_toolkitconfig_config(app_context):
    config: ToolkitConfig = ToolkitConfig()
    assert isinstance(config.config, dict)


def test_toolkitconfig_keys(app_context):
    config: ToolkitConfig = ToolkitConfig()
    assert config.config.get("contractor", {}).get("name", "") == "CivicActions, Inc"


def test_toolkitconfig_check_config_values(app_context):
    config: ToolkitConfig = ToolkitConfig()
    contractor_name = config.check_config_values(file="contractor", key="name")
    assert contractor_name == "CivicActions, Inc"


def test_toolkitconfig_get_rendered_files(app_context):
    config: ToolkitConfig = ToolkitConfig()
    rendered_files = config.get_rendered_files()
    assert len(rendered_files) == 2


def test_toolkitconfig_get_template_files(app_context):
    config: ToolkitConfig = ToolkitConfig()
    rendered_files = config.get_template_files()
    assert len(rendered_files) == 2
