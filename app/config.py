import os
from dotenv import load_dotenv


load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
VAULT_PATH = os.getenv("VAULT_PATH")
LANGUAGE = os.getenv("LANGUAGE", "English")

TYPE_TO_FOLDER = {
    "submission": "Submission",
    "escape": "Escape",
    "sweep": "Sweep",
    "pass": "Pass",
    "position": "Position",
    "takedown": "Takedown",
    "throw": "Throw",
}