import os
from dotenv import load_dotenv


load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
VAULT_PATH = os.getenv("VAULT_PATH")
LANGUAGE = os.getenv("LANGUAGE", "German")

TYPE_TO_FOLDER = {
    "submission": "Submission",
    "escape": "Escape",
    "sweep": "Sweep",
    "pass": "Pass",
    "position": "Positionen",
    "takedown": "Takedown",
    "throw": "Throw",
}