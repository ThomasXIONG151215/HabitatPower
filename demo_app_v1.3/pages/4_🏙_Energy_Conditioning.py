import streamlit as st

from components.elements import dashboard 
from streamlit_elements import elements, mui, html
st.markdown("# 🏙 能源运营调节模块")
st.sidebar.markdown("# 🏙 Energy Operational Conditioning Module")
st.markdown("执行医院系统的物理场仿真模拟并不同需求实时策划出最优的资源调配")

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
        { "field": 'space', "headerName": '空间名称', "width": 90 },
        { "field": 'volume', "headerName": '空间体积(m3)', "width": 150, "editable": True, },
        { "field": 'space_heat_capacitance', "headerName": '空间热容(kJ/K)',  "width": 110, "editable": True, },
        { "field": 'envelope_heat_resistance', "headerName": '围护体热阻(K/kW)',  "width": 110, "editable": True, },
        { "field": 'neighbor_heat_conductance', "headerName": '近邻热感(K/(H.kJ))',  "width": 110, "editable": True, },
        { "field": 'average_heat_load', "headerName": '典型热负荷(kJ)',  "width": 110, "editable": True, },
        { "field": 'average_fresh_air_demand', "headerName": '典型需求新风量(m3/h)',  "width": 110, "editable": True, },
    ]

END_DEVICE_MANAGEMENT_COLUMNS = [ #一台主机(多联机室外机or水系统)一个
        { "field": 'id', "headerName": 'ID', "width": 90 },
        { "field": 'end_device', "headerName": '末端代号', "width": 90 },
        { "field": 'cooling_capacity', "headerName": '额定制冷量(kW)', "width": 150, "editable": False, },
        { "field": 'heating_capacity', "headerName": '额定制热量(kW)',  "width": 110, "editable": False, },
        { "field": 'fresh_air_capacity', "headerName": '额定循环风量(m3/h)',  "width": 110, "editable": False, },
        { "field": 'fresh_air_power_use', "headerName": '风机运行功率(kW)',  "width": 110, "editable": False, },

        { "field": 'cooling_task', "headerName": '指定制冷量(kW)', "width": 150, "editable": True, },
        { "field": 'heating_task', "headerName": '指定制热量(kW)',  "width": 110, "editable": True, },
        { "field": 'fresh_air_task', "headerName": '指定循环风量(m3/h)',  "width": 110, "editable": True, },
        { "field": 'substance_ratio', "headerName": '冷媒开度(%)',  "width": 110, "editable": True, },
        { "field": 'frequency', "headerName": '风机运行频率(Hz)',  "width": 110, "editable": True, },
    ]

MAIN_DEVICE_COLUMNS = [ #一台主机(多联机室外机or水系统)一个
        { "field": 'id', "headerName": 'ID', "width": 90 },
        { "field": 'main_device', "headerName": '主机代号', "width": 90 },
        { "field": 'cooling_capacity', "headerName": '额定制冷量(kW)', "width": 150, "editable": False, },
        { "field": 'heating_capacity', "headerName": '额定制热量(kW)',  "width": 110, "editable": False, },
        { "field": 'cooling_power_use', "headerName": '制冷COP',  "width": 110, "editable": False, },
        { "field": 'heating_power_use', "headerName": '制热COP',  "width": 110, "editable": False, },

        { "field": 'cooling_task', "headerName": '指定总制冷量(kW)', "width": 150, "editable": True, },
        { "field": 'heating_task', "headerName": '指定总制热量(kW)',  "width": 110, "editable": True, },
    ]


