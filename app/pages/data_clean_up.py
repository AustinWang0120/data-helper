import streamlit as st
import pandas as pd
from app.helpers.utilities import get_csv_download_link


def run():
    st.title("Data 处理器")

    # 上传文件
    uploaded_file = st.file_uploader("上传一个CSV文件", type=["csv"])

    if uploaded_file:
        data = pd.read_csv(uploaded_file)

        # 用户输入代表空值的字符串或字符
        missing_value_identifier = st.text_input("请输入代表空值的字符串或字符（例如：'.'）：")

        # 如果数据中有该字符串或字符，替换为NaN
        if missing_value_identifier:
            data.replace(missing_value_identifier, pd.NA, inplace=True)

        # 选择有缺失值的列部分
        st.write("选择需要移除的缺失值列：")
        options = st.multiselect(
            '选择列',
            data.columns,
            []
        )

        # 按钮触发数据清洗
        if st.button('移除缺失值'):
            for option in options:
                data.dropna(subset=[option], inplace=True)

            # 显示下载CSV的链接
            st.markdown(get_csv_download_link(data), unsafe_allow_html=True)

            st.write("处理后的数据预览：")
            st.write(data)
