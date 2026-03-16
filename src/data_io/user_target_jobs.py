from src.types.domain import Job
from src.config.config import MyConfig
import copy
def get_target_jobs(user_jobs, jobs: list[Job], my_config: MyConfig) -> list[Job]:
    target_jobs = []
    for job_tuple in user_jobs:
        job_to_add = None
        for job in jobs:
            if job_tuple[0] == job.title:
                job_to_add = copy.deepcopy(job)
                if job_tuple[1] == "target":
                    job_to_add.weight = my_config.target_job_weight
                elif job_tuple[1] == "dream":
                    job_to_add.weight = my_config.dream_job_weight
                elif job_tuple[1] == "backup":
                    job_to_add.weight = my_config.backup_job_weight
                else:
                    raise ValueError(f"job_tuple contains invalid job_type: {job_tuple[1]}")
                break
        if job_to_add is not None:
            target_jobs.append(job_to_add)
    return target_jobs