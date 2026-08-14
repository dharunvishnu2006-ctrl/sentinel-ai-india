import json
import logging
from pathlib import Path

logger = logging.getLogger(f"sentinel.{__name__}")

VERSIONS_FILE = Path("docs/versions.json")


def load_versions(path: Path = VERSIONS_FILE) -> list:
    if not path.exists():
        raise FileNotFoundError(
            f"versions.json not found at {path}. " f"Run from the project root."
        )
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        raise ValueError(f"versions.json is malformed: {e}")
    versions = data.get("versions", [])
    logger.info(f"Loaded {len(versions)} versions")
    return versions


def current_version(versions=None):
    if versions is None:
        versions = load_versions()
    shipped = [v for v in versions if v["status"] == "shipped"]
    return shipped[-1] if shipped else None


def feature_lines(version):
    return [f"- {feat}" for feat in version.get("features", [])]


def bug_lines(version):
    return [f"- {bug}" for bug in version.get("bugs_fixed", [])]


def total_roadmap_steps(versions=None):
    return 600
