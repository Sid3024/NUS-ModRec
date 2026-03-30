from fastapi import APIRouter, HTTPException, Query

from src.api.schemas import RecommendRequest
from src.api.repository import get_all_majors, get_jobs_for_major
from src.api.recommender_service import generate_recommendations

router = APIRouter()


@router.get("/majors")
def get_majors():
    return {"majors": get_all_majors()}


@router.get("/jobs")
def get_jobs(major: str = Query(...)):
    jobs = get_jobs_for_major(major)

    if not jobs:
        raise HTTPException(status_code=404, detail=f"No jobs found for major '{major}'")

    return {"jobs": jobs}


@router.post("/recommend")
def recommend_modules(request: RecommendRequest):
    if not request.jobs:
        raise HTTPException(status_code=400, detail="At least one job must be provided")

    modules = generate_recommendations(
        user_major=request.major.strip(),
        user_jobs=[job.model_dump() for job in request.jobs],
    )

    return {"modules": modules}
