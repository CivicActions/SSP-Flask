"""
Copyright 2019-2025 CivicActions, Inc. See the README file at the top-level
directory of this distribution and at https://github.com/CivicActions/ssp-flask#license.


Given a YAML file and path to directory of template files, this tool
generates markdown files, replicating the directory structure in the template
directory. It uses the https://github.com/CivicActions/secrender tool for
variable replacement.
"""

from pathlib import Path

from flask import flash

from app.ssp_tools.helpers import secrender
from app.ssp_tools.helpers.ssptoolkit import find_toc_tag, load_template_args


def create_files(ssp_base: Path | str, to_render: str):
    ssp_path: Path = Path(ssp_base) if isinstance(ssp_base, str) else ssp_base
    output_to: Path = ssp_path.joinpath(to_render.replace("templates", "rendered"))
    render: Path = ssp_path.joinpath(to_render)
    render = render.with_suffix(".md.j2") if render.suffix == ".md" else render

    if render.exists():
        if render.is_dir():
            create_multiple_files(to_render=render, output_to=output_to)
        elif render.is_file():
            write_file(to_render=render, output_to=output_to)
    else:
        flash(f"File '{render}' does not exist.", "error")


def create_multiple_files(to_render: Path, output_to: Path):
    if not output_to.is_dir():
        output_to.mkdir(parents=True, exist_ok=True)
    template_path = Path(to_render).rglob("*")
    template_files = [file for file in template_path if file.is_file()]

    for template in template_files:
        new_file = output_to.joinpath(template)
        write_file(to_render=new_file, output_to=output_to)


def write_file(to_render: Path, output_to: Path):
    template_args = load_template_args()
    new_file = output_to.joinpath(output_to)
    if new_file.suffix == ".j2":
        new_file = new_file.with_name(new_file.stem)
    flash(f"Creating file: {new_file} from {to_render}", "info")

    secrender.secrender(
        template_path=to_render.as_posix(),
        template_args=template_args,
        output_path=new_file.as_posix(),
    )

    find_toc_tag(file=str(new_file))
