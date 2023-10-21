import streamlit as st
import base64
import re


def process_lines(lines):
    with_numbers = [line for line in lines if re.search(r'\d', line)]
    without_numbers = [line for line in lines if not re.search(r'\d', line)]

    unique_with_numbers = list(set(with_numbers))
    unique_without_numbers = list(set(without_numbers))

    formatted_with_numbers = ', '.join(
        [f'"{line}"' for line in unique_with_numbers])
    formatted_without_numbers = ', '.join(
        [f'"{line}"' for line in unique_without_numbers])

    return formatted_with_numbers, formatted_without_numbers


def get_txt_download_link_for_data(data, filename):
    b64 = base64.b64encode(data.encode()).decode()
    href = f'<a href="data:file/txt;base64,{b64}" download="{filename}.txt">点击下载 {filename} 文件</a>'
    return href


def run():
    st.title("Variables 分类器")

    uploaded_file = st.file_uploader("上传一个 TXT 文件", type=['txt'])

    if uploaded_file:
        # 读取txt文件的内容到列表中
        lines = uploaded_file.readlines()
        lines = [line.decode("utf-8").strip() for line in lines]

        with_numbers, without_numbers = process_lines(lines)

        # 显示下载链接
        st.markdown(get_txt_download_link_for_data(
            with_numbers, "with_numbers"), unsafe_allow_html=True)
        st.markdown(get_txt_download_link_for_data(
            without_numbers, "without_numbers"), unsafe_allow_html=True)
