from dataclasses import dataclass

from src import versions


@dataclass(frozen=True)
class Brand:
    name: str = "Sentinel AI India"
    vision: str = "Unified AI security command centre"
    today_text: str = (
        "agent registry, priority queue, routing, links to "
        "CloudShield and AutoPilot - agents are Python classes; "
        "LLM agents arrive in v4"
    )
    accent: str = "#B45309"


BRAND = Brand()


def current_version(version_list=None):
    # Return newest shipped version name.
    shipped = versions.current_version(version_list)
    return shipped["version"] if shipped else None


def today_line(version):
    return f"Today ({version}): {BRAND.today_text}"
