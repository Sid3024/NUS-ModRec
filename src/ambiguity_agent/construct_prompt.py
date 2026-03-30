from src.custom_types.domain import Job, Mod, Student, ModType
from src.ambiguity_agent.prompt_content import system_prompt, user_prompt, user_reprompt

def construct_agent_reprompt_dict(initial_prompt_messages: list[dict], llm_initial_response: str, error_msg: str, max_valid_index: int) -> list[dict]:
    """
    Constructs messages dict for the re-prompt to agent.

    Args:
        initial_prompt_messages (list[dict]): messages dict from the initial llm call.
        llm_initial_response (str): llm response to the initial api call.
        error_msg (str): Error message describing the error in initial llm response, for constructing the reprompt message.
        max_valid_index (int): To explicitly remind the llm of the allowed response index range to reduce chance of another erroneous response.

    Returns:
        list[dict]: messages parameter to pass into llm api call for reprompt.
    """

    additional_messages = [
        {"role": "assistant", "content": llm_initial_response},
        {"role": "user", "content": user_reprompt(error_msg=error_msg, max_valid_index=max_valid_index)},
    ]
    new_messages = initial_prompt_messages + additional_messages
    return new_messages

def construct_agent_initial_prompt_dict(student: Student, mod_type: ModType, candidate_mods: list[Mod], already_selected_mods: list[Mod]) -> list[dict]:
    """
    Constructs messages dict for the initial prompt to agent.

    Args:
        student (Student): student agent is optimising for.
        mod_type (ModType): Type of mod agent is selecting.
        candidate_mods (list[Mod]): Pool of mods from which agent can choose. 
        (Note: different from mod_pool, which is the entire pool of mods to select from in each step. 
        candidate_mods is a subset of mod_pool that is shown to the agent.)
        already_selected_mods (list[Mod]): List of mods that were already chosen.

    Returns:
        list[dict]: messages parameter to pass into llm api call for initial prompt.
    """

    messages = [
        {"role": "system", "content": system_prompt()},
        {"role": "user", "content": user_prompt(
                student=student,
                mod_type=mod_type,
                candidate_mods=candidate_mods,
                already_selected_mods=already_selected_mods
            )
        }
    ]
    return messages
