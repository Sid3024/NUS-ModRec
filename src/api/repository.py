from pathlib import Path

from src.data_io.load import load_majors, load_job_titles


def get_all_majors(MAJORS_JSON_PATH: Path) -> list[str]:
    return load_majors(MAJORS_JSON_PATH)


def get_jobs_for_major(JOBS_JSON_PATH: Path, major: str) -> list[str]:
    return load_job_titles(JOBS_JSON_PATH, major)