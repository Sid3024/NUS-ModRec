from src.types.domain import Job, Mod, Student, ModType

def system_prompt() -> str:
    """
    Generates the system prompt for ambiguity agent prompting.

    Returns:
        str: System prompt.
    """
    return (
        "You are an AI assistant that helps choose the best university module "
        "from a candidate list for a student.\n\n"
        "You must base your choice only on the information provided in the user message.\n\n"
        "You MUST follow these rules strictly:\n"
        "1. Output MUST be valid JSON.\n"
        "2. The JSON must contain EXACTLY these fields:\n"
        '   - "module_title": string\n'
        '   - "index": integer\n'
        '   - "reasoning": string\n'
        '3. The "index" must be a valid index from the provided candidate module list.\n'
        '4. The "module_title" must EXACTLY match the title of the module at that index.\n'
        "5. Do NOT output any extra text outside the JSON.\n"
        "6. The reasoning should be concise and refer only to the provided student and module information.\n"
        "7. If multiple modules seem similarly suitable, choose the single best one using the provided context."
    )

def user_prompt(
    student: Student,
    mod_type: ModType,
    candidate_mods: list[Mod],
    already_selected_mods: list[Mod]
) -> str:
    """
    Constructs the user prompt for the LLM module selection agent.

    The prompt includes:
    - Student profile (major, context)
    - Target jobs with priority (target/dream/backup)
    - Candidate module pool
    - Already selected modules (to avoid redundancy)

    The LLM is instructed to select the single best next module.

    Args:
        student: Student agent is optimising for.
        mod_type: type of mod agent is selecting.
        user_jobs (list[Job]): Jobs the user has chosen.
        candidate_mods (list[Mod]): Pool of mods for the agent to select from.
        already_selected_mods (list[Mod]): List of mods already selected for the user to take.

    Returns:
        str: User prompt.
    """
    
    
    jobs_str = "\n".join(job.to_prompt_str() for job in student.my_jobs)
    candidate_mods_str = "\n".join(mod.to_prompt_str() for mod in candidate_mods)

    if already_selected_mods:
        selected_mods_str = "\n".join(
            mod.to_prompt_str() for mod in already_selected_mods
        )
    else:
        selected_mods_str = "- None"

    return (
        "Student profile:\n"
        "- University: NUS\n"
        f"- Major: {student.major}\n"
        f"- Student description: {student.desc}\n"
        "- Goal: choose the single best next module\n\n"

        f"The module type we are looking to select is {mod_type.type}\n\n"
        f"{mod_type.type}\n"

        "Selected jobs:\n"
        f"{jobs_str}\n\n"

        "Job importance:\n"
        "- Target jobs are the highest priority and should influence the decision most strongly.\n"
        "- Dream jobs are the next priority and should be used to refine the decision.\n"
        "- Backup jobs are the lowest priority and should only have a small influence.\n\n"

        "Already selected modules:\n"
        f"{selected_mods_str}\n\n"

        "Significance of already selected modules:\n"
        "- These modules have already been chosen by the student.\n"
        "- You should consider what skills and topics they already cover.\n"
        "- Prefer a candidate module that adds important new value, fills gaps, or complements the already selected modules well.\n"
        "- If a candidate module overlaps heavily with already selected modules, that reduces its value unless that overlap is especially valuable for the student's highest-priority jobs.\n\n"

        "Candidate modules:\n"
        f"{candidate_mods_str}\n\n"

        "Task:\n"
        "Select the single best candidate module for this student.\n\n"

        "How to choose:\n"
        "- Prioritize alignment with target jobs first.\n"
        "- Then consider alignment with dream jobs.\n"
        "- Only lightly consider backup jobs.\n"
        "- Consider both direct relevance to the selected jobs and how well the module complements the already selected modules.\n"
        "- If multiple candidates seem similarly good, prefer the one that provides broader or more important additional coverage.\n\n"

        "Required JSON fields:\n"
        '- "module_title": the exact title of the chosen candidate module.\n'
        '- "index": the exact index of the chosen candidate module from the candidate module list.\n'
        '- "reasoning": a concise and user-presentable summary of why this module was chosen. '
        "It should mention the most important reasons, including job alignment, how it complements the already selected modules, "
        "and why it is stronger than the other candidate modules.\n\n"

        "The reasoning should be short, clear, and suitable to show directly to the student.\n\n"

        "Return the result in the required JSON format."
    )

def user_reprompt(error_msg: str, max_valid_index: int) -> str:
    return (
        "Your previous response was invalid.\n\n"
        f"Error: {error_msg}\n\n"
        "Please try again and follow the required format exactly.\n\n"
        "Return ONLY valid JSON with EXACTLY these fields:\n"
        '- "module_title": string\n'
        '- "index": integer\n'
        '- "reasoning": string\n\n'
        "All the above mentioned fields must be present and their values must not be None"
        'The "index" must be a valid index from the candidate module list.\n'
        'The "module_title" must EXACTLY match the title of the module at that index.\n'
        'The "reasoning" must be concise, clear, and user-presentable. It must not be empty\n\n'
        "Do not include any text outside the JSON."
    )