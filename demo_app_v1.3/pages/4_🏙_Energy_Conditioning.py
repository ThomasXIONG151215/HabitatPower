import streamlit as st

from components.elements import dashboard 
from streamlit_elements import elements, mui, html
st.markdown("# ð è½æºè¿è¥è°èæ¨¡å")
st.sidebar.markdown("# ð Energy Operational Conditioning Module")
st.markdown("æ§è¡å»é¢ç³»ç»çç©çåºä»¿çæ¨¡æå¹¶ä¸åéæ±å®æ¶ç­ååºæä¼çèµæºè°é")

import plotly.express as px
import pandas as pd
from streamlit import session_state as state
from streamlit_elements import elements, sync, event
from types import SimpleNamespace
import json
import numpy as np
from components.elements.dashboard import Dashboard, Editor, Card, DataGrid, Radar, Pie, Player, DataGrid2

SPACE_COLUMNS = [
        { "field": 'id', "headerName": 'ID', "width": 90 },
        { "field": 'space', "headerName": 'ç©ºé´åç§°', "width": 90 },
        { "field": 'volume', "headerName": 'ç©ºé´ä½ç§¯(m3)', "width": 150, "editable": True, },
        { "field": 'space_heat_capacitance', "headerName": 'ç©ºé´ç­å®¹(kJ/K)',  "width": 110, "editable": True, },
        { "field": 'envelope_heat_resistance', "headerName": 'å´æ¤ä½ç­é»(K/kW)',  "width": 110, "editable": True, },
        { "field": 'neighbor_heat_conductance', "headerName": 'è¿é»ç­æ(K/(H.kJ))',  "width": 110, "editable": True, },
        { "field": 'average_heat_load', "headerName": 'å¸åç­è´è·(kJ)',  "width": 110, "editable": True, },
        { "field": 'average_fresh_air_demand', "headerName": 'å¸åéæ±æ°é£é(m3/h)',  "width": 110, "editable": True, },
    ]

END_DEVICE_MANAGEMENT_COLUMNS = [ #ä¸å°ä¸»æº(å¤èæºå®¤å¤æºoræ°´ç³»ç»)ä¸ä¸ª
        { "field": 'id', "headerName": 'ID', "width": 90 },
        { "field": 'end_device', "headerName": 'æ«ç«¯ä»£å·', "width": 90 },
        { "field": 'cooling_capacity', "headerName": 'é¢å®å¶å·é(kW)', "width": 150, "editable": False, },
        { "field": 'heating_capacity', "headerName": 'é¢å®å¶ç­é(kW)',  "width": 110, "editable": False, },
        { "field": 'fresh_air_capacity', "headerName": 'é¢å®å¾ªç¯é£é(m3/h)',  "width": 110, "editable": False, },
        { "field": 'fresh_air_power_use', "headerName": 'é£æºè¿è¡åç(kW)',  "width": 110, "editable": False, },

        { "field": 'cooling_task', "headerName": 'æå®å¶å·é(kW)', "width": 150, "editable": True, },
        { "field": 'heating_task', "headerName": 'æå®å¶ç­é(kW)',  "width": 110, "editable": True, },
        { "field": 'fresh_air_task', "headerName": 'æå®å¾ªç¯é£é(m3/h)',  "width": 110, "editable": True, },
        { "field": 'substance_ratio', "headerName": 'å·åªå¼åº¦(%)',  "width": 110, "editable": True, },
        { "field": 'frequency', "headerName": 'é£æºè¿è¡é¢ç(Hz)',  "width": 110, "editable": True, },
    ]

MAIN_DEVICE_COLUMNS = [ #ä¸å°ä¸»æº(å¤èæºå®¤å¤æºoræ°´ç³»ç»)ä¸ä¸ª
        { "field": 'id', "headerName": 'ID', "width": 90 },
        { "field": 'main_device', "headerName": 'ä¸»æºä»£å·', "width": 90 },
        { "field": 'cooling_capacity', "headerName": 'é¢å®å¶å·é(kW)', "width": 150, "editable": False, },
        { "field": 'heating_capacity', "headerName": 'é¢å®å¶ç­é(kW)',  "width": 110, "editable": False, },
        { "field": 'cooling_power_use', "headerName": 'å¶å·COP',  "width": 110, "editable": False, },
        { "field": 'heating_power_use', "headerName": 'å¶ç­COP',  "width": 110, "editable": False, },

        { "field": 'cooling_task', "headerName": 'æå®æ»å¶å·é(kW)', "width": 150, "editable": True, },
        { "field": 'heating_task', "headerName": 'æå®æ»å¶ç­é(kW)',  "width": 110, "editable": True, },
    ]


