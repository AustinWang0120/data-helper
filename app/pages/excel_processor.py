import streamlit as st
from app.helpers.data_operations import extract_and_sort_row
from app.helpers.utilities import get_txt_download_link
import pandas as pd


def run():
    st.title('Excel 处理器')

    # 上传文件
    uploaded_file = st.file_uploader(
        "上传一个 Excel 或 CSV 文件", type=['xlsx', 'csv'])

    if uploaded_file:
        # 根据文件扩展名来决定使用哪个 pandas 读取函数
        if uploaded_file.name.endswith('.xlsx'):
            df = pd.read_excel(uploaded_file, header=None)
        elif uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file, header=None)

        # 使用 Streamlit 的滑块组件让用户选择要提取的行（默认为第一行）
        row_number = st.slider("选择要提取的行", 0, len(df)-1, 0)

        # 使用 Streamlit 的选择框组件让用户选择排序方法
        sort_methods = ["不排序", "字母顺序", "字母逆序", "长度递增", "长度递减"]
        sort_method = st.selectbox("选择排序方法", sort_methods)

        # 提取并排序选定行的内容
        sorted_data = extract_and_sort_row(df, row_number, sort_method)

        # 输出到 Streamlit
        st.write("处理后的数据：")
        for item in sorted_data:
            st.write(item)

        # 提供下载链接
        st.markdown(get_txt_download_link(sorted_data), unsafe_allow_html=True)
