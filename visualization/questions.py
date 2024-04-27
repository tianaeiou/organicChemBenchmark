""" streamlit run questions.py """
import os
import streamlit as st
import json


KEY_LIST = ["num_questions", "difficulty", "prompt_template", "chapter", "memo"]


# 读取习题的JSON文件
def read_exercise_from_json(file_path):
    with open(file_path, 'r') as file:
        exercise = json.load(file)
    return exercise

def main():
    # 设置页面标题
    st.title('Organic Chemistry Benchmark')

    # 选择习题集文件夹
    folder_path = "../Materials/textbooks/Organic_Chemistry_Structure_and_Function/single_modal"

    # 读取习题集文件夹中的所有JSON文件
    exercise_files = [file for file in os.listdir(folder_path) if file.endswith('.json')]

    # 左侧栏显示习题文件列表
    selected_file = st.sidebar.selectbox('Existing Problem Set', exercise_files)

    if selected_file:
        # 读取选中的习题文件
        exercise_file_path = os.path.join(folder_path, selected_file)
        exercise = read_exercise_from_json(exercise_file_path)

        # 在右侧展示习题内容
        st.header(selected_file)
        st.subheader('Type：' + exercise['type'])
        st.write('Question：', exercise['question'])
        for key in KEY_LIST:
            st.write(f"{key}: ", exercise[key])

    # 获取所有习题的类型和问题列表
    all_types = set()
    all_questions = set()
    for file in exercise_files:
        exercise_file_path = os.path.join(folder_path, file)
        exercise = read_exercise_from_json(exercise_file_path)
        all_types.add(exercise['type'])
        all_questions.add(exercise['question'])

    # 筛选条件选择框
    st.header('Filter')
    filter_type = st.selectbox('Filter by type', ['', *all_types])
    # filter_question = st.selectbox('Filter by ', ['', *all_questions])
    filter_question = ""

    # 根据筛选条件进行习题筛选
    filtered_exercises = []
    for file in exercise_files:
        exercise_file_path = os.path.join(folder_path, file)
        exercise = read_exercise_from_json(exercise_file_path)
        if (filter_type == '' or filter_type == exercise['type']) and (
                filter_question == '' or filter_question == exercise['question']):
            filtered_exercises.append(exercise)

    # 展示筛选后的习题列表
    st.subheader('Filtered Results')
    st.write('Find {} available results'.format(len(filtered_exercises)))
    for exercise in filtered_exercises:
        st.subheader(exercise['chapter'])
        st.write(exercise['question'])


if __name__ == '__main__':
    main()
