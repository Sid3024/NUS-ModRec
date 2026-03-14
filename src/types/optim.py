from dataclasses import dataclass, field
import numpy as np
from src.types.domain import Job, Mod

@dataclass
class PlanOptimState:
    target_jobs: list[Job] = field(default_factory=list)
    mod_pool: list[Mod] = field(default_factory=list)
    selected_mods: list[Mod] = field(default_factory=list)
    

#     def iter_jobs(self):
#         return iter(self.target_jobs)

#     def iter_mods(self):
#         return iter(self.mod_pool)
    
# @dataclass
# class SelectedMods:
#     mods: list[Mod] = field(default_factory=list)
#     capacity: int = 2
#     size: int = 0

#     def append(self, mod : Mod):
#         self.mods.append(mod)
#         self.size += 1

#     def __len__(self):
#         return len(self.mods)

#     def is_full(self):
#         return len(self) == self.capacity