SPACE_ROWS = [
        { "id": 1, "space": '病房区域I', "volume": 210, "space_heat_capacitance": 35, "envelope_heat_resistance": 1.3 , 'neighbor_heat_conductance': 2.1, 'average_heat_load':1200, 'average_fresh_air_demand': 13000},
        { "id": 2, "space": '病房区域II', "volume": 210, "space_heat_capacitance": 42, "envelope_heat_resistance": 1.3 , 'neighbor_heat_conductance': 2.1, 'average_heat_load':600, 'average_fresh_air_demand': 15000},
        { "id": 3, "space": '办公区域', "volume": 1190, "space_heat_capacitance": 45, "envelope_heat_resistance": 1.3 , 'neighbor_heat_conductance': 2.1, 'average_heat_load':2500, 'average_fresh_air_demand': 4000},
        { "id": 4, "space": '公共走廊', "volume": 1071, "space_heat_capacitance": 16, "envelope_heat_resistance": 1.3 , 'neighbor_heat_conductance': 2.1, 'average_heat_load':700, 'average_fresh_air_demand': 5600},
        { "id": 5, "space": '娱乐活动区', "volume": 420, "space_heat_capacitance": 32, "envelope_heat_resistance": 1.3 , 'neighbor_heat_conductance': 2.1, 'average_heat_load':2100, 'average_fresh_air_demand': 13020},
    ]

END_ROWS = [
        {"id": 1, "end_device": "室内机I", "cooling_capacity": 3.2, "heating_capacity": 2.3, "fresh_air_capacity": 12000, "fresh_air_power_use": 32, "cooling_task": 34, "heating_task":50, "fresh_air_task": 3000, "substance_ratio":30, "frequency":33},
        {"id": 2, "end_device": "室内机II", "cooling_capacity": 3.2, "heating_capacity": 2.3, "fresh_air_capacity": 12000, "fresh_air_power_use": 32, "cooling_task": 34, "heating_task":50, "fresh_air_task": 3000, "substance_ratio":30, "frequency":33},
        {"id": 3, "end_device": "室内机III", "cooling_capacity": 3.2, "heating_capacity": 2.3, "fresh_air_capacity": 12000, "fresh_air_power_use": 32, "cooling_task": 34, "heating_task":50, "fresh_air_task": 3000, "substance_ratio":30, "frequency":33},
        {"id": 4, "end_device": "室内机IV", "cooling_capacity": 3.2, "heating_capacity": 2.3, "fresh_air_capacity": 12000, "fresh_air_power_use": 32, "cooling_task": 34, "heating_task":50, "fresh_air_task": 3000, "substance_ratio":30, "frequency":33},
        {"id": 5, "end_device": "室内机V", "cooling_capacity": 3.2, "heating_capacity": 2.3, "fresh_air_capacity": 12000, "fresh_air_power_use": 32, "cooling_task": 34, "heating_task":50, "fresh_air_task": 3000, "substance_ratio":30, "frequency":33}
]

MAIN_ROWS = [
        {"id": 1, "main_device": "多联主机", "cooling_capacity": 21.2, "heating_capacity": 20.3, "cooling_power_use": 4.3, "heating_power_use": 3.2, "cooling_task": 2234, "heating_task": 1500},
]


