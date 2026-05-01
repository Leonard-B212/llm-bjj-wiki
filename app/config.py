import os
from dotenv import load_dotenv


VAULT_PATH = r"C:\Users\leona\Documents\Obsidian\BJJ"


load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

TYPE_TO_FOLDER = {
    "submission": "Submission",
    "escape": "Escape",
    "sweep": "Sweep",
    "pass": "Pass",
    "position": "Positionen",
    "takedown": "Takedown",
    "throw": "Throw",
}