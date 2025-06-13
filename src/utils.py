import json
import re
def load_jsonl(file_path):
    data = []
    with open(file_path, 'r') as f:
        for line in f.readlines():
            data.append(json.loads(line.strip()))
    return data


def extract_dictionary_from_string(s):
    # extract the strings between "```json" and "```"
    pattern = r'```json(.*)```'
    match = re.search(pattern, s)
    if match:
        return match.group(1).strip()
    else:
        return None


# TODO: implement the model call yourself
def call_model(system_prompt, user_prompt):
    pass


# TODO: implement the token counting yourself
def cnt_tokens(text):
    pass