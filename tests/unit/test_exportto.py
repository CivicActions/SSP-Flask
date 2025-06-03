import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

from app.ssp_tools.exportto import export_to, render_file, render_multiple


class TestExportTo(unittest.TestCase):

    @patch("app.ssp_tools.exportto.get_ssp_root")
    @patch("app.ssp_tools.exportto.convert_file")
    @patch("app.ssp_tools.exportto.flash")
    @patch("app.ssp_tools.exportto.Path")
    def test_render_file(
        self, mock_path, mock_flash, mock_convert_file, mock_get_ssp_root
    ):
        mock_path.return_value.exists.return_value = True
        to_render = Path("/fake/path/file.md")
        output_to = Path("/fake/output/file")

        render_file(
            to_render=to_render, output_to=output_to, ssp_root=mock_get_ssp_root
        )

        mock_convert_file.assert_called_once()
        mock_flash.assert_called_once()

    @patch("app.ssp_tools.exportto.get_ssp_root")
    @patch("app.ssp_tools.exportto.render_file")
    def test_render_multiple(self, mock_render_file, mock_get_ssp_root):
        to_render = MagicMock()
        to_render.glob.return_value = [
            Path("/fake/path/file1.md"),
            Path("/fake/path/file2.md"),
        ]
        output_to = Path("/fake/output")

        render_multiple(
            to_render=to_render, output_to=output_to, ssp_root=mock_get_ssp_root
        )

        self.assertEqual(mock_render_file.call_count, 2)

    @patch("app.ssp_tools.exportto.get_ssp_root")
    @patch("app.ssp_tools.exportto.render_file")
    @patch("app.ssp_tools.exportto.render_multiple")
    @patch("app.ssp_tools.exportto.flash")
    @patch("app.ssp_tools.exportto.logger")
    def test_export_to_with_file(
        self,
        mock_flash,
        mock_render_multiple,
        mock_render_file,
        mock_get_ssp_root,
        mock_logger,
    ):
        mock_get_ssp_root.return_value = Path("/fake/ssp_root")
        mock_file = MagicMock()
        mock_file.exists.return_value = True
        mock_file.is_dir.return_value = False

        with patch("app.ssp_tools.exportto.Path") as mock_path:
            mock_path.return_value.joinpath.return_value = mock_file
            mock_path.return_value.parts = ("", "some", "path")
            mock_file.parent.exists.return_value = True

            export_to(to_export="/some/path/file.md")

            mock_render_file.assert_called_once()
            mock_render_multiple.assert_not_called()
            mock_flash.assert_not_called()
