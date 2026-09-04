import os

from app.config import LANGUAGE


SCHEMA_DIR = os.path.dirname(__file__)


def load_schema(note_type):
    schema_path = os.path.join(SCHEMA_DIR, f"{note_type}_schema.md")

    if not os.path.exists(schema_path):
        raise FileNotFoundError(f"Schema not found: {schema_path}")

    with open(schema_path, "r", encoding="utf-8") as file:
        return file.read()


def load_global_rules():
    path = os.path.join(SCHEMA_DIR, "global_rules.md")

    with open(path, "r", encoding="utf-8") as file:
        return file.read().replace("{LANGUAGE}", LANGUAGE)