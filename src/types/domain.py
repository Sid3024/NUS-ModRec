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
    job_weight: float = 0.0
    skills: list[Skill] = field(default_factory=list)

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
