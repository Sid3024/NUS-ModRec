from __future__ import annotations

import logging
import time
import uuid
from datetime import datetime, timezone
from typing import Any

from src.config.config import my_config
from src.data_io.load import load_jobs, load_mods
from src.data_io.construct import construct_student
from src.custom_types.domain import ModType
from src.alg.greedy_basic import greedy_basic_selection
from src.explanation_agent.agent import run_explanation_agent
from src.recommendation_audit import log_recommendation_event

logger = logging.getLogger(__name__)


def generate_recommendations(
    user_major: str,
    user_jobs: list[dict[str, Any]],
    session_id: str | None = None,
) -> list[dict[str, str]]:
    """
    Generates module recommendations and logs the event to SQLite.

    Args:
        user_major: User's selected major.
        user_jobs: List of dicts like:
            [
                {"title": "ML Engineer", "type": "target"},
                {"title": "Data Scientist", "type": "dream"},
            ]
        session_id: Anonymous frontend session ID for analytics.

    Returns:
        List of recommended modules in the form:
            [
                {
                    "title": "...",
                    "desc": "...",
                    "reasoning": "..."
                },
                ...
            ]
    """
    request_id = str(uuid.uuid4())
    start_time = time.perf_counter()

    logger.info(
        "generate_recommendations started | request_id=%s | session_id=%s | major=%s",
        request_id,
        session_id,
        user_major,
    )

    try:
        jobs = load_jobs(my_config.JOBS_FILE_PATH, major=user_major)
        mods = load_mods(my_config.MODS_FILE_PATH, major=user_major)

        student = construct_student(
            user_major=user_major,
            user_jobs_input=user_jobs,
            jobs=jobs,
            my_config=my_config,
        )

        mod_type = ModType(type="Technical Electives")
        user_chosen_mods: list[Any] = []

        selected_mods = greedy_basic_selection(
            mod_pool=mods,
            user_chosen_mods=user_chosen_mods,
            student=student,
            mod_type=mod_type,
            my_config=my_config,
        )

        success_received_all_reasoning, selected_mods_with_reasoning, error_msg = (
            run_explanation_agent(
                student=student,
                selected_mods=selected_mods,
            )
        )

        # Convert into frontend-friendly response format
        response_mods: list[dict[str, str]] = []

        # Build quick lookup from explanation agent output
        reasoning_by_title = {}
        if selected_mods_with_reasoning is not None:
            for mod_dict in selected_mods_with_reasoning:
                title = mod_dict.get("title")
                reasoning = mod_dict.get("reasoning", "")
                if title is not None:
                    reasoning_by_title[title] = reasoning

        if selected_mods is not None:
            for mod in selected_mods:
                response_mods.append(
                    {
                        "title": mod.title,
                        "desc": mod.desc.text if mod.desc is not None else "",
                        "reasoning": reasoning_by_title.get(mod.title, ""),
                    }
                )

        latency_ms = int((time.perf_counter() - start_time) * 1000)

        event = {
            "event": "recommendation_generated",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "request_id": request_id,
            "session_id": session_id,
            "major": user_major,
            "jobs": user_jobs,
            "recommended_mods": response_mods,
            "ambiguity_agent_used": False,  # update later if you track this
            "fallback_used": not success_received_all_reasoning,
            "latency_ms": latency_ms,
            "success": True,
            "error_message": error_msg,
        }
        log_recommendation_event(event)

        logger.info(
            "generate_recommendations success | request_id=%s | num_mods=%s | latency_ms=%s | explanation_success=%s | selected_mods=%s",
            request_id,
            len(response_mods),
            latency_ms,
            success_received_all_reasoning,
            [m["title"] for m in response_mods],
        )

        return response_mods

    except Exception as e:
        latency_ms = int((time.perf_counter() - start_time) * 1000)

        event = {
            "event": "recommendation_failed",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "request_id": request_id,
            "session_id": session_id,
            "major": user_major,
            "jobs": user_jobs,
            "recommended_mods": [],
            "ambiguity_agent_used": False,
            "fallback_used": False,
            "latency_ms": latency_ms,
            "success": False,
            "error_message": str(e),
        }
        log_recommendation_event(event)

        logger.exception(
            "generate_recommendations failed | request_id=%s | latency_ms=%s",
            request_id,
            latency_ms,
        )
        raise
