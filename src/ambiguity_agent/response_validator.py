import json
from src.types.domain import Mod

def validate_response(response: str, candidate_mods: list[Mod]) -> tuple[bool, str]:
    """
    Validates response and ensure it is of correct format by performing following checks:
    1) Reponse is a valid json object.
    2) All required fields title: str, index: int, reasoning: str, are present and of the correct type (including not None)
    3) index is within range
    4) Reasoning is not empty
    5) Title matches the title at Index of the candidate_mods list

    Args:
        response (str): raw LLM response
        candidate_mods (list[Mod]): pool of mods for agent to select from, required for checking title match and index range
    
    Returns:
        bool: True with empty string if response is of valid format (passes all checks), False with error msg otherwise
    """

    valid_json, error_msg = is_valid_json(response=response)
    if not valid_json:
        return False, error_msg
    
    valid_fields, error_msg = validate_field_formatting(response=response, max_valid_index=len(candidate_mods)-1)
    if not valid_fields:
        return False, error_msg
    
    title_match, error_msg = validate_title_match(response=response, candidate_mods=candidate_mods)
    if not title_match:
        return False, error_msg

    return True, ""
    

def is_valid_json(response: str) -> tuple[bool, str]:
    """
    validates that response is a valid json.
    """
    
    try:
        json.loads(response)
        return True, ""
    except json.JSONDecodeError:
        return False, "response is not a valid json"
    
def validate_field_formatting(response: str, max_valid_index: int) -> tuple[bool, str]:
    """
    Checks whether json fields are correctly formatted.
    Ensures fields exists, are of the correct type, and take on expected values (index within range and reasoning not empty)

    Args:
        response (str): response str to be validated
        max_valid_index (int): max index value allowed (corresponding to max index value of candidate_pool list)

    Returns:
        bool: True if correctly formatted, False otherwise
    """

    resp_dict = json.loads(response)
    required_fields = ["module_title", "index", "reasoning"]

    #check required fields exist
    for field in required_fields:
        if field not in resp_dict:
            return False, f"missing_{field}"
        
    module_title = resp_dict["module_title"]
    index = resp_dict["index"]    
    reasoning = resp_dict["reasoning"]
        
    #check field types are correct
    if not isinstance(module_title, str):
        return False, f"invalid_title_type, expected str, got {type(module_title)}"
    
    if not isinstance(index, int):
        return False, f"invalid_index_type, expected int, got {type(index)}"
    
    if not isinstance(reasoning, str):
        return False, f"invalid_reasoning_type, expected str, got {type(reasoning)}"
    
    #check index range
    if index < 0 or index > max_valid_index:
        return False, f"index OOR, expected 0 <= index <= {max_valid_index}, got {index=}"
    
    #check reasoning not null
    if reasoning.strip() == "":
        return False, "Reasoning is empty"
    
    return True, ""

def validate_title_match(response: str, candidate_mods: list[Mod]) -> tuple[bool, str]:
    """
    Checks that the module_title in llm response matches the module_title of the mod at the index specified by the llm of candidate_mods (llm response consistency check).

    Args:
        response (str): Raw llm output.
        candidate_mods (list[Mod]): list of mods that was input to llm and from which to reference the expected module_title at the llm specified index.

    Returns:
        bool: True if module_title matches expected module_title, False otherwise.
    """
    resp_dict = json.loads(response)
    module_title = resp_dict["module_title"].lower()
    index = resp_dict["index"]
    expected_title = candidate_mods[index].title.lower()
    if (module_title[0:5] == expected_title[0:5]): #soft check; only checks equality of module code ie first 6 chars, case-insensitive
        return True, ""
    else:
        return False, f"title from llm response ({module_title}) does not match expected title from candidate_mods ({expected_title})"
