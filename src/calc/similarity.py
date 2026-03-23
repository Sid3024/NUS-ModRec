import numpy as np
from numpy.typing import NDArray
from src.types.domain import TextBlock, Skill, Topic, Job, Mod

def Job_list_Mod_sim_using_cache(jobs: list[Job], mod: Mod, sim_cache: list[list[NDArray[np.float64]]], selection_sim_threshold: float) -> float:
    score = 0.0
    for job in jobs:
        score += Job_Mod_sim(
            job=job, 
            mod=mod, 
            job_mod_sim_matrix=sim_cache[mod.id][job.id],
            selection_sim_threshold=selection_sim_threshold
        )
    return score

def Job_list_Mod_sim(jobs: list[Job], mod: Mod, selection_sim_threshold: float) -> float:
    score = 0.0
    for job in jobs:
        score += Job_Mod_sim(
            job=job, 
            mod=mod, 
            selection_sim_threshold=selection_sim_threshold
        )
    return score

def Job_Mod_sim(job: Job, mod: Mod, job_mod_sim_matrix: list[list[float]], selection_sim_threshold: float) -> float:
    score = 0.0
    for i, topic in enumerate(mod.topics):
        for j, skill in enumerate(job.skills):
            #sim = topic_skill_sim(topic=topic, skill=skill)
            sim = job_mod_sim_matrix[i][j]
            diminished_gain = scoring_func(
                sim=sim,
                max_sim_so_far=skill.max_sim_score_so_far,
                selection_sim_threshold=selection_sim_threshold
            )
            score += diminished_gain * job.weight
    return score

def build_job_mod_sim_matrix(job: Job, mod: Mod) -> NDArray[np.float64]:
    sim_matrix = np.zeros((len(mod), len(job)))
    for i, topic in enumerate(mod.topics):
        for j, skill in enumerate(job.skills):
            sim_matrix[i][j] = topic_skill_sim(topic=topic, skill=skill)
    return sim_matrix

def topic_skill_sim(topic : Topic, skill : Skill) -> float:
    return cosine_sim(topic.content.embd, skill.content.embd) * topic.weight * skill.weight

def cosine_sim(x : np.ndarray, y : np.ndarray) -> float:
    return np.dot(x,y) / (np.linalg.norm(x) * np.linalg.norm(y))

def scoring_func(sim: float, max_sim_so_far: float, selection_sim_threshold: float) -> float:
    if sim < selection_sim_threshold:
        return 0.0
    else:
        return max(0.0, sim - max_sim_so_far)