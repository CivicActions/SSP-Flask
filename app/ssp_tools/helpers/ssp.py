"""
Copyright 2019-2025 CivicActions, Inc. See the README file at the top-level
directory of this distribution and at https://github.com/CivicActions/ssp-flask#license.
"""

from typing import List

from pydantic import BaseModel

from app.ssp_tools.family import Family


class Ssp(BaseModel):
    name: str
    standards: List[str]
    families: List[Family]
