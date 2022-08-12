import streamlit as st 

from streamlit import session_state as state

from demo_app_v1_1.page import page_group

from demo_app_v1_1.streamlit_gallery import components

import sys

from demo_app_v1_1.models import System_Models

import sys
sys.path.append('/Users/wuzhenxiong/主营科研/红宝石项目/plotly_dirgraph_master')
from demo_app_v1_1.plotly_dirgraph_master.addEdge import addEdge, addEdge_3D

import plotly.graph_objects as go

def main():
    page = page_group("p")

    st.write(
        """
        🚄 🐻 's HabitatPower 1.1
        ======================
        """
        )

    with st.expander("READ ME"):
        st.write('In this version demo users could try out building their own systems and test its energy consumptions under various parameters conditions.')

    with st.sidebar:
        st.title("Elder 🐻 Discovery")

        with st.expander('Scene Creation', True):
            #choice = st.selectbox('Apps', ['System App', 'Transfer App'])
            #if choice == 'System App':
            #    system_app.app()
            page.item('Click to create scene', components.scene_create, default = True)
        
        with st.expander('Parameters Editing', True):
            page.item('Click to edit parameters', components.par_editor)

        #with st.expander('Dashboard Run', True):
         #   page.item('Click to run dashboard', components.elements)


    #if choice == 'System App':
     #   system_app.app()

    page.show()



if __name__ == "__main__":
    #st.set_page_config(page_title="🚄 🐻 's HabitatPower", page_icon = "🚄 🐻", layout="wide")
    main()
