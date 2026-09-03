from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"


def load_yaml(filename):
    with open(DATA / filename, encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_course():
    return load_yaml("course.yml")["course"]


def load_website():
    return load_yaml("website.yml")["website"]

def load_content():
    return load_yaml("website.yml")["content"]

def load_schedule():
    return load_yaml("schedule.yml")["events"]

def load_team():
    return load_yaml("team.yml")["team"]

def load_announcements():

    with open("data/announcements.yml", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}

    return data.get("announcements", [])