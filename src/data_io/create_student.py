# from src.custom_types.domain import Job, Student
# from src.config.config import MyConfig
# import copy
# from typing import Any


# def construct_student_api(user_major: str, 
#     user_jobs_input: list[tuple[str, Any]],
#     jobs: list[Job], 
#     my_config: MyConfig) -> Student:
#     """
#     Constructs a student object.

#     Args:
#         user_major (str): The student's major.
#         user_desc (str): The student's description.
#         user_jobs (list[tuple[str, str]]): tuple of the list of user's chosen jobs in the form (title, job_type_str).
#         my_config (MyConfig): Config class containing the weights of each job type.
#     """
    
#     user_jobs = []
#     for job_tuple in user_jobs_tuple:
#         job_to_add = None
#         for job in jobs:
#             if job_tuple[0] == job.title:
#                 job_to_add = copy.deepcopy(job)
#                 if job_tuple[1] == "target":
#                     job_to_add.type = "target"
#                     job_to_add.weight = my_config.target_job_weight
#                 elif job_tuple[1] == "dream":
#                     job_to_add.type = "dream"
#                     job_to_add.weight = my_config.dream_job_weight
#                 elif job_tuple[1] == "backup":
#                     job_to_add.type = "backup"
#                     job_to_add.weight = my_config.backup_job_weight
#                 else:
#                     raise ValueError(f"job_tuple contains invalid job_type: {job_tuple[1]}")
#                 break
#         if job_to_add is not None:
#             user_jobs.append(job_to_add)
#     student = Student(major=user_major, desc=user_desc, my_jobs=user_jobs)
#     return student

# def construct_student(user_major: str, 
#     user_desc: str, 
#     user_jobs_tuple: list[tuple[str, str]],
#     jobs: list[Job], 
#     my_config: MyConfig) -> Student:
#     """
#     Constructs a student object.

#     Args:
#         user_major (str): The student's major.
#         user_desc (str): The student's description.
#         user_jobs (list[tuple[str, str]]): tuple of the list of user's chosen jobs in the form (title, job_type_str).
#         my_config (MyConfig): Config class containing the weights of each job type.
#     """
    
#     user_jobs = []
#     for job_tuple in user_jobs_tuple:
#         job_to_add = None
#         for job in jobs:
#             if job_tuple[0] == job.title:
#                 job_to_add = copy.deepcopy(job)
#                 if job_tuple[1] == "target":
#                     job_to_add.type = "target"
#                     job_to_add.weight = my_config.target_job_weight
#                 elif job_tuple[1] == "dream":
#                     job_to_add.type = "dream"
#                     job_to_add.weight = my_config.dream_job_weight
#                 elif job_tuple[1] == "backup":
#                     job_to_add.type = "backup"
#                     job_to_add.weight = my_config.backup_job_weight
#                 else:
#                     raise ValueError(f"job_tuple contains invalid job_type: {job_tuple[1]}")
#                 break
#         if job_to_add is not None:
#             user_jobs.append(job_to_add)
#     student = Student(major=user_major, desc=user_desc, my_jobs=user_jobs)
#     return student
