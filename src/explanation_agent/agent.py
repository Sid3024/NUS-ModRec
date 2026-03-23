
from src.llm.llm_client import call_llm
from src.explanation_agent.construct_prompt import construct_initial_prompt, construct_reprompt_global_reprompt, construct_reprompt_local_reprompt
from src.explanation_agent.response_validator import global_validator, local_validator
from src.types.domain import Student, Mod
from src.config.config import my_config
from copy import deepcopy

def run_explanation_agent(student: Student, selected_mods: list[Mod]) -> tuple[bool, list[dict], str]:
    messages = construct_initial_prompt(student=student, selected_mods=selected_mods)
    print(f"{messages=}")
    llm_response = call_llm(messages=messages)
    if my_config.explanation_agent_reprompt_limit == 0:
        valid_response, error_msg = global_validator(response=llm_response, selected_mods=selected_mods)
        if valid_response:
            success, valid_dict_list, mods_without_valid_dict, error_msg = local_validator(response=llm_response, selected_mods=selected_mods)
            if success:
                return True, valid_dict_list, None
            else:
                return False, None, error_msg
        else:
            return False, None, error_msg
    remaining_mods = deepcopy(selected_mods)
    valid_dict_list = None
    for count in range(my_config.explanation_agent_reprompt_limit):
        print(f"{count=}")
        valid_response, error_msg = global_validator(response=llm_response, selected_mods=selected_mods)
        print(f"{valid_response=}, {error_msg=}")
        if not valid_response:
            print(f"{llm_response=}")
            print(f"{messages is None}")
            messages = construct_reprompt_global_reprompt(
                student=student,
                prev_messages=messages,
                prev_llm_resp=llm_response,
                selected_mods=remaining_mods,
                error_msg=error_msg
            )
            llm_response = call_llm(messages=messages)
        else:
            success, valid_dict_list, mods_without_valid_dict, error_msg = local_validator(response=llm_response, selected_mods=selected_mods)
            if success:
                return True, valid_dict_list, None
            else:
                remaining_mods = mods_without_valid_dict
                messages = construct_reprompt_local_reprompt(
                    student=student,
                    prev_messages=messages,
                    prev_llm_resp=llm_response,
                    remaining_mods=remaining_mods
                )
                llm_response = call_llm(messages=messages)
    return False, valid_dict_list, error_msg