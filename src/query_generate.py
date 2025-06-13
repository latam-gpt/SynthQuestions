import os
import argparse
import json
import random
import glob
import multiprocessing
from tqdm import tqdm
from functools import partial
from utils import load_jsonl, call_model, extract_dictionary_from_string, cnt_tokens
from prompts import QUERY_GENERATION_SYSTEM, QUERY_GENERATION_USER_TEMPLATE


def run(data_tuple, demonstration_pools, output_path, document_length_limit):
    pid = data_tuple[0]
    local_data = data_tuple[1]

    for i in range(len(local_data)):

        item = local_data[i]
        res = {}
        demos = random.sample(demonstration_pools, 10)
        text = item['document']
        if cnt_tokens(text) > document_length_limit:
            text = text[:document_length_limit]

        user = QUERY_GENERATION_USER_TEMPLATE.format(document=text)
        user_len = cnt_tokens(user)

        demo_str = ''
        for demo in demos:
            _d = demo['grounding']['document']
            if len(_d) > document_length_limit:
                _d = _d[:document_length_limit]
            _s = demo['grounding']['scene']
            _q = demo['message'][0]['content']
            _qc = '\n'.join([f'{k}: {v}' for k, v in demo['grounding']["query_compositions"].items()])

            _demo_str = f'<document>\n{_d}\n</document>\n<scene>\n{_s}\n</scene>\n<query_compositions>\n{_qc}\n</query_compositions>\n<query>\n{_q}\n</query>\n\n'

            _full_len = cnt_tokens(QUERY_GENERATION_SYSTEM.format(demos=demo_str+_demo_str)) + user_len
            if _full_len < 7500:
                demo_str += _demo_str
            else:
                break
        
        system = QUERY_GENERATION_SYSTEM.format(demos=demo_str)

        # generate query
        max_retries, retries = 3, 0
        while 'message' not in res and retries < max_retries:
            retries += 1
            try:
                response = call_model(system, user)
                response_dict = extract_dictionary_from_string(response)
                response_dict = json.loads(response_dict)
                res['document'] = item['document']
                res['id'] = item['id']
                res['scene'] = response_dict['scene']
                res['query_compositions'] = response_dict['query_compositions']
                res['prompt'] = response_dict['query']

            except Exception as e:
                print(f"{pid}>>>>>>>>>>{repr(e)}")
        
        if 'prompt' not in res:
            continue

        
        print(f"{pid}>>>>>>>>>> requested {i}-th sample <<<<<<<<<<<<")
        with open(f'{output_path}/{pid}.jsonl', "a+", encoding="utf-8") as f:
            f.write(json.dumps(res, ensure_ascii=False) + "\n")
  

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--input_path', type=str, required=True)
    parser.add_argument('--demonstration_path', type=str, required=True)
    parser.add_argument('--output_path', type=str, required=True)
    parser.add_argument('--document_length_limit', type=int, required=False, default=4096)
    parser.add_argument('--n_total_process', type=int, required=False, default=40)
    args = parser.parse_args()

    all_data = load_jsonl(args.input_path)
    if not os.path.exists(args.output_path):
        os.mkdir(args.output_path)
    all_files = glob.glob(f'{args.output_path}/*.jsonl')

    id_generated = []
    for _path in tqdm(all_files, desc='loading generated ids'):
        id_generated += [d['id'] for d in load_jsonl(_path)]
    id_generated = set(id_generated)

    all_data = [d for d in all_data if d['id'] not in id_generated]
    demonstration_pools = load_jsonl(args.demonstration_path)
    
    print(f'to process {len(all_data)} data')

    splited_data = [(i, []) for i in range(args.n_total_process)]
    for i in range(len(all_data)):
        splited_data[i%args.n_total_process][1].append(
            all_data[i]
        )
    
    with multiprocessing.Pool(processes=args.n_total_process) as pool:
        partial_run = partial(run, demonstration_pools=demonstration_pools, output_path=args.output_path)
        results = pool.map(partial_run, splited_data)

    print(f'>>>>>>>>>>>>finished {args.input_path}<<<<<<<<<<<<<')