import numpy as np

from src.types.domain import TextBlock, Skill, Topic, Job, Mod

def Job_list_Mod_sim(jobs: list[Job], mod: Mod, selection_sim_threshold: float) -> float:
    score = 0.0
    for job in jobs:
        score += Job_Mod_sim(
            job=job, 
            mod=mod, 
            selection_sim_threshold=selection_sim_threshold
        )
    return score

def Job_Mod_sim(job: Job, mod: Mod, selection_sim_threshold: float) -> float:
    score = 0.0
    for topic in mod.topics:
        for skill in job.skills:
            sim = topic_skill_sim(topic=topic, skill=skill)
            diminished_gain = scoring_func(
                sim=sim,
                max_sim_so_far=skill.max_sim_score_so_far,
                selection_sim_threshold=selection_sim_threshold
            )
            score += diminished_gain * job.weight
    return score

def topic_skill_sim(topic : Topic, skill : Skill) -> float:
    return cosine_sim(topic.content.embd, skill.content.embd) * topic.weight * skill.weight

def cosine_sim(x : np.ndarray, y : np.ndarray) -> float:
    return np.dot(x,y) / (np.linalg.norm(x) * np.linalg.norm(y))

def scoring_func(sim: float, max_sim_so_far: float, selection_sim_threshold: float) -> float:
    if sim < selection_sim_threshold:
        return 0.0
    else:
        return max(0.0, sim - max_sim_so_far)