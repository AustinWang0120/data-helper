import streamlit as st
from app.helpers.utilities import get_csv_download_link
import pandas as pd
import random
import re

def run():
    st.title("Transpose 分类处理器")

    uploaded_file = st.file_uploader("上传一个 TXT 文件", type=['txt'])

    if uploaded_file:
        # 读取txt文件的内容到列表中
        lines = uploaded_file.readlines()
        lines = [line.decode("utf-8").strip() for line in lines]

        # 定义一个函数来处理每一行的文本内容
        def process_line(line):
            for i in range(20, 0, -1):
                line = line.replace(f"proc{i}", "")
            line = re.sub(r"_+", "_", line)
            line = line.strip("_")
            return line

        # 处理所有的行
        processed_lines = [process_line(line) for line in lines]

        # 创建一个包含原始文本和处理后文本的 DataFrame
        df = pd.DataFrame({
            "Original Text": lines,
            "Processed Text": processed_lines
        })
        
        st.markdown(get_csv_download_link(df), unsafe_allow_html=True)

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