SPACE_ROWS = [
        { "id": 1, "space": 'çæ¿åºåI', "volume": 210, "space_heat_capacitance": 35, "envelope_heat_resistance": 1.3 , 'neighbor_heat_conductance': 2.1, 'average_heat_load':1200, 'average_fresh_air_demand': 13000},
        { "id": 2, "space": 'çæ¿åºåII', "volume": 210, "space_heat_capacitance": 42, "envelope_heat_resistance": 1.3 , 'neighbor_heat_conductance': 2.1, 'average_heat_load':600, 'average_fresh_air_demand': 15000},
        { "id": 3, "space": 'åå¬åºå', "volume": 1190, "space_heat_capacitance": 45, "envelope_heat_resistance": 1.3 , 'neighbor_heat_conductance': 2.1, 'average_heat_load':2500, 'average_fresh_air_demand': 4000},
        { "id": 4, "space": 'å¬å±èµ°å»', "volume": 1071, "space_heat_capacitance": 16, "envelope_heat_resistance": 1.3 , 'neighbor_heat_conductance': 2.1, 'average_heat_load':700, 'average_fresh_air_demand': 5600},
        { "id": 5, "space": 'å¨±ä¹æ´»å¨åº', "volume": 420, "space_heat_capacitance": 32, "envelope_heat_resistance": 1.3 , 'neighbor_heat_conductance': 2.1, 'average_heat_load':2100, 'average_fresh_air_demand': 13020},
    ]

END_ROWS = [
        {"id": 1, "end_device": "å®¤åæºI", "cooling_capacity": 3.2, "heating_capacity": 2.3, "fresh_air_capacity": 12000, "fresh_air_power_use": 32, "cooling_task": 34, "heating_task":50, "fresh_air_task": 3000, "substance_ratio":30, "frequency":33},
        {"id": 2, "end_device": "å®¤åæºII", "cooling_capacity": 3.2, "heating_capacity": 2.3, "fresh_air_capacity": 12000, "fresh_air_power_use": 32, "cooling_task": 34, "heating_task":50, "fresh_air_task": 3000, "substance_ratio":30, "frequency":33},
        {"id": 3, "end_device": "å®¤åæºIII", "cooling_capacity": 3.2, "heating_capacity": 2.3, "fresh_air_capacity": 12000, "fresh_air_power_use": 32, "cooling_task": 34, "heating_task":50, "fresh_air_task": 3000, "substance_ratio":30, "frequency":33},
        {"id": 4, "end_device": "å®¤åæºIV", "cooling_capacity": 3.2, "heating_capacity": 2.3, "fresh_air_capacity": 12000, "fresh_air_power_use": 32, "cooling_task": 34, "heating_task":50, "fresh_air_task": 3000, "substance_ratio":30, "frequency":33},
        {"id": 5, "end_device": "å®¤åæºV", "cooling_capacity": 3.2, "heating_capacity": 2.3, "fresh_air_capacity": 12000, "fresh_air_power_use": 32, "cooling_task": 34, "heating_task":50, "fresh_air_task": 3000, "substance_ratio":30, "frequency":33}
]

MAIN_ROWS = [
        {"id": 1, "main_device": "å¤èä¸»æº", "cooling_capacity": 21.2, "heating_capacity": 20.3, "cooling_power_use": 4.3, "heating_power_use": 3.2, "cooling_task": 2234, "heating_task": 1500},
]


HEAT_LOAD_PIE = [
        { "id": 1, "label": "çæ¿åºåI", "value": SPACE_ROWS[0]["average_heat_load"], "color": "hsl(12, 40%, 20%)" },
        { "id": 2, "label": "çæ¿åºåII", "value": SPACE_ROWS[1]["average_heat_load"], "color": "hsl(178, 70%, 50%)" },
        { "id": 3, "label": "åå¬åºå", "value": SPACE_ROWS[2]["average_heat_load"], "color": "hsl(322, 70%, 50%)" },
        { "id": 4, "label": "å¬å±èµ°å»", "value": SPACE_ROWS[3]["average_heat_load"], "color": "hsl(117, 70%, 50%)" },
        { "id": 5, "label": "å¨±ä¹æ´»å¨åº", "value": SPACE_ROWS[4]["average_heat_load"], "color": "hsl(286, 70%, 50%)" }
    ]

