from dataclasses import dataclass
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

@dataclass
class MyConfig:
    MODS_FILE_PATH: Path = PROJECT_ROOT / "data" / "mods" / "mods.json"
    JOBS_FILE_PATH: Path = PROJECT_ROOT / "data" / "jobs" / "jobs.json"

    selection_capacity: int = 4
    softmax_temperature: float = 10
    selection_ambiguity_threshold: float = 0.10
    selection_sim_threshold: float = 0.60
    ambiguity_agent_active: bool = False

    target_job_weight: float = 1.0
    dream_job_weight: float = 0.7
    backup_job_weight: float = 0.3

my_config = MyConfig()