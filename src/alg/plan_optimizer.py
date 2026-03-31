from src.config.config import MyConfig
from src.types.domain import Mod, Job
from src.types.optim import PlanOptimState
from src.calc.similarity import topic_skill_sim, Job_list_Mod_sim, build_job_mod_sim_matrix
import numpy as np
from numpy.typing import NDArray
from copy import deepcopy

class PlanOptimizer:
    def __init__(
            self, 
            plan_optim_state: PlanOptimState, 
            my_config: MyConfig
        ):
        self.plan_optim_state = plan_optim_state
        self.selection_capacity = my_config.selection_capacity
        self.softmax_temperature = my_config.softmax_temperature
        self.selection_sim_threshold = my_config.selection_sim_threshold
        self.selection_ambiguity_threshold = my_config.selection_ambiguity_threshold
        self.ambiguity_agent_active = my_config.ambiguity_agent_active
        self.sim_cache = None
        self.mod_id_sim_matrix_map = {}
        self.mod_map_next_idx = 0
        self.preselect_mods()

    def preselect_mods(self):
        for mod in self.plan_optim_state.user_chosen_mods:
            if self.is_full():
                return False
            self.update_max_sim_so_far(mod)
            self.plan_optim_state.selected_mods.append(mod)
        return True

        

    def get_sim_cache(self) -> list[list[NDArray[np.float64]]]:
        """
        Retrieves sim_cache, a 2d array of matrices of sim scores for the current optimisation set of mods and jobs.
        (Each element of the 2d array is a matrix of sim scores btw all possible topic and skill pairs for 1 specific mod-job combo).
        
        Returns:
            list[list[NDArray[np.float64]]]:
                2d array:
                    rows: mods
                    cols: jobs
                matrix:
                    rows: topics
                    cols: skills
        """

        if self.sim_cache is None:
            self.build_sim_cache()
        return self.sim_cache

    def build_sim_cache(self):
        """
        Build sim_cache.
        """
        self.serialize_user_jobs()
        self.serialize_mod_pool()
        self.sim_cache = [[0 for _ in range(len(self.plan_optim_state.user_jobs))] for _ in range(len(self.plan_optim_state.mod_pool))]
        for mod in self.plan_optim_state.mod_pool:
            for job in self.plan_optim_state.user_jobs:
                self.sim_cache[mod.id][job.id] = build_job_mod_sim_matrix(job=job, mod=mod)

    def serialize_user_jobs(self):
        """
        Gives unique indices to each job object and each skill in user_jobs (skill indices are unique across jobs).
        """
        i = 0
        for j, job in enumerate(self.plan_optim_state.user_jobs):
            job.id = j
            for skill in job.skills:
                skill.id = i
                i += 1

    def serialize_mod_pool(self):
        """
        Gives unique indices to each mod object and each topic in mod_pool (topic indices are unique across mods).
        """
        i = 0
        for j, mod in enumerate(self.plan_optim_state.mod_pool):
            mod.id = j
            for topic in mod.topics:
                topic.id = i
                i += 1

    def select_mod(self, selected_mod_idx : int) -> bool:
        """
        Moves the selected mod from mod_pool to selected_mods in plan_optim_state.
        Updates the max_sim_score_so_far for all jobs based on the selected mod.
        Note: doesnt not decide which mod to select; the selected mod is passed into this function

        Args:
            selected_mod_idx (int): Index of the selected mod in mod_pool.

        Returns:
            boolean: True if successfully performed required operations, False otherwise (eg if full)
        """

        if self.is_full():
            return False
        selected_mod = self.plan_optim_state.mod_pool.pop(selected_mod_idx)
        self.update_max_sim_so_far(selected_mod)
        self.plan_optim_state.selected_mods.append(selected_mod)
        return True
    
    def update_max_sim_so_far(self, mod: Mod):
        """
        Updates max_sim_score_so_far for all jobs based on the selected mod.

        Args:
            mod (Mod): Mod based on which to updates max_sim_score_so_far
        """
        if self.build_sim_cache is None:
            self.build_sim_cache()
        for job in self.plan_optim_state.user_jobs:
            for i, skill in enumerate(job.skills):
                skill_mod_max_sim = 0.0
                for j, topic in enumerate(mod.topics):
                    if mod.id == -1:
                        sim = topic_skill_sim(topic=topic, skill=skill)
                    else:
                        assert job.id != -1 and topic.id != -1 and skill.id != -1, f"Expected job.id, topic.id, skill.id to all NOT be -1 (un-init), got {job.id=}, {topic.id=}, {skill.id=}"
                        sim_matrix = self.sim_cache[mod.id][job.id]
                        sim = sim_matrix[j][i]
                    
                    if sim > skill_mod_max_sim:
                        skill_mod_max_sim = sim
                if skill_mod_max_sim > skill.max_sim_score_so_far:
                    skill.max_sim_score_so_far = skill_mod_max_sim

    def is_full(self):
        return len(self.plan_optim_state.selected_mods) == self.selection_capacity
    
    def is_bucket_empty(self):
        return len(self.plan_optim_state.mod_pool) == 0
    

    # def get_mod_score(self, mod: Mod) -> float:
    #     if self.sim_score_matrix is None:
    #         self.build_sim_score_matrix()
    #     idx = self.mod_id_sim_matrix_map[mod.id]
    #     return self.sim_score_matrix[idx]

    # def build_sim_score_matrix(self):
    #     self.sim_score_matrix = []
    #     for mod in self.plan_optim_state.mod_pool:
    #         self.mod_id_sim_matrix_map[mod.id] = self.mod_map_next_idx
    #         self.mod_map_next_idx += 1
    #         self.sim_score_matrix.append(Job_list_Mod_sim(jobs=self.plan_optim_state.user_jobs, mod=mod, selection_sim_threshold=self.selection_sim_threshold))
    
