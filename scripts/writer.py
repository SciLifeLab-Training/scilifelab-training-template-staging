from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GENERATED = ROOT / "_generated"


def write_partial(filename, content):

    GENERATED.mkdir(exist_ok=True)

    (GENERATED / filename).write_text(
        content,
        encoding="utf-8",
    )