HEAT_LOAD_PIE = [
        { "id": 1, "label": "病房区域I", "value": SPACE_ROWS[0]["average_heat_load"], "color": "hsl(12, 40%, 20%)" },
        { "id": 2, "label": "病房区域II", "value": SPACE_ROWS[1]["average_heat_load"], "color": "hsl(178, 70%, 50%)" },
        { "id": 3, "label": "办公区域", "value": SPACE_ROWS[2]["average_heat_load"], "color": "hsl(322, 70%, 50%)" },
        { "id": 4, "label": "公共走廊", "value": SPACE_ROWS[3]["average_heat_load"], "color": "hsl(117, 70%, 50%)" },
        { "id": 5, "label": "娱乐活动区", "value": SPACE_ROWS[4]["average_heat_load"], "color": "hsl(286, 70%, 50%)" }
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

with st.expander("项目信息总汇"):
        
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

with st.expander("热交互统计模拟"):
          st.subheader("热交互统计模拟")
          st.file_uploader("上传历史数据 (时间段-各区域温湿度变化-室外温湿度辐照值-设备参数与能耗情况)") #辐照值和室外温度帮助预估发电量
          start_sim = st.button("一键仿真")
          #参数拟合结果， 仿真精确度
          
          df_parameters = pd.DataFrame({
                    '空间区域': ['病房区域I', '病房区域II', '办公区域', '公共走廊', '娱乐活动区'],
                    '空间热容(kJ/K)': [100, 100, 120, 80, 30],
                    '围护体热阻(K/kW)': [32, 100, 23, 43, 43],
                    '近邻热感(K/(H.kJ))': [1, 4, 2, 9, 3],
                    })
          df_accuracy = pd.DataFrame({
                    '区块划分': ['环境区块', '系统部件'],
                    '拟合R2': [0.93, 0.97658],
                    '测试R2': [0.91, 0.94321]
                    })
          if start_sim:
                    st.dataframe(df_parameters, use_container_width=True)
                    st.dataframe(df_accuracy, use_container_width=True)
          

with st.expander("强化最优运行"): #最好是已知设定温度 
          st.subheader("内嵌物理信息强化学习")
          #空气质量指标设定值
          #空气调节步长，
          st.selectbox("选择算法", options=['Double-DQN', 'Policy Gradient', 'Intrinsic Curiosity Module', 'Deep Q learning'])
          start_opt = st.button("一键优化")

          #能耗
          df = pd.DataFrame(dict(
                    Time = ['08:00', '08:10', '08:20', '08:30', '08:40', '08:50', 
                    '09:00', '09:10', '09:20', '09:30', '09:40', '09:50', 
                    '10:00', '10:10', '10:20', '10:30', '10:40', '10:50', 
                    '11:00', '11:10', '11:20', '11:30', '11:40', '11:50'],
                    ))
          df['原本运行能耗(kW)'] = np.random.randint(low=100, high=1000, size=24)
          df["原本运营达标程度(%)"] = np.random.randint(low=89, high=100, size=24)

          df['新能源发电量(kW)'] = np.random.randint(low=30, high=60, size=24)
          #光伏发电量，节省能耗

          if start_opt:
                st.markdown("典型日强化运营性能")
                df['强化运行能耗(kW)'] = [ i - np.random.randint(low=-10, high=20) for i in df['原本运行能耗(kW)']]
                df["强化运营环境达标程度(%)"] = np.random.randint(low=84, high=100, size=24)
                df['强化运营节能收益(¥)'] = (df['新能源发电量(kW)'] + (df['原本运行能耗(kW)'] - df['强化运行能耗(kW)'])) * 0.617

                st.session_state.fig_pv = px.line(df, x='Time', y = '新能源发电量(kW)', title='新能源发电变化')
                st.session_state.fig_profit = px.line(df, x='Time', y = '强化运营节能收益(¥)', title='强化运营收益变化')
                

                col1, col2 = st.columns(2)
                with col1:
                    st.markdown('##### 能耗运行对比')
                    st.bar_chart(df, x='Time', y = ['原本运行能耗(kW)','强化运行能耗(kW)'])
                    st.markdown('##### 新能源产能')
                    st.line_chart(df, x='Time', y = '新能源发电量(kW)')
                    #st.plotly_chart(st.session_state.fig_cost, use_container_width=True)  
                with col2:
                    st.markdown("##### 环境指标达标度")
                    st.line_chart(df, x='Time', y = ['原本运营达标程度(%)','强化运营环境达标程度(%)'])
                    st.markdown("##### 可持续性节能收益")
                    st.area_chart(df, x='Time', y = '强化运营节能收益(¥)', )
                    #st.plotly_chart(st.session_state.fig_acc, use_container_width=True)
                
                
                

                




          #运营达标程度
          
#df = pd.read_csv("Thermal_Demand.csv")
#st.write(df)




#with 

