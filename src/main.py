from src.config.config import my_config
from src.data_io.load import load_jobs, load_mods
from src.alg.greedy_basic import greedy_basic_selection
from src.data_io.create_student import construct_student
from src.types.domain import ModType
from src.explanation_agent.agent import run_explanation_agent
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
    selected_mods = greedy_basic_selection(
        mod_pool=mods,
        student=student,
        mod_type=mod_type,
        my_config=my_config
    )
    for mod in selected_mods:
        print(mod.title)
    success_received_all_reasoning, selected_mods_with_reasoning, error_msg = run_explanation_agent(student=student, selected_mods=selected_mods)
    print(f"{success_received_all_reasoning=}")
    print(f"{error_msg=}")
    if selected_mods is not None:
        for mod_dict in selected_mods_with_reasoning:
            print(f"mod: {mod_dict['title']}\nreasoning: {mod_dict['reasoning']}")
    
    

if __name__ == "__main__":
    main()