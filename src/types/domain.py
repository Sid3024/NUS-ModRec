import numpy as np
from dataclasses import dataclass, field

@dataclass
class TextBlock:
    text: str
    embd: np.ndarray

@dataclass
class Skill:
    content: TextBlock
    weight: float = 1.0
    max_sim_score_so_far: float = 0.0

@dataclass
class Job:
    title: str
    type: str = ""
    weight: float = 0.0
    skills: list[Skill] = field(default_factory=list)

    def to_prompt_str(self) -> str:
        skills_str = ", ".join(skill.content.text for skill in self.skills)  

        return (
            f"Job: {self.title}\n"
            f"Skills: {skills_str}\n"
        )

@dataclass
class Topic:
    content: TextBlock
    weight: float = 1.0
    score: float = 0.0

@dataclass
class Mod:
    title: str
    desc: TextBlock
    topics: list[Topic] = field(default_factory=list)

    def __iter__(self):
        return iter(self.topics)
    
    def to_prompt_str(self) -> str:
        topics_str = ", ".join(topic.content.text for topic in self.topics)

        return (
            f"Module: {self.title}\n"
            f"Topics: {topics_str}\n"
        )

@dataclass
class Student:
    major: str    
    desc: str
    my_jobs: list[Job] = field(default_factory=list)

@dataclass
class ModType:
    type: str

