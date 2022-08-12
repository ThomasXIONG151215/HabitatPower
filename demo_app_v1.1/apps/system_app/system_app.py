import sys

sys.path.append('/Users/wuzhenxiong/主营科研/红宝石项目/models')

import System_Models

import streamlit as st 

from streamlit_elements import elements, mui, html

def main():
    st.markdown('# System page')

    with elements("new_element"):
        mui.Typography("Hello world")

if __name__ == "__main__":
    main()
