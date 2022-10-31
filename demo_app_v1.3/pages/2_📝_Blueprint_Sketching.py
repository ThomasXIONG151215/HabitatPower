from curses import use_default_colors
import streamlit as st 
import streamlit.components.v1 as components
st.set_page_config(layout="wide")
st.markdown("# 📝 能量蓝图绘制模块")
st.sidebar.markdown("# 📝 Blueprint Sketching")
st.markdown("低代码-可拖拽节点编辑器形式的场景设计界面")

components.iframe("http://1.117.83.145/", height=1000, width=800, scrolling=False)