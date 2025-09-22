import argparse
import json
import glob
import multiprocessing
from tqdm import tqdm
from functools import partial
from utils import load_jsonl
from web_search import web_search_by_keywords


def run(data_tuple, output_path):
    pid = data_tuple[0]
    local_data = data_tuple[1]

    for i in range(len(local_data)):
        item = local_data[i]
        keywords = item.get('keywords', [])

        if not keywords:
            print(f"{pid}>>>>>>>>>> No keywords found for item {i}, skipping <<<<<<<<<<<<<<")
            continue

        # Perform web search using keywords
        try:
            search_result = web_search_by_keywords(keywords)

            if search_result and search_result.get('fetched_content'):
                # Add only the fetched content to the document key
                item['document'] = search_result.get('fetched_content', '')
                print(f"{pid}>>>>>>>>>> Successfully found document for item {i} (score: {search_result.get('bm25_score', 0.0):.4f}) <<<<<<<<<<<<<<")
            else:
                print(f"{pid}>>>>>>>>>> No search results found for item {i} <<<<<<<<<<<<<<")
                item['document'] = None

        except Exception as e:
            print(f"{pid}>>>>>>>>>> Search failed for item {i}: {e} <<<<<<<<<<<<<<")
            item['document'] = None

        # Write the item with document information
        with open(f'{output_path}/{pid}.jsonl', "a+", encoding="utf-8") as f:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_file', type=str, required=True)
    parser.add_argument('--output_path', type=str, required=True)
    parser.add_argument('--n_total_process', type=int, required=False, default=4)  # Reduced default for web requests
    args = parser.parse_args()

    all_data = load_jsonl(args.input_file)

    # Check for already processed items
    all_files = glob.glob(f'{args.output_path}/*.jsonl')
    id_generated = []
    for _path in tqdm(all_files, desc='loading generated ids'):
        id_generated += [d['id'] for d in load_jsonl(_path)]

    all_data = [d for d in all_data if d['id'] not in id_generated]

    print(f'to process {len(all_data)} data')

    # Split data across processes
    splited_data = [(i, []) for i in range(args.n_total_process)]
    for i in range(len(all_data)):
        splited_data[i % args.n_total_process][1].append(all_data[i])

    # Run multiprocessing
    with multiprocessing.Pool(processes=args.n_total_process) as pool:
        partial_run = partial(run, output_path=args.output_path)
        results = pool.map(partial_run, splited_data)

    print(f'>>>>>>>>>>>>finished {args.input_file}<<<<<<<<<<<<<')