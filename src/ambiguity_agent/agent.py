from src.types.domain import Job, Mod, Student, ModType
from src.ambiguity_agent.construct_prompt import construct_agent_initial_prompt_dict, construct_agent_reprompt_dict
from src.ambiguity_agent.response_validator import validate_response
from src.llm.llm_client import call_llm
import json

def run_ambiguity_agent(student: Student, mod_type: ModType, candidate_mods: list[Mod], already_selected_mods: list[Mod]) -> dict:
    """
    Runs the agent to select a mod from a list of candidate mod based on student attributes (major, desc, my_jobs) and mods that have already been selected.

    Args:
        student (Student): student object with required attributes for decision making (major, desc, my_jobs).
        mod_type (ModType): type of mod agent is selecting.
        candidate_mods (list[Mod]): list of mods from which the agent can select.
        already_selected_mods (list[Mod]): list of mods that have already been selected.

    Returns:
        dict: includes fields:
        title (str): title of the selected mod.
        index (int): index of the selected mod in the candidate_mods list (0-indexed).
        reasoning (str): reason for selecting the specific mod (free form text).
    """
    
    messages = construct_agent_initial_prompt_dict(
        student=student,
        mod_type=mod_type,
        candidate_mods=candidate_mods,
        already_selected_mods=already_selected_mods
    )
    raw_response = call_llm(messages=messages)
    response = clean_llm_response(response=raw_response)
    print(f"{response=}")
    valid, error_msg = validate_response(response=response, candidate_mods=candidate_mods)
    if valid:
        return json.loads(response)
    else:
        print("Agent's initial response was invalid")
        print(f"Error msg: {error_msg}")
        reprompt_messages = construct_agent_reprompt_dict(
            initial_prompt_messages=messages,
            llm_initial_response=response,
            error_msg=error_msg,
            max_valid_index=len(candidate_mods) - 1,
        )
        raw_reprompt_response = call_llm(messages=reprompt_messages)
        reprompt_response = clean_llm_response(response=raw_reprompt_response)
        print(f"{reprompt_response=}")
        valid, error_msg = validate_response(response=reprompt_response, candidate_mods=candidate_mods)
        if valid:
            return json.loads(response)
        else:
            print("Agent's reprompt response was invalid")
            print(f"Error msg: {error_msg}")
            return None
        
def clean_llm_response(response: str) -> str:
    response = response.strip()

    if response.startswith("```"):
        lines = response.splitlines()

        # remove first fence line
        lines = lines[1:]

        # remove last fence line if present
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]

        response = "\n".join(lines).strip()

    return response
            

