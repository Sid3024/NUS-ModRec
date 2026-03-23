import json
from src.types.domain import Mod
def parse_response(response: str, selected_mods: list[Mod]) -> tuple[bool, list[Mod]]:
    pass



def global_validator(response: str, selected_mods: list[Mod]) -> tuple[bool, str]:
    """
    Validates that response is a valid json and is a list with at least 1 valid dictionary of the expected format.
    """
    try:
        json_resp = json.loads(response)
    except json.JSONDecodeError:
        return False, "Response is not a valid json"
    if not isinstance(json_resp, list):
        return False, "LLM response of incorrect format, parsed output is a valid json but not a valid list."
    mod_title_list = [mod.title for mod in selected_mods]
    mod_code_list = [mod_title[0:5] for mod_title in mod_title_list]
    for dictionary in json_resp:
        if isinstance(dictionary, dict) and "title" in dictionary.keys() and "reasoning" in dictionary.keys() and dictionary["reasoning"].strip() != "" and dictionary["title"][0:5] in mod_code_list:
            return True, "" #at least one valid dict entry in response
    return False, "Response is a valid json and list but does not contain any dictionaries of the expected format."
                
    
def local_validator(response: str, selected_mods: list[Mod]) -> tuple[bool, list[dict], list[Mod], str]:
    """
    Checks that the llm output dict for each mod is of the correct format, and returns the dicts that are and the titles that are not (for reprompting)

    Args:
        response (str): The llm response.
        selected_mods (list[Mod]): list of mods selected by the alg the llm is generating explanations for.

    Returns:
        tuple[bool, list[dict], list[Mod], str]:
            bool: True if no local error (ie all selected mods have their valid dict in returned list[dict]), else False
            list[dict]: The list of valid dictionaries containing mod title and reasoning. 
            list[Mod]: The list of mods for which valid dicts were not returned.
            str: The error_msg, if no error then error_msg is None.

    Notes:
        - Assumes input response str is of correct format (no global errors)
    """
    json_resp = json.loads(response)
    if not isinstance(json_resp, list):
        return False, "LLM response of incorrect format, parsed output is a valid json but not a valid list."
    
    mod_title_list = [mod.title for mod in selected_mods]
    mod_code_list = [mod_title[0:5] for mod_title in mod_title_list]

    valid_dict_list = []
    mods_titles_with_valid_dict = []
    error_msg = None
    for dictionary in json_resp:
        if not isinstance(dictionary, dict) or "title" not in dictionary.keys() or "reasoning" not in dictionary.keys() or dictionary["reasoning"].strip() == "" or dictionary["title"][0:5] not in mod_code_list:
            if error_msg is None:
                error_msg = "LLM response of incorrect format, parsed output contains at least one element that is not a dictionary of the expected format"
        else:
            valid_dict_list.append(dictionary)
            mods_titles_with_valid_dict.append(dictionary["title"])

    mods_without_valid_dict = []

    if len(mods_titles_with_valid_dict) == len(selected_mods):
        for mod in selected_mods:
            if mod.title not in mods_titles_with_valid_dict:
                mods_without_valid_dict.append(mod)
    
    success = (len(valid_dict_list) == len(selected_mods))
    return success, valid_dict_list, mods_without_valid_dict, error_msg


    