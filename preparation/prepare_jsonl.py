""" convert json files from Materials to jsonl. jsonl is used to call deployed LLMs"""
import json
import os
from prompt_template import PROMPT_TEMPLATE_DICT

def add_prompt_to_question(input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            data = json.loads(line)
            question = data.get('question', '')
            question_type = data.get('type')
            prefix = PROMPT_TEMPLATE_DICT.get(question_type.split("/")[0])
            if prefix:
                data['question'] = f"{prefix} {question}"
            json.dump(data, outfile)
            outfile.write('\n')

def merge_json_to_jsonl(directory, output_file):
    with open(output_file, 'w') as outfile:
        for filename in os.listdir(directory):
            if filename.endswith('.json'):
                filepath = os.path.join(directory, filename)
                with open(filepath, 'r') as infile:
                    data = json.load(infile)
                    data['filename'] = filename  # 添加文件名到 JSON 数据中
                    json.dump(data, outfile)
                    outfile.write('\n')  # 写入换行符，将每个 JSON 对象分隔开




if __name__ == "__main__":
    # 示例用法
    # directory = '../Materials/textbooks/Organic_Chemistry_Structure_and_Function/single_modal'
    raw_jsonl_file = '../Materials/jsonl_dataset/Organic_Chemistry_Structure_and_Function_single_modal.jsonl'
    # merge_json_to_jsonl(directory, raw_jsonl_file)
    processed_jsonl_file = '../Materials/jsonl_dataset/prompt_Organic_Chemistry_Structure_and_Function_single_modal.jsonl'
    add_prompt_to_question(raw_jsonl_file,processed_jsonl_file)