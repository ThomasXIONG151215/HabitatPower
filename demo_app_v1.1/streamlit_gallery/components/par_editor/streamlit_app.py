import streamlit as st 
import json 
import networkx as nx
import sys
sys.path.append('/Users/wuzhenxiong/主营科研/红宝石项目/models')
import numpy as np 
from System_Models import Chiller, Pump, Fan, Tower, Exchanger, AHU
from streamlit import session_state

json_object = None 
with open("/Users/wuzhenxiong/业余初创项目/研屋调源/streamlit_app_1.2/streamlit_gallery/data/created_scene.json", "r") as openfile:
    json_object = json.load(openfile)
graph_data = nx.node_link_graph(json_object)

exchangers = []
chillers = []
cooling_pumps = []
chilled_pumps = []
towers = []

for i in graph_data.nodes:
    if 'Exchanger' in i:
        object = Exchanger()
        exchangers.append(object)
    elif 'Chiller' in i:
        object = Chiller(777)
        object.Tower = Tower()
        chillers.append(object)
    elif 'Cooling Pump' in i:
        object = Pump(2)
        cooling_pumps.append(object)
    elif 'Chilled Pump' in i:
        object = Pump(2)
        chilled_pumps.append(object)
    #elif 'Tower' in i: 
        #   object = Tower()
        #  towers.append(object)\

all_data = {}

for i in range(len(exchangers)):
    all_data['exchanger ' + str(i + 1) + ' T_ahu_L'] = []

for i in range(len(chillers)):
    all_data['chiller ' + str(i + 1) + ' Qe'] = []
    all_data['chiller ' + str(i + 1) + ' Te'] = []
    all_data['chiller ' + str(i + 1) + ' r'] = []
    all_data['chiller ' + str(i + 1) + ' Ncom'] = []

for i in range(len(cooling_pumps)):
    all_data['cooling pump ' + str(i + 1) + ' G'] = []
    all_data['cooling pump ' + str(i + 1) + ' N'] = []

for i in range(len(chilled_pumps)):
    all_data['chilled pump ' + str(i + 1) + ' G'] = []
    all_data['chilled pump ' + str(i + 1) + ' N'] = []


all_data['common tower Twl'] = []
all_data['common tower Twe'] = []
all_data['air enthalpy'] = []
all_data['moist air enthalpy'] = []
all_data['total_Q'] = []

all_data['try step'] = []

