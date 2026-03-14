from src.config.config import my_config
from src.data_io.load import load_jobs, load_mods
from src.alg.greedy_basic import greedy_basic_selection
def main():
    jobs = load_jobs(my_config.JOBS_FILE_PATH)
    mods = load_mods(my_config.MODS_FILE_PATH)
    # print(f"{jobs=}")
    # print(f"{mods=}")

    out = greedy_basic_selection(mods, jobs, my_config)
    print(out)

if __name__ == "__main__":
    main()