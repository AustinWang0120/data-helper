import streamlit as st
from app.helpers.utilities import get_csv_download_link, get_txt_download_link
import pandas as pd
import re


def remove_proci(line):
    for i in range(20, 0, -1):
        line = line.replace(f"proc{i}", "")

    if re.search(r"proc", line):
        line = re.sub(r"proc", "", line)
        line = re.sub(r"(\d+)$", "", line)

    line = re.sub(r"_+", "_", line)
    line = line.strip("_")
    return line


def run():
    st.title("Transpose 分类器")

    uploaded_file = st.file_uploader("上传一个 TXT 文件", type=['txt'])

    if uploaded_file:
        # 读取txt文件的内容到列表中
        lines = uploaded_file.readlines()
        lines = [line.decode("utf-8").strip() for line in lines]

        # 处理所有的行
        processed_lines = [remove_proci(line) for line in lines]

        # 创建一个包含原始文本和处理后文本的 DataFrame
        df = pd.DataFrame({
            "Original Text": lines,
            "Processed Text": processed_lines
        })

        # 显示下载CSV的链接
        st.markdown(get_csv_download_link(df), unsafe_allow_html=True)

        # 显示下载TXT的链接
        st.markdown(get_txt_download_link(
            processed_lines), unsafe_allow_html=True)

        # 显示处理后的数据
        st.write(df)
