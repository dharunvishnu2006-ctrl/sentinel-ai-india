from src.versions import load_versions, current_version, total_roadmap_steps

versions = load_versions()
print(f"Loaded {len(versions)} versions")
current = current_version(versions)
print(
    f"Current: {current['version']}, "
    f"{current['steps_covered']} steps, {current['tests']} tests"
)
print(f"Total roadmap: {total_roadmap_steps()}")