def main():
    st.header("Parameters Editor")
    #all_data = {}
    for i in range(len(exchangers)):
        session_state['exchanger ' + str(i + 1) + ' T_ahu_L'] = 0

    for i in range(len(chillers)):
        session_state['chiller ' + str(i + 1) + ' Qe'] = 0
        session_state['chiller ' + str(i + 1) + ' Te'] = 0
        session_state['chiller ' + str(i + 1) + ' r'] = 0
        session_state['chiller ' + str(i + 1) + ' Ncom'] = 0

    for i in range(len(cooling_pumps)):
        session_state['cooling pump ' + str(i + 1) + ' G'] = 0
        session_state['cooling pump ' + str(i + 1) + ' N'] = 0

    for i in range(len(chilled_pumps)):
        session_state['chilled pump ' + str(i + 1) + ' G'] = 0
        session_state['chilled pump ' + str(i + 1) + ' N'] = 0


    session_state['common tower Twl'] = 0
    session_state['common tower Twe'] = 0
    session_state['air enthalpy'] = 0
    session_state['moist air enthalpy'] = 0
    session_state['total_Q'] = 0


    col1, col2 = st.columns(2)
    with col1:
        with st.expander('Cooling Demand'):
            total_Q = st.number_input('Total cooling demand (kW)', step = 10, value = 300) #500#kW 
            session_state['total_Q'] = total_Q
    with col2:
        h_a_Es = []
        h_as_Es = []
        with st.expander('Outdoor Conditions'):
            h_a_E = st.number_input('air enthalpy in kW', step = 20, value = 400)#400
            h_as_E = st.number_input('moist air enthalpy in kW', step = 20, value = 500)#500
            h_a_Es.append(h_a_E)
            h_as_Es.append(h_as_E)
            session_state['air enthalpy'] = h_a_E
            session_state['moist air enthalpy'] = h_as_E
    exchangers_T_w = []
    count = 1
    with st.expander('Current Feedbacks'):
        if len(exchangers) >= 1:
            for exchanger in exchangers:
                value = st.number_input('Outlet water T from exchanger ' + str(count), min_value=18, max_value=30, value = 25)
                exchangers_T_w.append(value)
                session_state['exchanger ' + str(count) + ' T_ahu_L'] = value
                count+=1
        else:
            value = st.number_input('Outlet water T from exchanger ' + str(count), min_value=18, max_value=30, value = 25)
            st.write('There is no heat exchanger in you system')


    with st.expander('Initial Settings'):
        col4, col5 = st.columns(2)

        with col4:
            chillers_Qe_settings = []
            
            count = 1
            st.write(chillers)
            for chiller in chillers:
                chiller.Qe = st.number_input('Chiller ' + str(count) + ' Qe (kW)', value = 0.5 * (total_Q), min_value = float(0), max_value = float(total_Q), step = float(10))
                chillers_Qe_settings.append(chiller.Qe)
                session_state['chiller ' + str(count) + ' Qe'] = chiller.Qe
                count +=1
        
        with col5:
            towers_Te = []
            towers_Tl = []
            count = 1
            if len(towers) >= 1:
                pass 
            else:
                st.write('There is no tower in your system, will set a common one')
                Tower_Twe = st.number_input('Common tower entering water temperature',min_value= 25, max_value = 35, value=28)
                Tower_Twl = st.number_input('Common tower leaving water temperature',min_value= 25, max_value = 35, value=28)
                session_state['common tower Twe'] = Tower_Twe
                session_state['common tower Twl'] = Tower_Twl

                towers_Te.append(Tower_Twe)
                towers_Tl.append(Tower_Twl)

        
    with st.expander('Operational Settings'):
        col6, col7= st.columns(2)
        
        with col6:
            st.subheader('Cooling Pumps')
            count = 1
            cool_pumps_flow_rate = [] #demo中假设各类设备之间是集成关系，而不是一对一关系
            cool_pumps_N = []
            for cool_pump in cooling_pumps:
                cool_pump.flow_rate = st.slider('Cooling Pump LD 1 '+ str(count) + ' flow rate (t/h)', min_value = 150, max_value = 350, value = 281)
                session_state['cooling pump ' + str(count) + ' G'] = cool_pump.flow_rate
                cool_pump.run_pump(cool_pump.flow_rate)
                cool_pumps_N.append(cool_pump.Npump)
                cool_pumps_flow_rate.append(cool_pump.flow_rate)
                session_state['cooling pump ' + str(count) + ' N'] = cool_pump.Npump

                count += 1

            cooling_pumps_average_G = np.mean(cool_pumps_flow_rate)
            #假设没有流量损失
            

        with col7:
            st.subheader('Chilled Pumps')
            count = 1
            chilled_pumps_flow_rate = []
            chilled_pumps_N = []
            for chill_pump in chilled_pumps:
                chill_pump.flow_rate = st.slider('Chilled Pump LD 1 '+ str(count) + ' flow rate (t/h)', min_value = 150, max_value = 360, value = 221)
                session_state['chilled pump ' + str(count) + ' G'] = chill_pump.flow_rate
                chill_pump.run_pump(chill_pump.flow_rate)
                chilled_pumps_N.append(chill_pump.Npump)
                chilled_pumps_flow_rate.append(chill_pump.flow_rate)
                session_state['chilled pump ' + str(count) + ' N'] = chill_pump.Npump

                count += 1
                
            chilled_pumps_average_G = np.mean(chilled_pumps_flow_rate)


        st.subheader('Chillers')
        count = 1
        chillers_N = []
        for chiller in chillers:
            r = chiller.Qe / chiller.Qe_max
            st.write('Chiller ' + str(count) + 'load ratio is ' + str(r))
            chiller.Te = st.slider('Chiller ' + str(count) + ' Evaporation Temperature (C)', min_value = 22, max_value = 35, value = 27)
            chiller.G_w_e = cooling_pumps_average_G
            chiller.G_w_c = chilled_pumps_average_G
            chiller.Tower.G_w = cooling_pumps_average_G #水塔与冷机之间也没有流量损失
            chiller.simple_run(r, chiller.Te, Tower_Twe, Tower_Twl)
            chillers_N.append(chiller.Ncom)

            session_state['chiller ' + str(count) + ' r'] = r
            session_state['chiller ' + str(count) + ' Te'] = chiller.Te
            session_state['chiller ' + str(count) + ' Ncom'] = chiller.Ncom

            count += 1
        
    def button_store_data():
        for key in [key for key in all_data if key != 'try step']:
            all_data[key].append(session_state[key])
        all_data['try step'].append(len(all_data['try step']) + 1)
        #st.write(all_data)
            #session_state.test.append(session_state[key])
        #session_state.test+=1

    st.button('Store data', on_click=button_store_data)
    
    #if store:
     #   st.session_state.count +=1
      #  for key in all_data:
       #     all_data[key].append(session_state[key])
        #    session_state.test.append(session_state[key])
        
    #st.write(all_data)
    st.header('Power Results')
    #run
    col9, col10, col11 = st.columns(3)
    with col9:
        count = 1
        for cool_pump_N in cool_pumps_N:
            st.write('Cooling pump ' + str(count) + ' consumption (kW)', cool_pump_N)
            count += 1
    
    with col10:
        count = 1
        for chill_pump_N in chilled_pumps_N:
            st.write('Chill pump ' + str(count) + ' consumption (kW)', chill_pump_N)
            count += 1

    with col11:
        count = 1
        for chiller_N in chillers_N:
            st.write('Chiller ' + str(count) + ' consumption (kW)', chiller_N)
            count += 1
        
    
    import plotly.express  as px 
    import pandas as pd 
    import plotly.graph_objects as go 

    #st.write(all_data)

    st.header('Historical Records')

    col12, col13 = st.columns((1,1))

    with col12:
        st.subheader('Energy Consumptions')
        ylist = []
        for i in range(len(chillers_N)):
            ylist.append('chiller ' + str(i+1) + ' Ncom')
        for i in range(len(chilled_pumps_N)):
            ylist.append('chilled pump ' + str(i+1) + ' N')
        for i in range(len(cool_pumps_N)):
            ylist.append('cooling pump ' + str(i+1) + ' N')
        fig = px.line(data_frame = all_data, y =ylist,title='Consumptions', labels='Power in kW')
        #fig = px.line(data_frame = all_data, y =ylist,title='Consumptions')
        #fig.add_trace(go.Scatter(y =all_data['chill pump 1 N']))
        fig.update_layout(yaxis_title = 'Power in kW', height = 500, width = 450)
        st.plotly_chart(fig)  
    with col13:
        st.subheader('Water Flow Rates')
        ylist = []
        for i in range(len(chilled_pumps_N)):
            ylist.append('chilled pump ' + str(i+1) + ' G')
        for i in range(len(cool_pumps_N)):
            ylist.append('cooling pump ' + str(i+1) + ' G')
        fig = px.line(data_frame = all_data, y =ylist,title='Water flow rates')
        fig.update_layout(yaxis_title = 'Flow rate in t/h',height = 500, width = 450)
        st.plotly_chart(fig)  





if __name__ == "__main__":
    main()