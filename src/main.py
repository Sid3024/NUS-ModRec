from src.config.config import my_config
from src.data_io.load import load_jobs, load_mods
from src.alg.greedy_basic import greedy_basic_selection
from src.data_io.create_student import construct_student
from src.types.domain import ModType
def main():
    user_jobs_tuple = [("Logistics Engineer", "backup"), ("Supply Chain Manager", "target")]
    user_major = "Industrial Systems Engineering"
    user_desc = "I like math heavy mods"
    jobs = load_jobs(my_config.JOBS_FILE_PATH)
    mods = load_mods(my_config.MODS_FILE_PATH)
    student = construct_student(
        user_major=user_major,
        user_desc=user_desc,
        user_jobs_tuple=user_jobs_tuple,
        jobs=jobs,
        my_config=my_config
    )
    for job in student.my_jobs:
        print(f"{job.title=}, {job.weight=}")
    mod_type = ModType(type="Technical Electives")
    out = greedy_basic_selection(
        mod_pool=mods,
        student=student,
        mod_type=mod_type,
        my_config=my_config
    )
    for mod in out:
        print(mod.title)

if __name__ == "__main__":
    main()