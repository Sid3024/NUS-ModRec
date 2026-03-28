from dataclasses import dataclass, field
import numpy as np
from src.types.domain import Job, Mod

@dataclass
class PlanOptimState:
    user_jobs: list[Job] = field(default_factory=list)
    mod_pool: list[Mod] = field(default_factory=list)
    selected_mods: list[Mod] = field(default_factory=list)
    user_chosen_mods: list[Mod] = field(default_factory=list)
