# SSP Flask

SSP Flask is a wrapper for the [CivicActions SSP Toolkit](https://github.com/Civicactions/ssp-toolkit)
that uses a web application using a [Flask](https://flask.palletsprojects.com/en/stable/)
app to facilitate the generation of SSP documentation.

## Installation

### Repo setup

Clone the SSP Flask repository to a directory on your system and enter the SSP Flask directory:

```shell
git git clone https://git.civicactions.net/lincs/ssp-flask.git
cd testssp-flask
```

Copy your existing SSP Toolkit the same directory:

```shell
cp -rf [PATH TO YOUR REPO]/testssp-toolkit .
```

If you are starting a new project, clone the SSP Toolkit into the `ssp-flask` directory:

```shell
git clone git@github.com:CivicActions/testssp-toolkit.git
```

### Project setup

Once you have the SSP Flask code and the SSP Toolkit living in the same directory, create a `.env` file
with the following values:

```dotenv
SECRET_KEY=SomeSecretKeyOrNotSoSecretKey
SSP_BASE=SSPTOOLKITDIRECTORY
```

The `SSP_BASE` variable should point to the directory in which your SSP Toolkit repository is in within
the SSP Flask project root directory.

### Project structure

The SSP Flask uses a slightly different directory structure than older versions of the SSP Toolkit.
Rather than rendering files directly into directories in the project root, all the rendered files are
written to a directory named `rendered` in the project root. The rendered files will maintain the
file structure in the rendered directory that they have in the templates directory. For example, the
contingency plan in the templates
appendices directory, `/templates/appendices/contingency-plan.md.j2`, will
 be rendered to `/rendered/appendices/contingency-plan.md`.

You can either create a `rendered` directory and move your existing root level directories,
`appendencies`, `components`, `docs`, `docx` and `frontmatter`, to the rendered
directory, or let SSP Flask create the rendered directory and create all new files.

## Usage

You can either run the application using the [UV package manager](https://docs.astral.sh/uv/)
or using Docker.

### Using UV

Once you have cloned the repository, install the dependencies and run the Flask
app using the following commands:

```shell
uv sync
uv run -- flask --port 3000
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

_more updates coming_
