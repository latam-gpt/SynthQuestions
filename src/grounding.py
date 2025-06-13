import argparse
from builtins import range
import json
import glob
import multiprocessing
from tqdm import tqdm
from functools import partial
from utils import load_jsonl, call_model, extract_dictionary_from_string
from prompts import GROUNDING_SYSTEM, GROUNDING_USER_TEMPLATE


def run(data_tuple, output_path):
    pid = data_tuple[0]
    local_data = data_tuple[1]
    
    for i in range(len(local_data)):

        item = local_data[i]
        prompt = GROUNDING_USER_TEMPLATE.format(document=item['document'], query=item['prompt'])

        max_retries, retries = 3, 0
        while retries < max_retries:
            retries += 1
            try:
                response = call_model(GROUNDING_SYSTEM, prompt)
                response_dict = extract_dictionary_from_string(response)
                response_dict = json.loads(response_dict)
                item['grounding'] = {
                    'scene': response_dict['scene'],
                    'query_compositions': response_dict['query_compositions']
                }

            except Exception as e:
                print(f"{pid}>>>>>>>>>> {repr(e)}")
        
        if 'grounding' not in item:
            continue

        print(f"{pid}>>>>>>>>>> requested {i}-th sample <<<<<<<<<<<<<<")
        with open(f'{output_path}/{pid}.jsonl', "a+", encoding="utf-8") as f:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")
  

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--input_file', type=str, required=True)
    parser.add_argument('--output_path', type=str, required=True)
    parser.add_argument('--n_total_process', type=int, required=False, default=40)
    args = parser.parse_args()

    all_data = load_jsonl(args.input_file)

    all_files = glob.glob(f'{args.output_path}/*.jsonl')
    id_generated = []
    for _path in tqdm(all_files, desc='loading generated ids'):
        id_generated += [d['id'] for d in load_jsonl(_path)]

    all_data = [d for d in all_data if d['id'] not in id_generated]
    print(f'to process {len(all_data)} data')

    splited_data = [(i, []) for i in range(args.n_total_process)]
    for i in range(len(all_data)):
        splited_data[i%args.n_total_process][1].append(
            all_data[i]
        )

    with multiprocessing.Pool(processes=args.n_total_process) as pool:
        partial_run = partial(run, output_path=args.output_path)
        results = pool.map(partial_run, splited_data)

    print(f'>>>>>>>>>>>>finished {args.file}<<<<<<<<<<<<<')