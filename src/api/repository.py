from pathlib import Path

from src.data_io.load import load_majors, load_job_titles
from src.config.config import my_config


def get_all_majors() -> list[str]:
    return load_majors(my_config.MAJORS_FILE_PATH)


def get_jobs_for_major(major: str) -> list[str]:
    return load_job_titles(my_config.JOBS_FILE_PATH, major)