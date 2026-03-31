from src.explanation_agent.prompt_content import get_system_prompt, get_user_prompt, get_user_reprompt_global_error, get_user_reprompt_local_error
from src.types.domain import Mod, Student
from src.explanation_agent.response_validator import global_validator, local_validator



def construct_initial_prompt(student: Student, selected_mods: list[Mod]) -> str:
    messages = [
        {"role": "system", "content": get_system_prompt()},
        {"role": "user", "content": get_user_prompt(
                student=student,
                selected_mods=selected_mods
            )
        }
    ]
    return messages

def construct_reprompt_global_reprompt(student: Student, prev_messages: list[dict], prev_llm_resp: str, selected_mods: list[Mod], error_msg: str) -> str:
    llm_message = {"role": "assistant", "content": prev_llm_resp}
    new_user_message = {"role": "user", "content": get_user_reprompt_global_error(student=student, selected_mods=selected_mods, error_msg=error_msg)}
    messages = prev_messages + [llm_message, new_user_message]
    return messages

def construct_reprompt_local_reprompt(student: Student, prev_messages: list[dict], prev_llm_resp: str, valid_mods_dicts: list[dict], remaining_mods: list[Mod]) -> str:
    llm_message = {"role": "assistant", "content": prev_llm_resp}
    new_user_message = {"role": "user", "content": get_user_reprompt_local_error(student=student, valid_mods=valid_mods_dicts, invalid_mods=remaining_mods)}
    messages = prev_messages + [llm_message, new_user_message]
    return messages
