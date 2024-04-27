""" convert json files from Materials to jsonl. jsonl is used to call deployed LLMs"""
import json
import os

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
    directory = '../Materials/textbooks/Organic_Chemistry_Structure_and_Function/single_modal'  # 替换为你的目录路径
    output_file = '../Materials/jsonl_dataset/Organic_Chemistry_Structure_and_Function_single_modal.jsonl'  # 替换为你的输出文件路径
    merge_json_to_jsonl(directory, output_file)