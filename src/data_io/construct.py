import copy
from typing import Any

from src.types.domain import Job, Student
from src.config.config import MyConfig


def construct_student(
    user_major: str,
    user_jobs_input: list[dict[str, Any]],
    jobs: list[Job],
    my_config: MyConfig
) -> Student:
    """
    Constructs a Student object from API input.

    Args:
        user_major: The student's major.
        user_jobs_input: Jobs from API request, e.g.
            [{"title": "ML Engineer", "type": "target"}]
        jobs: Master job list (with embeddings).
        my_config: Config with job type weights.
    """

    user_jobs: list[Job] = []

    for job_input in user_jobs_input:
        input_title = job_input.get("title")
        input_type = job_input.get("type")

        if input_title is None:
            raise ValueError("Each job input must contain a 'title'")
        if input_type is None:
            raise ValueError("Each job input must contain a 'type'")

        job_to_add = None

        # Find matching job from master list
        for job in jobs:
            if input_title == job.title:
                job_to_add = copy.deepcopy(job)

                # Assign type + weight
                if input_type == "target":
                    job_to_add.type = "target"
                    job_to_add.weight = my_config.target_job_weight

                elif input_type == "dream":
                    job_to_add.type = "dream"
                    job_to_add.weight = my_config.dream_job_weight

                elif input_type == "backup":
                    job_to_add.type = "backup"
                    job_to_add.weight = my_config.backup_job_weight

                else:
                    raise ValueError(f"Invalid job type: {input_type}")

                break

        if job_to_add is None:
            raise ValueError(f"Job title not found in master list: {input_title}")

        user_jobs.append(job_to_add)

    student = Student(
        major=user_major,
        desc="",
        my_jobs=user_jobs
    )

    return student
