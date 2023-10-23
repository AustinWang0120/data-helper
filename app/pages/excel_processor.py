import streamlit as st
from app.helpers.utilities import get_txt_download_link
import pandas as pd


def extract_and_sort_row(df, row_number, sort_method):
    # 提取指定行的内容并确保所有数据都是字符串类型
    data_row = [str(item) for item in df.iloc[row_number].tolist()]

    # 根据所选的排序方法进行排序
    if sort_method == "字母顺序":
        return sorted(data_row)
    elif sort_method == "字母逆序":
        return sorted(data_row, reverse=True)
    elif sort_method == "长度递增":
        return sorted(data_row, key=len)
    elif sort_method == "长度递减":
        return sorted(data_row, key=len, reverse=True)
    else:
        return data_row


def run():
    st.title('Excel 处理器')

    # 上传文件
    uploaded_file = st.file_uploader("上传一个CSV文件-1", type=['csv'])

    if uploaded_file:
        # 根据文件扩展名来决定使用哪个 pandas 读取函数
        if uploaded_file.name.endswith('.xlsx'):
            df = pd.read_excel(uploaded_file, header=None)
        elif uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file, header=None)

        # 使用下拉菜单组件让用户选择要提取的行
        row_number = st.selectbox("选择要提取的行", df.index+1)-1

        # 使用 Streamlit 的选择框组件让用户选择排序方法
        sort_methods = ["不排序", "字母顺序", "字母逆序", "长度递增", "长度递减"]
        sort_method = st.selectbox("选择排序方法", sort_methods)

        # 让用户输入一串字符串，用于将以此开头的内容都去除，如果用户没有输入，则不用去除任何内容
        remove_starting_with = st.text_input("请输入开头内容以去除相关内容：")

        if st.button("查看结果"):
            # 提取并排序选定行的内容，并且去除以用户输入的字符串开头的内容
            sorted_data = extract_and_sort_row(df, row_number, sort_method)
            if remove_starting_with:
                sorted_data = [item for item in sorted_data if not item.startswith(
                    remove_starting_with)]

            # 提供下载链接
            st.markdown(get_txt_download_link(
                sorted_data), unsafe_allow_html=True)

            if len(sorted_data) > 50:
                # 展示一共有多少行数据
                st.write(f"处理后的数据共有 {len(sorted_data)} 行")
                st.write("前50行处理后的数据：")
                for item in sorted_data[:50]:
                    st.write(item)
            else:
                st.write("处理后的数据：")
                for item in sorted_data:
                    st.write(item)
