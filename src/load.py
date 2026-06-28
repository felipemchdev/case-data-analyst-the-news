import pandas as pd
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"


def load_sessions():
    return pd.read_csv(RAW_DIR / "palavritas_sessions.csv")


def load_attempts():
    return pd.read_csv(RAW_DIR / "palavritas_attempts.csv")


def load_user_profile():
    return pd.read_csv(RAW_DIR / "user_profile.csv")


def load_all():
    return load_sessions(), load_attempts(), load_user_profile()


def save_cleaned(sessions, attempts, profile):
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    sessions.to_csv(PROCESSED_DIR / "sessions_clean.csv", index=False)
    attempts.to_csv(PROCESSED_DIR / "attempts_clean.csv", index=False)
    profile.to_csv(PROCESSED_DIR / "profile_clean.csv", index=False)
    print(f"Salvo em {PROCESSED_DIR}")
