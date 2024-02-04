import os
import pathlib

from dotenv import load_dotenv

load_dotenv(dotenv_path=pathlib.Path(".env"))


def find_setting(key: str) -> str:
    if os.environ[key] is None:
        raise RuntimeError(f"Not found env key: {key}")
    return os.environ[key]


def find_setting_no_error(key: str) -> str | None:
    return os.environ[key]


loglevel = find_setting_no_error("LOGLEVEL")
csv_dir = find_setting("CSV_DIR")
mode = find_setting("MODE")
resume_race_id = find_setting_no_error("RESUME_RACE_ID")
