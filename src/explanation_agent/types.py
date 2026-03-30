from src.custom_types.domain import Mod
from dataclasses import dataclass

@dataclass
class ValidMod:
    mod: Mod
    reasoning: str

    def get_expl_prompt_str(self) -> str:
        if self.mod is None or self.reasoning is None:
            return None
        return self.mod.get_prompt_str() + "\n" + self.reasoning


@dataclass
class InvalidMod:
    mod: Mod
    error_msg: str

    def get_expl_prompt_str(self) -> str:
        if self.mod is None or self.error_msg is None:
            return None
        return self.mod.get_prompt_str() + "\n" + self.error_msg

