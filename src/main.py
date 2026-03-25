from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.routes import router
from src.logging_setup import setup_logging
from src.recommendation_audit import init_audit_db


setup_logging()
init_audit_db()

app = FastAPI(title="NUS ModRec API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)







# from src.config.config import my_config
# from src.data_io.load import load_jobs, load_mods
# from src.alg.greedy_basic import greedy_basic_selection
# from src.data_io.create_student import construct_student
# from src.types.domain import ModType
# from src.explanation_agent.agent import run_explanation_agent
# def main():
#     user_jobs_tuple = [("Logistics Engineer", "backup"), ("Supply Chain Manager", "target")]
#     user_major = "Industrial Systems Engineering"
#     user_desc = "I like math heavy mods"
#     jobs = load_jobs(my_config.JOBS_FILE_PATH)
#     mods = load_mods(my_config.MODS_FILE_PATH)
#     student = construct_student(
#         user_major=user_major,
#         user_desc=user_desc,
#         user_jobs_tuple=user_jobs_tuple,
#         jobs=jobs,
#         my_config=my_config
#     )
#     for job in student.my_jobs:
#         print(f"{job.title=}, {job.weight=}")
#     mod_type = ModType(type="Technical Electives")
#     user_chosen_mods = []
#     selected_mods = greedy_basic_selection(
#         mod_pool=mods,
#         user_chosen_mods=user_chosen_mods,
#         student=student,
#         mod_type=mod_type,
#         my_config=my_config
#     )
#     for mod in selected_mods:
#         print(mod.title)
#     success_received_all_reasoning, selected_mods_with_reasoning, error_msg = run_explanation_agent(student=student, selected_mods=selected_mods)
#     print(f"{success_received_all_reasoning=}")
#     print(f"{error_msg=}")
#     if selected_mods is not None:
#         for mod_dict in selected_mods_with_reasoning:
#             print(f"mod: {mod_dict['title']}\nreasoning: {mod_dict['reasoning']}")
    
    

# if __name__ == "__main__":
#     main()