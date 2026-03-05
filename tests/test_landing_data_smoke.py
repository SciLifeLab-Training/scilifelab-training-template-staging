from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]


def load_yaml(path: Path) -> dict:
    content = yaml.safe_load(path.read_text(encoding="utf-8"))
    assert isinstance(content, dict)
    return content


def test_instances_have_one_visible_current() -> None:
    data = load_yaml(ROOT / "data" / "instances.yml")
    instances = data.get("instances")
    assert isinstance(instances, list)

    current = [item for item in instances if isinstance(item, dict) and item.get("status") == "current"]
    assert len(current) == 1
    assert current[0].get("visible", True) is True


def test_landing_data_has_expected_sections() -> None:
    data = load_yaml(ROOT / "data" / "landing.yml")
    assert isinstance(data.get("course"), dict)
    assert isinstance(data.get("hero_actions"), list)
    assert isinstance(data.get("cards"), list)
