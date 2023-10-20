# 导入所需的库
import streamlit as st
import pandas as pd

def extract_and_sort_row(df, row_number, sort_method):
    # 提取指定行的内容
    data_row = df.iloc[row_number].tolist()

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

st.title('Excel 数据处理')

# 上传文件
uploaded_file = st.file_uploader("上传一个 Excel 文件", type=['xlsx'])

if uploaded_file:
    # 读取 Excel 文件
    df = pd.read_excel(uploaded_file)

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
