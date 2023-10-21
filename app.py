import streamlit as st
from app.pages import excel_processor, text_processor

page = st.sidebar.selectbox("选择页面", ["Excel 数据处理器", "Transpose 分类处理器"])

if page == "Excel 数据处理器":
    excel_processor.run()
elif page == "Transpose 分类处理器":
    text_processor.run()
