import os
import argparse
from builtins import range
import json
import glob
import re
import multiprocessing
from functools import partial
from tqdm import tqdm
from utils import load_jsonl, call_model, extract_dictionary_from_string
from prompts import PROMPT_SCORING_SYSTEM, PROMPT_SCORING_USER


def run(data_tuple, output_path):
    pid = data_tuple[0]
    local_data = data_tuple[1]
   
    for i in range(len(local_data)):

        item = local_data[i]
            
        # scoring
        prompt = item['prompt']
        res = {
            'id': item['id'],
            'message': [
                {'role': 'user', 'content': prompt}
            ]
        }
        system_prompt = PROMPT_SCORING_SYSTEM
        user_prompt = PROMPT_SCORING_USER.format(prompt=prompt)
        
        # score the prompt
        scores_dict = None
        retries, max_retries = 0, 3
        while not scores_dict and retries < max_retries:
            retries += 1
            try:
                response = call_model(system_prompt, user_prompt)
                scores_dict = json.loads(extract_dictionary_from_string(response))
                break
            except Exception as e:
                continue
        
        # calculate the total score
        if scores_dict:
            res[f'prompt_scores'] = scores_dict
            prompt_total_score = 0
            for k, v in scores_dict.items():
                if int(v['score']) >= 1:
                    prompt_total_score += 1
            res[f'prompt_total_score'] = prompt_total_score
        # if the prompt is not scored, skip the rest of the process
        else:
            continue
        
        # write files per pid, preventing writing conflicts
        print(f"{pid}>>>>>>>>>> requested {i}-th sample <<<<<<<<<<")
        with open(f'{output_path}/{pid}.jsonl', "a+", encoding="utf-8") as f:
            f.write(json.dumps(res, ensure_ascii=False) + "\n")
  

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--input_path', type=str, required=True)
    parser.add_argument('--output_path', type=str, required=True)
    parser.add_argument('--n_total_process', type=int, required=False, default=40)
    args = parser.parse_args()

    all_data = load_jsonl(args.input_path)
    output_dir = args.output

    # grab all generated data and remove them from the original data
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    all_files = glob.glob(f'{output_dir}/*.jsonl')
    id_generated = []
    for _path in tqdm(all_files, desc='loading generated ids'):
        id_generated += [d['id'] for d in load_jsonl(_path)]
    id_generated = set(id_generated)

    data_to_process = [d for d in all_data if d['id'] not in id_generated]
    print(f'to process {len(data_to_process)} data')

    splited_data = [(i, []) for i in range(args.n_total_process)]
    for i in range(len(data_to_process)):
        splited_data[i%args.n_total_process][1].append(
            data_to_process[i]
        )

    partial_run = partial(run, output_path=args.output_path)
    with multiprocessing.Pool(processes=args.n_total_process) as pool:
        results = pool.map(partial_run, splited_data)

    print(f'>>>>>>>>>>>>finished {args.file}<<<<<<<<<<<<<')