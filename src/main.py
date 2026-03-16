from src.config.config import my_config
from src.data_io.load import load_jobs, load_mods
from src.alg.greedy_basic import greedy_basic_selection
from src.data_io.user_target_jobs import get_target_jobs
def main():
    user_jobs = [("Logistics Engineer", "backup"), ("Supply Chain Manager", "target")]

    jobs = load_jobs(my_config.JOBS_FILE_PATH)
    mods = load_mods(my_config.MODS_FILE_PATH)
    target_jobs = get_target_jobs(user_jobs=user_jobs, jobs=jobs, my_config=my_config)
    for job in target_jobs:
        print(f"{job.title=}, {job.weight=}")

    out = greedy_basic_selection(mods, target_jobs, my_config)
    for mod in out:
        print(mod.title)

if __name__ == "__main__":
    main()