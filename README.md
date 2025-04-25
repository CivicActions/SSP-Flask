# SSP Flask

The [CivicActions SSP Toolkit](https://github.com/Civicactions/ssp-toolkit) is a collection of Python
scripts, and markdown and YAML file templates that are used to automate the generation of System Security
Plan documents. SSP Flask is a wrapper for the SSP Toolkit which uses a
[Flask](https://flask.palletsprojects.com/en/stable/) web application to facilitate the generation and
management of the files.

## Installation

### Repo setup

Clone the SSP Flask repository to a directory on your system and enter the SSP Flask directory:

```shell
git git clone git@github.com:CivicActions/SSP-Flask.git
cd ssp-flask
```

Copy your existing SSP Toolkit the same directory:

```shell
cp -rf [PATH TO YOUR REPO]/ssp-toolkit ./ssp
```

If you are starting a new project, clone the SSP Toolkit into a directory named `ssp` within the `ssp-flask`
directory and checkout the v2.0.0 tag with the correct file structure to use with SSP Flask.

```shell
git clone git@github.com:CivicActions/ssp-toolkit.git ssp
git checkout tags v2.0.0
```

### Project setup

Once you have the SSP Flask code and the SSP Toolkit in the same directory, create a `.env` file with the
following values:

```dotenv
SECRET_KEY=SomeSecretKeyOrNotSoSecretKey
SSP_BASE=ssp
```

The `SSP_BASE` variable should point to the directory in which your SSP Toolkit repository is in within the SSP
Flask project root directory. If you choose to use something other than `ssp` for the SSP Toolkit directory
you will need to add it to the `.gitignore` file so that the Toolkit files are not included in any commits
that you make.

### Project structure

The SSP Flask uses a slightly different directory structure than older versions of the SSP Toolkit. Rather
than rendering files directly into directories in the project root, all the rendered files are written to a
directory named `rendered` in the project root. The rendered files will maintain the file structure in the
rendered directory that they have in the templates directory. For example, the contingency plan in the
templates appendices directory, `/templates/appendices/contingency-plan.md.j2`, will be rendered to
`/rendered/appendices/contingency-plan.md`.

You can either create a `rendered` directory and move your existing root level directories,
`appendencies`, `components`, `docs`, `docx` and `frontmatter`, to the rendered
directory, or let SSP Flask create the rendered directory and create all new files there.

If you use the `v2.0.0` tag version of the SSP Toolkit, the files are structured to work with SSP Flask.

## Usage

You can either run the application using the [uv package manager](https://docs.astral.sh/uv/)
or using Docker.

### Using uv

Once you have cloned the repository, install the dependencies and run the Flask
app using the following commands:

```shell
uv sync
uv run -- flask run --port 3000
```

You should see a message similar the following, and should be able to access
the website using the address listed:

```shell
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://127.0.0.1:3000
```

### Using Docker/docker compose

#### Installation on Windows Subsystem for Linux (WSL2)

The easiest way to run Docker on WSL2 is using the
[Docker Desktop](https://www.docker.com/products/docker-desktop) application.

This will install both Docker and docker compose.

#### Running the application

To start the application, enter into the project root directory and run either:

```shell
docker-compose up
```

or

```shell
docker compose up
```

depending on your version of docker compose.

## Local development

### Dependencies and virtual environments

We are using the [uv package manager](https://docs.astral.sh/uv/getting-started/installation/). Once you have
cloned the repo, you will need to run `uv sync` in order to create your virtual environment and to install
all the required Python packages. `uv` will install the required Python version if your local version of
Python doesn't meet the minimum requirements.

### Linting and code checking

You will need to install [pre-commit](https://pre-commit.com/#install) and instantiate it in your git
repository by running `pre-commit install`. Once pre-commit is installed it will run every time that you make
a commit. Some of the checkers can be pretty pedantic, but they are helpful, if a bit annoying.

### Gitflow

`develop` is the default branch, so all work will require creating a branch from `develop`. The naming
convention for branches should use the prefix `ssp-[TICKET NUMBER]-` followed my some pithy descriptor. For example `ssp-20-help-route`.

Pull Requests require at least one reviewer, and require that all scans and checks pass before merging.

## License

GNU General Public License v3.0 or later. Some portions of this work were produced under a Government contract and are licensed under the terms of Creative Commons Zero v1.0 Universal.

SPDX-License-Identifier: `GPL-3.0-or-later`

Copyright 2019-2024 CivicActions, Inc.
