from pathlib import Path

from dotenv import load_dotenv


def load_environment() -> None:
    """Load environment variables from the repository .env file."""
    project_root = Path(__file__).resolve().parents[1]
    load_dotenv(project_root / ".env", override=False)
