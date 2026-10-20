import ast
import json
import re
from datetime import datetime, timedelta, timezone
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

import pytest
from streamlit.testing.v1 import AppTest

from src import brand, home_data

ROOT = Path(__file__).resolve().parent.parent
PAGES = [
    "views/home.py",
    "views/command_centre.py",
    "views/evolution.py",
    "views/about.py",
]
COMING_NEXT_LABEL = "Coming next - 4 modules"


def _versions_json():
    path = ROOT / "docs" / "versions.json"
    return json.loads(path.read_text(encoding="utf-8"))["versions"]


def _newest_shipped():
    shipped = [v for v in _versions_json() if v["status"] == "shipped"]
    return shipped[-1]


def _online_response(payload):
    response = MagicMock()
    response.json.return_value = payload
    response.raise_for_status.return_value = None
    return response


@pytest.fixture
def offline():
    # Fail every request without sleeping.
    no_sleep = SimpleNamespace(sleep=lambda seconds: None)
    with (
        patch(
            "src.clients.requests.get",
            side_effect=ConnectionError("offline"),
        ),
        patch("src.retry.time", no_sleep),
    ):
        yield


def _run_page(page=None):
    at = AppTest.from_file(str(ROOT / "app.py"), default_timeout=60)
    at.run()
    if page:
        at.switch_page(page)
        at.run()
    return at


def test_agents_kpi_equals_registry():
    registry = home_data.build_registry()
    assert home_data.agents_registered(registry) == len(registry.agents)
    assert home_data.agents_registered(registry) == 2


def test_systems_online_counts_both_online():
    payload = {"alerts_count": 1, "datasets_profiled": 1}
    with patch(
        "src.clients.requests.get",
        return_value=_online_response(payload),
    ):
        checks = home_data.check_systems()
    assert len(checks) == 2
    assert home_data.systems_online(checks) == 2


def test_systems_online_counts_none_offline(offline):
    checks = home_data.check_systems()
    assert home_data.systems_online(checks) == 0
    for check in checks:
        assert check["status"] == "degraded"
        assert check["checked_at"].utcoffset() == timedelta(0)


def test_status_line_shows_utc():
    from views.shared import status_line

    check = {
        "status": "degraded",
        "checked_at": datetime(2026, 10, 20, 8, 5, 9, tzinfo=timezone.utc),
    }
    assert status_line(check) == "not reachable, checked 08:05:09 UTC"


def test_status_lines_on_pages_show_utc(offline):
    home = _run_page()
    home_text = " ".join(m.value for m in home.main.markdown)
    assert home_text.count(" UTC") == 2
    centre = _run_page("views/command_centre.py")
    centre_text = " ".join(c.value for c in centre.main.caption)
    assert centre_text.count(" UTC") == 2


def test_task_history_column_order():
    calls = _chart_calls("dataframe")
    assert calls
    for page, node in calls:
        order = _keyword(node, "column_order")
        assert order == ["urgency", "task", "trace_id"], page


def test_display_status_maps_failures():
    assert home_data.display_status("online") == "online"
    assert home_data.display_status("degraded") == "not reachable"
    assert home_data.display_status("anything") == "not reachable"


def test_tasks_kpi_equals_file_rows(tmp_path):
    path = tmp_path / "history.csv"
    path.write_text(
        "1,First,id-1\n2,Second,id-2\n5,Third,id-3\n",
        encoding="utf-8",
    )
    rows = home_data.load_task_history(path)
    assert home_data.tasks_recorded(rows) == 3
    assert rows[0] == {"urgency": 1, "task": "First", "trace_id": "id-1"}


def test_missing_task_file_gives_zero(tmp_path):
    rows = home_data.load_task_history(tmp_path / "missing.csv")
    assert home_data.tasks_recorded(rows) == 0


def test_tests_kpi_equals_versions_json():
    assert home_data.tests_passing() == _newest_shipped()["tests"]


def test_today_version_equals_versions_json():
    version = brand.current_version()
    assert version == _newest_shipped()["version"]
    assert version in brand.today_line(version)


