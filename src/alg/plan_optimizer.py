from src.config.config import MyConfig
from src.types.domain import Mod, Job
from src.types.optim import PlanOptimState
from src.calc.similarity import topic_skill_sim

class PlanOptimizer:
    def __init__(
            self, plan_optim_state: PlanOptimState, 
            my_config: MyConfig
        ):
        self.plan_optim_state = plan_optim_state
        self.selection_capacity = my_config.selection_capacity
        self.softmax_temperature = my_config.softmax_temperature
        self.selection_sim_threshold = my_config.selection_sim_threshold
        self.selection_ambiguity_threshold = my_config.selection_ambiguity_threshold
        self.ambiguity_agent_active = my_config.ambiguity_agent_active


    def select_mod(self, selected_mod_idx : int) -> bool:
        if self.is_full():
            return False
        selected_mod = self.plan_optim_state.mod_pool.pop()
        self.update_max_sim_so_far(selected_mod)
        self.plan_optim_state.selected_mods.append(selected_mod)
        return True
    
    def update_max_sim_so_far(self, mod: Mod):
        for job in self.plan_optim_state.target_jobs:
            for skill in job.skills:
                skill_mod_max_sim = 0.0
                for topic in mod.topics:
                    sim = topic_skill_sim(topic=topic, skill=skill)
                    if sim > skill_mod_max_sim:
                        skill_mod_max_sim = sim
                if skill_mod_max_sim > skill.max_sim_score_so_far:
                    skill.max_sim_score_so_far = skill_mod_max_sim

    def is_full(self):
        return len(self.plan_optim_state.selected_mods) == self.selection_capacity