df = pd.DataFrame(dict(
                    Time = ['08:00', '08:10', '08:20', '08:30', '08:40', '08:50', 
                    '09:00', '09:10', '09:20', '09:30', '09:40', '09:50', 
                    '10:00', '10:10', '10:20', '10:30', '10:40', '10:50', 
                    '11:00', '11:10', '11:20', '11:30', '11:40', '11:50'],
                    Temperatures = [20, 20.1, 20.1, 20.4, 20.5, 20.6,
                    21, 21.1, 20, 21.4, 20.5, 20.6,
                    22, 22, 21.6, 21.4, 22.5, 21.9,
                    22.5, 22.7, 22.3, 23, 23.2, 23.6],
                    Populations = [6, 6, 6, 6, 6, 6,
                    13, 13, 13, 7, 7, 7,
                    0, 0, 6, 6, 6, 6,
                    9, 9, 9, 9, 9, 9
                    ],
                    ))

with st.expander("é¡¹ç®ä¿¡æ¯æ»æ±"):
        
          if "w" not in state:
                    board = Dashboard()
                    w = SimpleNamespace(
                              dashboard=board,
                              pie=Pie(board, 3, 3, 4, 5, minW=1, minH=2),
                              #radar=Radar(board, 0, 3, 2, 5, minW=2, minH=2),
                              #card=Card(board, 6, 7, 3, 7, minW=2, minH=4),
                              #test_grid = DataGrid(board, 3,13, 6, 7, minH=4)
                              space_datagrid=DataGrid(board, 0, 0, 5, 5, minH=2),
                              end_device_datagrid=DataGrid(board, 2, 0, 4, 5, minH=2),
                              main_device_datagrid=DataGrid(board, 0, 1, 4, 5, minH=2),
                              editor=Editor(board, 0, 5, 4, 5 ,minW=1, minH=2),

                    )
                    state.w = w

                    #w.editor.add_tab("Card content", Card.DEFAULT_CONTENT, "plaintext")
                    w.editor.add_tab("Space Datagrid", json.dumps(SPACE_ROWS, indent=2, ensure_ascii=False), "json")
                    w.editor.add_tab("End Device Datagrid", json.dumps(END_ROWS, indent=2, ensure_ascii=False), "json")
                    w.editor.add_tab("Main Device Datagrid", json.dumps(MAIN_ROWS, indent=2, ensure_ascii=False), "json")
                    #w.editor.add_tab("Radar chart", json.dumps(Radar.DEFAULT_DATA, indent=2), "json")
                    w.editor.add_tab("Heat Load Pie", json.dumps(HEAT_LOAD_PIE, indent=2, ensure_ascii=False), "json")
                    #w.editor.add_tab("Datagrid 2")
          else:
                    w = state.w

          with elements("demo"):
                    event.Hotkey("ctrl+s", sync(), bindInputs=True, overrideDefault=False)

                    with w.dashboard(rowHeight=57):
                              w.editor()
                              #w.data_grid2()
                              #w.player()
                              w.pie("Heat Load Pie",w.editor.get_content("Heat Load Pie"))
                              #w.test_grid(DataGrid.DEFAULT_COLUMNS, json.dumps(DataGrid.DEFAULT_ROWS, ensure_ascii=False))
                              #w.radar(json.dumps(Radar.DEFAULT_DATA, indent=2))
                              #w.card(w.editor.get_content("Card content"))
                              w.space_datagrid( "Space Info" ,SPACE_COLUMNS, w.editor.get_content("Space Datagrid"))
                              w.end_device_datagrid( 'End Device Info', END_DEVICE_MANAGEMENT_COLUMNS , w.editor.get_content("End Device Datagrid"))
                              w.main_device_datagrid( 'Main Device Info' ,MAIN_DEVICE_COLUMNS , w.editor.get_content("Main Device Datagrid"))

with st.expander("ç­äº¤äºç»è®¡æ¨¡æ"):
          st.subheader("ç­äº¤äºç»è®¡æ¨¡æ")
          st.file_uploader("ä¸ä¼ åå²æ°æ® (æ¶é´æ®µ-ååºåæ¸©æ¹¿åº¦åå-å®¤å¤æ¸©æ¹¿åº¦è¾ç§å¼-è®¾å¤åæ°ä¸è½èæåµ)") #è¾ç§å¼åå®¤å¤æ¸©åº¦å¸®å©é¢ä¼°åçµé
          start_sim = st.button("ä¸é®ä»¿ç")
          #åæ°æåç»æï¼ ä»¿çç²¾ç¡®åº¦
          
          df_parameters = pd.DataFrame({
                    'ç©ºé´åºå': ['çæ¿åºåI', 'çæ¿åºåII', 'åå¬åºå', 'å¬å±èµ°å»', 'å¨±ä¹æ´»å¨åº'],
                    'ç©ºé´ç­å®¹(kJ/K)': [100, 100, 120, 80, 30],
                    'å´æ¤ä½ç­é»(K/kW)': [32, 100, 23, 43, 43],
                    'è¿é»ç­æ(K/(H.kJ))': [1, 4, 2, 9, 3],
                    })
          df_accuracy = pd.DataFrame({
                    'åºååå': ['ç¯å¢åºå', 'ç³»ç»é¨ä»¶'],
                    'æåR2': [0.93, 0.97658],
                    'æµè¯R2': [0.91, 0.94321]
                    })
          if start_sim:
                    st.dataframe(df_parameters, use_container_width=True)
                    st.dataframe(df_accuracy, use_container_width=True)
          

