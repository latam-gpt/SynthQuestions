import json
import re
import torch
from transformers import pipeline, AutoTokenizer

MODEL_NAME = "Qwen/Qwen3-14B"

def load_jsonl(file_path):
    data = []
    with open(file_path, 'r') as f:
        for line in f.readlines():
            data.append(json.loads(line.strip()))
    return data


def extract_dictionary_from_string(s):
    # extract the strings between "```json" and "```
    dict_str = None
    try:
        dict_str = json.loads(s)
        return json.dumps(dict_str)
    except json.decoder.JSONDecodeError:
        pattern = r'```json(.*)```'
        match = re.search(pattern, s)
        if match:
            dict_str = match.group(1).strip()
    return dict_str


# Initialize the pipeline globally for efficiency
_pipeline = None
_tokenizer = None

def _get_pipeline():
    global _pipeline
    if _pipeline is None:
        _pipeline = pipeline(
            "text-generation",
            model=MODEL_NAME,
            torch_dtype=torch.bfloat16,
            trust_remote_code=True,
            device_map="auto"
        )
    return _pipeline

def _get_tokenizer():
    global _tokenizer
    if _tokenizer is None:
        _tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    return _tokenizer

def call_model(system_prompt, user_prompt):
    """Call the model using transformers pipeline for local inference."""
    text_generator = _get_pipeline()
    
    # Format the prompt using chat template
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]
    
    # Use the tokenizer to apply chat template
    tokenizer = _get_tokenizer()
    formatted_prompt = tokenizer.apply_chat_template(
        messages, 
        tokenize=False, 
        add_generation_prompt=True,
        enable_thinking=False,
    )
    
    # Generate response using the pipeline
    outputs = text_generator(
        formatted_prompt,
        max_new_tokens=2048,
        temperature=0.7,
        top_p=0.9,
        do_sample=True,
        pad_token_id=tokenizer.eos_token_id
    )
    
    # Extract the generated text (remove the input prompt from the output)
    generated_text = outputs[0]['generated_text'][len(formatted_prompt):].strip()
    
    return generated_text


def cnt_tokens(text):
    """Count the number of tokens in a text using the model's tokenizer."""
    tokenizer = _get_tokenizer()
    
    # Tokenize the text and return the number of tokens
    tokens = tokenizer.encode(text, add_special_tokens=False)
    return len(tokens)