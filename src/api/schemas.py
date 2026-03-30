from pydantic import BaseModel
from typing import Literal


class JobInput(BaseModel):
    title: str
    type: Literal["target", "dream", "backup"]


class RecommendRequest(BaseModel):
    major: str
    jobs: list[JobInput]
