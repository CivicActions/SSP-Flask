"""
Copyright 2019-2025 CivicActions, Inc. See the README file at the top-level
directory of this distribution and at https://github.com/CivicActions/ssp-flask#license.
"""

import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-key-please-change")
    FLASK_DEBUG = False
    SSP_BASE = os.environ.get("SSP_BASE")


class DevelopmentConfig(Config):
    FLASK_DEBUG = True


class TestingConfig(Config):
    TESTING = True
    FLASK_DEBUG = True
    SSP_BASE = (
        Path(__file__).parent.parent.joinpath("tests").joinpath("testssp").as_posix()
    )
