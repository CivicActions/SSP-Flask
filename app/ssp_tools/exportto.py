"""
Copyright 2019-2025 CivicActions, Inc. See the README file at the top-level
directory of this distribution and at https://github.com/CivicActions/ssp-flask#license.
"""

from pathlib import Path

from flask import flash
from loguru import logger
from pypandoc import convert_file

from app.helpers.helpers import get_ssp_root


def render_multiple(to_render: Path, output_to: Path, ssp_root: Path):
    for file_path in to_render.glob("**/*.md"):
        render_file(to_render=file_path, output_to=output_to, ssp_root=ssp_root)


def render_file(to_render: Path, output_to: Path, ssp_root: Path):
    args: list = []
    custom_reference: Path = ssp_root.joinpath("assets/custom-reference.docx")
    if custom_reference.exists():
        args.append(f"--reference-doc={custom_reference.as_posix()}")

    convert_file(
        source_file=to_render,
        to="docx",
        outputfile=str(output_to.with_suffix(".docx")),
        extra_args=args,
    )
    logger.info(f"Exporting file to {output_to.with_suffix('.docx').as_posix()}")
    flash(f"Writing file {output_to.with_suffix('.docx').as_posix()}", "info")


def export_to(to_export: str | Path):
    ssp_root: Path = get_ssp_root()
    file_base_path: tuple = Path(to_export).parts[1:]
    file_to_export: Path = ssp_root.joinpath(to_export)
    export_directory: Path = ssp_root.joinpath("rendered", "docx")
    export_file = export_directory.joinpath(*file_base_path)
    if not export_file.parent.exists():
        export_file.parent.mkdir(exist_ok=False)

    if file_to_export.exists():
        if file_to_export.is_dir():
            render_multiple(
                to_render=file_to_export, output_to=export_file, ssp_root=ssp_root
            )
        else:
            render_file(
                to_render=file_to_export, output_to=export_file, ssp_root=ssp_root
            )
    else:
        logger.error(f"Exportto: file not found: {to_export}")
        flash(f"Exportto: file not found: {to_export}", "error")
