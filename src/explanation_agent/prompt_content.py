from src.types.domain import Job, Mod, Student
from src.explanation_agent.types import ValidMod
def get_system_prompt() -> str:
    system_prompt = (
        "You are an academic and career recommendation assistant.\n\n"
        "Your task is to explain why each already-selected NUS module is relevant "
        "for the student's chosen job goals.\n\n"
        "You must follow these rules:\n"
        "- Base your reasoning only on the information provided by the user\n"
        "- Do not invent module content, job skills, or benefits that are not supported by the input\n"
        "- Explain each module separately\n"
        "- Keep each explanation concise but specific\n"
        "- Avoid generic praise or vague statements\n"
        "- Avoid repeating the exact same reasoning across different modules unless necessary\n"
        "- Ensure the module title in the response exactly matches the provided module title\n"
        "- Return valid JSON only\n"
        "- Do not include markdown fences\n"
        "- Do not include any text before or after the JSON\n\n"
        "Return the response in this exact format:\n"
        "[\n"
        '  {"title": "<exact module title>", "reasoning": "<reasoning>"},\n'
        '  {"title": "<exact module title>", "reasoning": "<reasoning>"}\n'
        "]"
    )
    return system_prompt

def get_user_prompt(
    student: Student,
    selected_mods: list[Mod],
) -> str:
    jobs_str = "\n".join(job.to_prompt_str() for job in student.my_jobs)
    selected_mods_str = "\n".join(mod.to_prompt_str() for mod in selected_mods)
    user_prompt = (
        f"The student is targeting the following jobs:\n"
        f"{jobs_str}\n\n"
        f"The following modules have already been selected.\n"
        f"For each module, the title is followed immediately by its description and topics.\n\n"
        f"{selected_mods_str}\n\n"
        f"Task:\n"
        f"For each selected module, explain why it was chosen for this student.\n\n"
        f"Guidelines:\n"
        f"- Connect the module content to the student's target jobs\n"
        f"- Use the module description and topics as the main evidence\n"
        f"- Focus on practical relevance to the job goals\n"
        f"- Make each module's reasoning distinct where possible\n"
        f"- Keep each explanation to about 2 to 4 sentences\n\n"
        f"Return valid JSON only in the required format."
    )
    return user_prompt

def get_user_reprompt_global_error(
    student: Student,
    selected_mods: list[Mod],
    error_msg: str,
) -> str:
    jobs_str = "\n".join(job.to_prompt_str() for job in student.my_jobs)

    selected_mods_str = "\n\n".join(
        mod.to_prompt_str()
        for mod in selected_mods
        if mod is not None
    )

    selected_titles_str = "\n".join(
        f"- {mod.title}"
        for mod in selected_mods
        if mod is not None
    )

    return (
        f"The student is targeting the following jobs:\n"
        f"{jobs_str}\n\n"
        f"The previous response was invalid.\n"
        f"Reason: {error_msg}\n\n"
        f"The following modules have already been selected.\n"
        f"For each module, the title is followed immediately by its description and topics.\n\n"
        f"{selected_mods_str}\n\n"
        f"Task:\n"
        f"Regenerate explanations for ALL selected modules.\n\n"
        f"Requirements (must follow strictly):\n"
        f"- Return ONLY valid JSON\n"
        f"- Do NOT include markdown fences\n"
        f"- Do NOT include any text before or after the JSON\n"
        f"- Return a JSON list\n"
        f"- Each item must have exactly these fields:\n"
        f'  {{"title": "<exact module title>", "reasoning": "<non-empty reasoning>"}}\n'
        f"- Module titles must EXACTLY match the following:\n"
        f"{selected_titles_str}\n"
        f"- Return exactly one entry for each module above and no extra entries\n"
        f"- Explain each module separately\n"
        f"- Reasoning must be concise (2 to 4 sentences)\n"
        f"- Reasoning must be based only on the provided module info and the student's target jobs\n"
        f"- Do not invent module content, job skills, or benefits not supported by the input\n"
        f"- Do not repeat identical reasoning across modules"
    )

def get_user_reprompt_local_error(
    student: Student,
    valid_mods: list[dict[str, str]],
    invalid_mods: list[Mod],
) -> str:
    
    jobs_str = "\n".join(job.to_prompt_str() for job in student.my_jobs)
    valid_mods_str = "\n\n".join(
        f"title: {vm['title']}\n"
        f"reasoning: {vm['reasoning']}"
        for vm in valid_mods
        if vm["title"] is not None and vm["reasoning"] is not None
    )

    invalid_mods_str = "\n\n".join(
        im.to_prompt_str()
        for im in invalid_mods
        if im is not None
    )

    invalid_titles_str = "\n".join(
        f"- {im.mod.title}"
        for im in invalid_mods
        if im.mod is not None
    )

    return (
        f"The student is targeting the following jobs:\n"
        f"{jobs_str}\n\n"
        f"The previous response was partially invalid.\n\n"
        f"The following module explanations are already valid. "
        f"Do NOT change or regenerate them:\n"
        f"{valid_mods_str if valid_mods_str else 'None'}\n\n"
        f"The following modules need new explanations because they did not match the required format:\n\n"
        f"{invalid_mods_str}\n\n"
        f"Task:\n"
        f"Regenerate explanations ONLY for the modules listed above.\n\n"
        f"Requirements (must follow strictly):\n"
        f"- Return ONLY valid JSON\n"
        f"- Do NOT include markdown fences\n"
        f"- Do NOT include any text before or after the JSON\n"
        f"- Return a JSON list\n"
        f"- Each item must have exactly these fields:\n"
        f'  {{"title": "<exact module title>", "reasoning": "<non-empty reasoning>"}}\n'
        f"- Module titles must EXACTLY match the following:\n"
        f"{invalid_titles_str}\n"
        f"- Return one entry per module above and no extra entries\n"
        f"- Reasoning must be concise (2–4 sentences) and based only on provided module info\n"
        f"- Do not repeat identical reasoning across modules"
    )
