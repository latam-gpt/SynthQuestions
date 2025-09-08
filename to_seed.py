#!/usr/bin/env python3

import json
import argparse
import os

def extract_seed_data(input_file):
    """
    Extract id and first user message from input file and create seed output file
    """
    # Generate output filename with "seed_" prefix
    input_dir = os.path.dirname(input_file)
    input_filename = os.path.basename(input_file)
    output_filename = f"seed_{input_filename}"
    output_file = os.path.join(input_dir, output_filename)
    
    with open(input_file, 'r', encoding='utf-8') as infile, \
         open(output_file, 'w', encoding='utf-8') as outfile:
        
        for line in infile:
            # Parse the JSON line
            data = json.loads(line.strip())
            
            # Extract id
            record_id = data.get('id', '')
            
            # Extract first user message from the conversation
            messages = data.get('message', [])
            first_user_message = ""
            
            # Find the first message with role "user"
            for message in messages:
                if message.get('role') == 'user':
                    first_user_message = message.get('content', '')
                    break
            
            # Create the new JSON structure
            seed_data = {
                "id": record_id,
                "prompt": first_user_message
            }
            
            # Write to output file
            outfile.write(json.dumps(seed_data, ensure_ascii=False) + '\n')
    
    print(f"Successfully created {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract seed data from JSONL file")
    parser.add_argument("input_file", help="Input JSONL file path")
    
    args = parser.parse_args()
    
    if not os.path.exists(args.input_file):
        print(f"Error: File '{args.input_file}' not found")
        exit(1)
    
    extract_seed_data(args.input_file)