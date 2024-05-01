"""
prepare data
"""
import os
import json

folder_path = "/Users/person/codeScope/organicChemBenchmark/results"
prompt_data_file_path = "/Users/person/codeScope/organicChemBenchmark/Materials/jsonl_dataset/prompt_Organic_Chemistry_Structure_and_Function_single_modal.jsonl"
output_file = "/Users/person/codeScope/organicChemBenchmark/visualization/overall_results.jsonl"


def merge_data(folder_path, prompt_data_file_path, output_file):
    # 合并数据
    result_files = [file for file in os.listdir(folder_path) if file.endswith('.jsonl')]
    model_names = [f.split("_")[0] for f in result_files]
    with open(prompt_data_file_path, "r") as f:
        prompt = [json.loads(line) for line in f]
    for model_name, result in zip(model_names, result_files):
        file_path = os.path.join(folder_path, result)
        with open(file_path, "r") as f:
            data = [json.loads(line) for line in f]
        for i in range(len(prompt)):
            p = prompt[i]
            d = data[i]
            assert p["question"] == d["data"], "question does not match!"
            if "answer" not in p:
                p["answer"] = {}
            p["answer"][model_name] = d["reply_sentence"]
    with open(output_file, 'w') as outfile:
        for tmp in prompt:
            json.dump(tmp, outfile)
            outfile.write('\n')


# merge_data(folder_path,prompt_data_file_path,output_file)


"""
streamlit
"""
import streamlit as st
import json


# 读取JSONL文件并解析为Python对象
def read_benchmark_data(file_path):
    data = []
    with open(file_path, 'r') as file:
        for line in file:
            entry = json.loads(line)
            data.append(entry)
    return data


# 根据问题类型筛选数据
def filter_data_by_type(data, question_type):
    filtered_data = []
    for entry in data:
        if entry['type'] == question_type:
            filtered_data.append(entry)
    return filtered_data


# 主函数
def main():
    # 设置页面标题
    st.title('Organic Chemistry Benchmark')

    # 读取benchmark数据
    data = read_benchmark_data(output_file)

    # 获取问题类型列表
    question_types = list(set(entry['type'].split("/")[0] for entry in data))

    # 选择问题类型进行筛选
    question_type = st.sidebar.selectbox('选择问题类型', [''] + question_types)

    # 根据筛选条件获取数据
    filtered_data = filter_data_by_type(data, question_type)


    # 选择展示的问题
    selected_questions = st.multiselect('选择展示的问题', [entry['chapter'] for entry in filtered_data])

    # 根据选择的问题展示数据
    for entry in filtered_data:
        question = entry['question']
        chapter = entry['chapter']
        question_type_entry = entry['type']
        result = entry['answer']

        if chapter in selected_questions:
            st.write('QUESTION:', question)
            st.write('TYPE:', question_type_entry)

            for model, answer in result.items():
                st.write('MODEL:', model)
                st.write('ANSWER:', answer)

            st.write('---')


if __name__ == '__main__':
    main()