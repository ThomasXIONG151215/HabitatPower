import streamlit as st 

from streamlit_apps import System_App,Heat_Transfer_App, Wind_Field_App, Gym_app

PAGES = {
    "System Modelling": System_App,
    "Wind Field Modelling": Wind_Field_App,
    "Heat Transfer Modelling": Heat_Transfer_App,
    "Gym Training and Modelling": Gym_app
}

st.sidebar.title("Navigation")
selection = st.sidebar.radio("Go to", list(PAGES.keys()))
page = PAGES[selection]
page.app()
