"""
Copyright 2019-2025 CivicActions, Inc. See the README file at the top-level
directory of this distribution and at https://github.com/CivicActions/ssp-flask#license.
"""

import json
from collections import defaultdict
from pathlib import Path

from app.helpers.helpers import get_hash


class FileChecker:
    hash_file: Path
    hashes: dict[str, str] = defaultdict(lambda: "")
    changed_files: int = 0

    def __init__(self, ssp_root: Path):
        self.hash_file = ssp_root.joinpath("file_hashes").with_suffix(".json")
        if not Path(self.hash_file).exists():
            Path(self.hash_file).touch()
        with open(self.hash_file, "r+", encoding="utf-8") as f:
            try:
                self.hashes = json.load(f)
            except json.JSONDecodeError:
                self.hashes = {}

    # Check if the file has changed.
    def has_changed(self, path: str) -> bool:
        hashed_file = get_hash(path)
        if file_hash := self.hashes.get(path, False):
            has_changed = file_hash != hashed_file
        else:
            has_changed = True
        if has_changed:
            self.changed_files += 1
            self.hashes[path] = hashed_file
        return has_changed

    # Write the hashes to the hash_file.json
    def write_changes(self) -> None:
        print(f"Updating file hashes in {self.hash_file.as_posix()}")
        with open(self.hash_file, "w+", encoding="utf-8") as f:
            json.dump(self.hashes, f, indent=2)
