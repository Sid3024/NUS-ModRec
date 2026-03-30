import numpy as np
from numpy.typing import NDArray
from src.custom_types.domain import TextBlock, Skill, Topic, Job, Mod

def Job_list_Mod_sim_using_cache(
    jobs: list[Job],
    mod: Mod,
    sim_cache: list[list[NDArray[np.float64]]],
    selection_sim_threshold: float
) -> float:
    """
    Compute the total similarity score between a module and a list of jobs
    using precomputed similarity matrices.

    For each job, this function retrieves the corresponding topic–skill
    similarity matrix from `sim_cache` and computes the module–job score
    via `Job_Mod_sim`. The final score is the sum of these individual scores.

    Args:
        jobs (list[Job]): List of target jobs.
        mod (Mod): Module whose relevance is being evaluated.
        sim_cache (list[list[NDArray[np.float64]]]): Precomputed similarity cache
            where sim_cache[mod.id][job.id] is a 2D matrix of shape
            (len(mod.topics), len(job.skills)), containing cosine similarities
            between each topic–skill pair.
        selection_sim_threshold (float): Threshold used in the scoring function
            to control diminishing returns for similarity gains.

    Returns:
        float: Total aggregated similarity score between the module and all jobs.

    Raises:
        IndexError: If mod.id or job.id are out of bounds for `sim_cache`.

    Notes:
        - This function avoids recomputing topic–skill similarities by using
          cached matrices, significantly improving performance during
          greedy selection.
        - Each job contributes independently via `Job_Mod_sim`, and job weights
          are applied within that function.
        - Assumes `sim_cache` is correctly populated and aligned with mod/job IDs.
    """
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

def Job_Mod_sim(
    job: Job,
    mod: Mod,
    job_mod_sim_matrix: list[list[float]],
    selection_sim_threshold: float
) -> float:
    """
    Compute the similarity score between a module and a single job.

    The score aggregates contributions from all topic–skill pairs between the
    module and the job. Each contribution is based on a precomputed similarity
    value and adjusted using a diminishing returns scoring function to avoid
    overcounting already-covered skills.

    Args:
        job (Job): Target job containing a list of required skills.
        mod (Mod): Module containing a list of topics.
        job_mod_sim_matrix (list[list[float]]): Precomputed matrix where
            entry [i][j] represents the similarity between mod.topics[i]
            and job.skills[j].
        selection_sim_threshold (float): Threshold used in the scoring function
            to control diminishing returns for similarity gains.

    Returns:
        float: Weighted similarity score between the module and the job.

    Notes:
        - Uses `scoring_func` to compute diminished gain based on:
            - Current similarity (`sim`)
            - Maximum similarity already achieved for the skill
              (`skill.max_sim_score_so_far`)
        - This encourages coverage of new skills rather than redundant overlap.
        - The final score is scaled by `job.weight`.
        - Assumes `job_mod_sim_matrix` is correctly aligned with
          `mod.topics` and `job.skills` indices.
    """
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

def topic_skill_sim(topic: Topic, skill: Skill) -> float:
    """
    Compute the weighted similarity between a topic and a skill.

    The similarity is calculated as the cosine similarity between the
    embeddings of the topic and the skill, scaled by their respective weights:

        sim = cosine_sim(topic.embedding, skill.embedding)
              * topic.weight * skill.weight

    Args:
        topic (Topic): Topic object containing embedding and importance weight.
        skill (Skill): Skill object containing embedding and importance weight.

    Returns:
        float: Weighted similarity score between the topic and the skill.

    Raises:
        ValueError: Propagated from `cosine_sim` if embeddings have mismatched
        shapes or zero magnitude.

    Notes:
        - Assumes both topic and skill embeddings are valid numpy arrays.
        - Weighting allows prioritization of more important topics/skills in
          downstream aggregation (e.g., job-mod similarity scoring).
        - If embeddings are pre-normalized, cosine similarity reduces to a
          dot product.
    """
    return cosine_sim(topic.content.embd, skill.content.embd) * topic.weight * skill.weight

def cosine_sim(x: np.ndarray, y: np.ndarray) -> float:
    """
    Compute the cosine similarity between two vectors.

    Args:
        x (np.ndarray): First vector.
        y (np.ndarray): Second vector.

    Returns:
        float: Cosine similarity between x and y.

    Raises:
        ValueError: If shapes do not match or if either vector has zero norm.
    """
    if x.shape != y.shape:
        raise ValueError("x and y must have the same shape")

    norm_x = np.linalg.norm(x)
    norm_y = np.linalg.norm(y)

    if norm_x == 0 or norm_y == 0:
        raise ValueError("Cosine similarity is undefined for zero vectors")

    return float(np.dot(x, y) / (norm_x * norm_y))

def scoring_func(sim: float, max_sim_so_far: float, selection_sim_threshold: float) -> float:
    if sim < selection_sim_threshold:
        return 0.0
    else:
        return max(0.0, sim - max_sim_so_far)
