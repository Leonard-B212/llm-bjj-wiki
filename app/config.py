import os
from dotenv import load_dotenv


load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
VAULT_PATH = os.getenv("VAULT_PATH")
LANGUAGE = os.getenv("LANGUAGE", "English")

WRITER_MODEL = os.getenv("WRITER_MODEL", "gpt-5.6-luna")
CLASSIFIER_MODEL = os.getenv("CLASSIFIER_MODEL", "gpt-4.1-mini")

TYPE_TO_FOLDER = {
    "submission": "Submission",
    "escape": "Escape",
    "sweep": "Sweep",
    "pass": "Pass",
    "position": "Position",
    "takedown": "Takedown",
    "throw": "Throw",
}