with st.expander("å¼ºåæä¼è¿è¡"): #æå¥½æ¯å·²ç¥è®¾å®æ¸©åº¦ 
          st.subheader("ååµç©çä¿¡æ¯å¼ºåå­¦ä¹ ")
          #ç©ºæ°è´¨éææ è®¾å®å¼
          #ç©ºæ°è°èæ­¥é¿ï¼
          st.selectbox("éæ©ç®æ³", options=['Double-DQN', 'Policy Gradient', 'Intrinsic Curiosity Module', 'Deep Q learning'])
          start_opt = st.button("ä¸é®ä¼å")

          #è½è
          df = pd.DataFrame(dict(
                    Time = ['08:00', '08:10', '08:20', '08:30', '08:40', '08:50', 
                    '09:00', '09:10', '09:20', '09:30', '09:40', '09:50', 
                    '10:00', '10:10', '10:20', '10:30', '10:40', '10:50', 
                    '11:00', '11:10', '11:20', '11:30', '11:40', '11:50'],
                    ))
          df['åæ¬è¿è¡è½è(kW)'] = np.random.randint(low=100, high=1000, size=24)
          df["åæ¬è¿è¥è¾¾æ ç¨åº¦(%)"] = np.random.randint(low=89, high=100, size=24)

          df['æ°è½æºåçµé(kW)'] = np.random.randint(low=30, high=60, size=24)
          #åä¼åçµéï¼èçè½è

          if start_opt:
                st.markdown("å¸åæ¥å¼ºåè¿è¥æ§è½")
                df['å¼ºåè¿è¡è½è(kW)'] = [ i - np.random.randint(low=-10, high=20) for i in df['åæ¬è¿è¡è½è(kW)']]
                df["å¼ºåè¿è¥ç¯å¢è¾¾æ ç¨åº¦(%)"] = np.random.randint(low=84, high=100, size=24)
                df['å¼ºåè¿è¥èè½æ¶ç(Â¥)'] = (df['æ°è½æºåçµé(kW)'] + (df['åæ¬è¿è¡è½è(kW)'] - df['å¼ºåè¿è¡è½è(kW)'])) * 0.617

                st.session_state.fig_pv = px.line(df, x='Time', y = 'æ°è½æºåçµé(kW)', title='æ°è½æºåçµåå')
                st.session_state.fig_profit = px.line(df, x='Time', y = 'å¼ºåè¿è¥èè½æ¶ç(Â¥)', title='å¼ºåè¿è¥æ¶çåå')
                

                col1, col2 = st.columns(2)
                with col1:
                    st.markdown('##### è½èè¿è¡å¯¹æ¯')
                    st.bar_chart(df, x='Time', y = ['åæ¬è¿è¡è½è(kW)','å¼ºåè¿è¡è½è(kW)'])
                    st.markdown('##### æ°è½æºäº§è½')
                    st.line_chart(df, x='Time', y = 'æ°è½æºåçµé(kW)')
                    #st.plotly_chart(st.session_state.fig_cost, use_container_width=True)  
                with col2:
                    st.markdown("##### ç¯å¢ææ è¾¾æ åº¦")
                    st.line_chart(df, x='Time', y = ['åæ¬è¿è¥è¾¾æ ç¨åº¦(%)','å¼ºåè¿è¥ç¯å¢è¾¾æ ç¨åº¦(%)'])
                    st.markdown("##### å¯æç»­æ§èè½æ¶ç")
                    st.area_chart(df, x='Time', y = 'å¼ºåè¿è¥èè½æ¶ç(Â¥)', )
                    #st.plotly_chart(st.session_state.fig_acc, use_container_width=True)
                
                
                

                




          #è¿è¥è¾¾æ ç¨åº¦
          
#df = pd.read_csv("Thermal_Demand.csv")
#st.write(df)




#with 

