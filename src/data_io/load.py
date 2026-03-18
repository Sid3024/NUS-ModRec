import numpy as np
from pathlib import Path
import json

from src.types.domain import Mod, Job, TextBlock, Skill, Topic

def load_mods(MODS_JSON_PATH : Path) -> list[Mod]:
    with open(MODS_JSON_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    mods = []
    for mod_dict in data:
        desc = TextBlock(
            text=mod_dict["description"]["description"],
            embd=np.array(mod_dict["description"]["embd"], dtype=float)
        )

        topics = []
        for topic_dict in mod_dict["topics covered"]:
            topic = Topic(
                content=TextBlock(
                    text=topic_dict["topics covered"],
                    embd=np.array(topic_dict["embd"], dtype=float)
                )
            )
            topics.append(topic)

        mod = Mod(
            title=mod_dict["module"],
            desc=desc,
            topics=topics
        )

        mods.append(mod)
    return mods

def load_jobs(JOBS_JSON_PATH : Path) -> list[Job]:
    with open(JOBS_JSON_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    jobs = []
    for job_dict in data:
        skills = []
        for skill_dict in job_dict["skills"]:
            content = TextBlock(
                text=skill_dict["skills"],
                embd=np.array(skill_dict["embd"], dtype=float)
            )
            skill = Skill(content=content)
            skills.append(skill)
        
        job = Job(
            title=job_dict["job"],
            skills=skills
        )

        jobs.append(job)
    return jobs
