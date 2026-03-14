import numpy as np
import copy

from src.config.config import MyConfig
from src.types.domain import TextBlock, Skill, Topic, Mod, Job
from src.types.optim import PlanOptimState
from src.calc.similarity import Job_list_Mod_sim
from src.calc.softmax import softmax
from src.alg.plan_optimizer import PlanOptimizer

def greedy_basic_selection(
        mods : list[Mod],
        target_jobs : list[Job],
        my_config: MyConfig
    ) -> list[Mod]:
    plan_optim_state = PlanOptimState(
        target_jobs=copy.deepcopy(target_jobs),
        mod_pool=copy.deepcopy(mods)
    )
    plan_optim = PlanOptimizer(
        plan_optim_state=plan_optim_state,
        my_config=my_config
    )
    while not plan_optim.is_full():
        selected_mod_idx = select_mod(plan_optim=plan_optim)
        plan_optim.select_mod(selected_mod_idx)
    return plan_optim.plan_optim_state.selected_mods


        
def select_mod(plan_optim: PlanOptimizer) -> int:
    mod_scores = []
    for mod in plan_optim.plan_optim_state.mod_pool:
        score = Job_list_Mod_sim(
            jobs=plan_optim.plan_optim_state.target_jobs, 
            mod=mod,
            selection_sim_threshold=plan_optim.selection_ambiguity_threshold
        )
        mod_scores.append(score)
    mod_scores = np.array(mod_scores)
    mod_scores_softmax = softmax(mod_scores, plan_optim.softmax_temperature)
    max_score = np.max(mod_scores_softmax)
    result = [
        (i, max_score - score)
        for i, v in enumerate(mod_scores_softmax)
        if (max_score - score) < plan_optim.selection_sim_threshold
    ]
    if len(result) > 1 and plan_optim.ambiguity_agent_active:
        idx = 1 #TODO
        out = result[idx][0]
    else:
        out = result[0][0]
    return out
    


    
        



