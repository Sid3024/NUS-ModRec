import copy
from src.types.domain import Job, Student
from src.config.config import MyConfig
def construct_student(
    user_major: str,
    user_jobs_input: list,   # list[JobInput]
    jobs: list[Job],
    my_config: MyConfig
) -> Student:
    """
    Constructs a Student object from API input.

    Args:
        user_major (str): The student's major.
        user_jobs_input (list[JobInput]): Jobs from API request.
        jobs (list[Job]): Master job list (with embeddings).
        my_config (MyConfig): Config with job type weights.
    """

    user_jobs = []

    for job_input in user_jobs_input:
        job_to_add = None

        # Find matching job from master list
        for job in jobs:
            if job_input.title == job.title:
                job_to_add = copy.deepcopy(job)

                # Assign type + weight
                if job_input.type == "target":
                    job_to_add.type = "target"
                    job_to_add.weight = my_config.target_job_weight

                elif job_input.type == "dream":
                    job_to_add.type = "dream"
                    job_to_add.weight = my_config.dream_job_weight

                elif job_input.type == "backup":
                    job_to_add.type = "backup"
                    job_to_add.weight = my_config.backup_job_weight

                else:
                    raise ValueError(f"Invalid job type: {job_input.type}")

                break

        if job_to_add is not None:
            user_jobs.append(job_to_add)

    student = Student(
        major=user_major,
        desc="",  # no longer coming from API
        my_jobs=user_jobs
    )

    return student