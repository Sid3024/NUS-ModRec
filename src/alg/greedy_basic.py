import numpy as np
import copy

from src.config.config import MyConfig
from src.types.domain import Mod, Student, ModType
from src.types.optim import PlanOptimState
from src.calc.similarity import Job_list_Mod_sim, Job_list_Mod_sim_using_cache
from src.calc.softmax import softmax
from src.alg.plan_optimizer import PlanOptimizer
from src.ambiguity_agent.agent import run_ambiguity_agent

def greedy_basic_selection(
        mod_pool: list[Mod],
        student: Student,
        mod_type: ModType,
        my_config: MyConfig
    ) -> list[Mod]:
    """
    Selects a list of mods for the student, that is optimised based on the students target jobs and their personal details (major, description).

    Args:
        mod_pool (list[Mod]): Pool of mods to select from.
        student (Student): Object of the current user containing their details (major, desc, my_jobs).
        mod_type (ModType): Type of mods we are selecting.
        target_jobs (list[Job]): List of jobs the student wants that we optimise for.
        my_config (MyConfig): Includes config params (eg for plan optimiser)
    
    Returns:
        list[Mod]: The selected list of mods
    """

    plan_optim_state = PlanOptimState(
        user_jobs=copy.deepcopy(student.my_jobs),
        mod_pool=copy.deepcopy(mod_pool)
    )
    plan_optim = PlanOptimizer(
        plan_optim_state=plan_optim_state,
        my_config=my_config
    )
    while not plan_optim.is_full() and not plan_optim.is_bucket_empty():
        selected_mod_idx = select_mod(student=student, mod_type=mod_type, plan_optim=plan_optim, max_options_for_ambiguity_agent=my_config.max_options_for_ambiguity_agent)
        plan_optim.select_mod(selected_mod_idx)
    return plan_optim.plan_optim_state.selected_mods


        
def select_mod(student: Student, mod_type: ModType, plan_optim: PlanOptimizer, max_options_for_ambiguity_agent: int) -> int:
    """
    Selects a single mod given the mods that have already been chosen.

    Args:
        plan_optim (PlanOptimizer): Allows function to keep track of chosen mods, and max_sim_score_so_far for each job skill (required for score calculation)

    Returns:
        int: index of mod chosen in the mod_pool list in PlanOptimizer

    """
    
    mod_scores = []
    sim_cache = plan_optim.get_sim_cache()
    for mod in plan_optim.plan_optim_state.mod_pool:
        score = Job_list_Mod_sim_using_cache(
            jobs=plan_optim.plan_optim_state.user_jobs,
            mod=mod,
            sim_cache=sim_cache,
            selection_sim_threshold=plan_optim.selection_sim_threshold
        )
        # score = Job_list_Mod_sim(
        #     jobs=plan_optim.plan_optim_state.user_jobs, 
        #     mod=mod,
        #     selection_sim_threshold=plan_optim.selection_sim_threshold
        # )
        #score = plan_optim.get_mod_score(mod=mod)
        if len(mod.topics):
            score /= len(mod.topics)
        mod_scores.append(score)
    mod_scores = np.array(mod_scores)
    max_score_idx = np.argmax(mod_scores)
    print(f"{mod_scores=}")
    if plan_optim.ambiguity_agent_active:
        mod_scores_softmax = softmax(mod_scores, plan_optim.softmax_temperature)
        print(f"{mod_scores_softmax=}")
        max_score = np.max(mod_scores_softmax)
        all_results = [
            (i, max_score - v)
            for i, v in enumerate(mod_scores_softmax)
            if (max_score - v) < plan_optim.selection_sim_threshold
        ]
        all_results.sort(key=lambda t: t[1])
        result = all_results[:max_options_for_ambiguity_agent]
        print(f"{result=}")
        candidate_mods = [plan_optim.plan_optim_state.mod_pool[r[0]] for r in result]
        assert(len(result) > 0), f"{len(result)=}"
        if len(result)>1:
            print("calling ambiguity agent")
            ambiguity_agent_dict = run_ambiguity_agent(
                student=student,
                mod_type=mod_type,
                candidate_mods=candidate_mods,
                already_selected_mods=plan_optim.plan_optim_state.selected_mods
            )
            print(f"{ambiguity_agent_dict=}")
            if ambiguity_agent_dict is not None:
                idx = ambiguity_agent_dict["index"]
                return result[idx][0]
    return max_score_idx
    


    
        



