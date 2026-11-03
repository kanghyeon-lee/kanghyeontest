from pathlib import Path

import pytest

ROOT = Path(__file__).parent
MARKER_BY_DIR = {
    ROOT / "tests": "web",
    ROOT / "api_tests": "api",
}


def pytest_collection_modifyitems(items):
    # 디렉터리 기준으로 web / api 마커를 자동으로 붙인다 (pytest -m api / -m web)
    for item in items:
        path = Path(str(item.fspath))
        for directory, marker in MARKER_BY_DIR.items():
            if directory in path.parents:
                item.add_marker(getattr(pytest.mark, marker))
