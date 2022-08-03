import streamlit as st

def app():
  st.markdown('# Demo Introduction')
  st.markdown('This demo app introduce the HabitatPower philosophy on the way energy system simulation is ought to be.')
  st.markdown('## Scenario Case ')
  st.markdown('The first scenario case of the app ever presented shall be a simple cold water refrigeration system. Engineers have to the best way to respond to a certain cooling demand by controlling various refrigeration parameters. ')
  st.markdown('The system is mainly composed by two chillers, four water pumps, two cooling towers and two air handling units: The water coming back from the air handling units could be regarded as a feedback signal from the environment alongside the thermal demand from the hall and the platform.')
  st.image('./scenario_case_1.png')
  st.write('Further controls onto the air-side managements will be developed alongside many other functionalities')
