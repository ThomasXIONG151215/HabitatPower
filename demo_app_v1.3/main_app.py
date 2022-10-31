from curses import use_default_colors
import streamlit as st 
import streamlit.components.v1 as components
st.set_page_config(layout="wide")
import base64

# 显示PDF文件的函数
def st_display_pdf(pdf_file):
    with open(pdf_file, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    pdf_display = f'<embed src="data:application/pdf;base64,{base64_pdf}" width="1700" height="800" type="application/pdf">'
    st.markdown(pdf_display, unsafe_allow_html=True)


st.title("演示文稿")

st_display_pdf("演示文稿.pdf")

