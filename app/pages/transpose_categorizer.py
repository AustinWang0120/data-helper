import streamlit as st
from app.helpers.data_operations import remove_proci
from app.helpers.utilities import get_csv_download_link, get_txt_download_link
import pandas as pd
import random
import re


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

        # 随机选择最多50行展示
        sample_size = min(50, len(lines))
        sampled_indices = random.sample(range(len(lines)), sample_size)

        for idx in sampled_indices:
            original = lines[idx]
            processed = processed_lines[idx]
            col1, col2 = st.columns(2)
            with col1:
                st.text(original)
            with col2:
                st.text(processed)