def test_route_map_has_fixed_size_and_hops():
    dot = home_data.route_map_dot()
    assert f'size="{home_data.ROUTE_MAP_SIZE}"' in dot
    assert dot.count('label="1 hop"') == 2


def test_urgency_counts_match_rows():
    rows = [
        {"urgency": 1, "task": "a", "trace_id": "x"},
        {"urgency": 1, "task": "b", "trace_id": "y"},
        {"urgency": 4, "task": "c", "trace_id": "z"},
    ]
    counts = home_data.urgency_counts(rows)
    assert counts["Urgency"] == ["1", "2", "3", "4", "5"]
    assert counts["Tasks"] == [2, 0, 0, 1, 0]


def _chart_calls(name):
    # Collect chart calls across pages.
    found = []
    for page in PAGES:
        tree = ast.parse((ROOT / page).read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue
            if getattr(node.func, "attr", None) == name:
                found.append((page, node))
    return found


def _keyword(node, arg):
    values = [k.value for k in node.keywords if k.arg == arg]
    return ast.literal_eval(values[0]) if values else None


def test_route_map_called_at_content_width():
    calls = _chart_calls("graphviz_chart")
    assert calls
    for page, node in calls:
        assert _keyword(node, "width") == "content", page


def test_telemetry_bar_chart_height():
    calls = _chart_calls("bar_chart")
    assert calls
    for page, node in calls:
        assert _keyword(node, "height") == 220, page


def test_no_matplotlib_on_pages():
    assert not _chart_calls("pyplot")


def test_command_centre_has_no_invented_lists():
    text = (ROOT / "views" / "command_centre.py").read_text(encoding="utf-8")
    for name in (
        "queue_depths",
        "tasks_per_agent",
        "response_times",
        "response_times_by_agent",
    ):
        assert name not in text


def test_no_html_in_any_python_file():
    banned = ("unsafe_" + "allow_html", "st." + "html")
    for path in ROOT.rglob("*.py"):
        parts = path.relative_to(ROOT).parts
        if "venv" in parts or ".git" in parts:
            continue
        text = path.read_text(encoding="utf-8")
        for word in banned:
            assert word not in text, f"{word} found in {path}"


def test_home_top_lines(offline):
    at = _run_page()
    assert not at.exception
    assert at.title[0].value == brand.BRAND.name
    values = [m.value for m in at.main.markdown]
    assert f"#### Vision: {brand.BRAND.vision}" in values
    today = brand.today_line(brand.current_version())
    assert f":orange[**{today}**]" in values
    pattern = re.compile(r"^:orange\[\*\*.+\*\*\]$")
    assert any(pattern.match(v) for v in values)


def test_home_kpis_match_sources(offline):
    at = _run_page()
    shown = {m.label: m.value for m in at.main.metric}
    rows = home_data.load_task_history()
    registry = home_data.build_registry()
    version = brand.current_version()
    assert shown["Agents registered"] == str(len(registry.agents))
    assert shown["Connected systems online"] == "0 of 2"
    assert shown["Tasks recorded"] == str(len(rows))
    tests_label = f"Tests passing (recorded for {version})"
    assert shown[tests_label] == str(_newest_shipped()["tests"])


def test_coming_next_in_sidebar_closed(offline):
    at = _run_page()
    boxes = [e for e in at.sidebar.expander if e.label == COMING_NEXT_LABEL]
    assert len(boxes) == 1
    box = boxes[0]
    assert box.proto.expanded is False
    text = "\n".join(m.value for m in box.markdown)
    lines = [ln for ln in text.splitlines() if "arrives in" in ln]
    assert len(lines) == 4
    assert len(box.metric) == 0
    home_labels = [e.label for e in at.main.expander]
    assert COMING_NEXT_LABEL not in home_labels


@pytest.mark.parametrize("page", PAGES)
def test_every_page_runs(offline, page):
    at = _run_page(page)
    assert not at.exception
    assert len(at.title) == 1
    captions = " ".join(c.value for c in at.sidebar.caption)
    assert "System healthy" in captions
