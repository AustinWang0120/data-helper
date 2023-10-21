import streamlit as st
import streamlit_analytics
from app.pages import excel_processor, transpose_categorizer, variables_trim, data_clean_up

with streamlit_analytics.track():
    page = st.sidebar.selectbox(
        "选择页面", ["Excel 数据处理器", "Transpose 分类处理器", "Variables 分类器", "Data 处理器"])

    if page == "Excel 数据处理器":
        excel_processor.run()
    elif page == "Transpose 分类处理器":
        transpose_categorizer.run()
    elif page == "Variables 分类器":
        variables_trim.run()
    elif page == "Data 处理器":
        data_clean_up.run()
