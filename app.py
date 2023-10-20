# 导入所需的库
import streamlit as st
import pandas as pd
import random
import base64
import re

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

def get_txt_download_link(data):
    import base64
    txt = "\n".join(str(x) for x in data)
    b64 = base64.b64encode(txt.encode()).decode()
    href = f'<a href="data:file/txt;base64,{b64}" download="sorted_data.txt">点击下载 TXT 文件</a>'
    return href

def feature_1():
    st.title('Excel 数据处理器')

    # 上传文件
    uploaded_file = st.file_uploader("上传一个 Excel 或 CSV 文件", type=['xlsx', 'csv'])

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

def feature_2():
    st.title("文本处理")

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

        # 为处理过的文本创建CSV下载链接
        def get_csv_download_link(dataframe):
            csv = dataframe.to_csv(index=False)
            b64 = base64.b64encode(csv.encode()).decode()
            return f'<a href="data:file/csv;base64,{b64}" download="processed_data.csv">点击下载处理后的 CSV 文件</a>'

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

page = st.sidebar.selectbox("选择页面", ["Excel 数据处理器", "Transpose 分类处理器"])

if page == "Excel 数据处理器":
    feature_1()
elif page == "Transpose 分类处理器":
    feature_2()
