import streamlit as st 

st.markdown("# 💨 空气质量设计模块")
st.sidebar.markdown("# 💨 Air Quality Design Module")
st.markdown("设计空气洁净度需求，快速衡量医院不同区域在典型日不同时刻所需的新风量与换热量")
import plotly.express as px
import pandas as pd


with st.expander("病房区域I 空气质量设计"):
          room_V = st.number_input("病房区域I 空间体积(m3)", value=210)
          initial_T = st.number_input("病房区域I 初始温度(C)", value=23)
          initial_ppm = st.number_input("病房区域I 初始产生CO2浓度(ppm)", value=600)
          initial_W = st.number_input("病房区域I 初始循环风量(m3/h)", value=3000)#m3/h 
          df = pd.DataFrame(dict(
                    Time = ['08:00', '08:10', '08:20', '08:30', '08:40', '08:50', 
                    '09:00', '09:10', '09:20', '09:30', '09:40', '09:50', 
                    '10:00', '10:10', '10:20', '10:30', '10:40', '10:50', 
                    '11:00', '11:10', '11:20', '11:30', '11:40', '11:50'],
                    Temperatures = [20, 20.1, 20.1, 20.4, 20.5, 20.6,
                    21, 21.1, 20, 21.4, 20.5, 20.6,
                    22, 22, 21.6, 21.4, 22.5, 21.9,
                    22.5, 22.7, 22.3, 23, 23.2, 23.6],
                    Populations = [12, 12, 12, 20, 20, 20,
                    12, 12, 12, 12, 16, 16,
                    17, 17, 17, 17, 20, 20,
                    19, 12, 12, 18, 18, 18
                    ],


                    ))
          df['室外温度(C)'] = [20, 20.1, 20.1, 20.4, 20.5, 20.6, 21, 21.1, 20, 21.4, 20.5, 20.6, 22, 22, 21.6, 21.4, 22.5, 21.9, 22.5, 22.7, 22.3, 23, 23.2, 23.6]
          df['室外温度(C)'] = df['室外温度(C)'] + 4
          df['Temperatures'] = df['Temperatures'] + 3 
          df['产生CO2浓度(ppm)'] = 0.0144 * df['Populations'] / room_V * 10e6
          df['室内含热量(kJ)'] = initial_T * room_V * 1.003 * 1.29 + 0.44 * df['Populations'] * 154 * 600/1000 + initial_W/6 * (df['室外温度(C)'] - initial_T) * 1.29 * 1.004 #循环风项得先把风量单位调到十分钟

          #with st.expander("场景情况"):

          st.markdown('## 上午场景条件')
          df_schedule = pd.DataFrame([
          dict(Task="Patient", Start='2022-04-15 08:00', Finish='2022-04-15 12:00', Resource="Patient", Number=12),
          dict(Task="Nurse 1", Start='2022-04-15 08:30', Finish='2022-04-15 09:30', Resource="Nurse", Number=8),
          dict(Task="Doctor", Start='2022-04-15 10:00', Finish='2022-04-15 11:20', Resource="Doctor", Number=4),
          dict(Task="Nurse 2", Start='2022-04-15 10:40', Finish='2022-04-15 10:50', Resource="Nurse", Number=8),
          dict(Task="Visitor", Start='2022-04-15 11:30', Finish='2022-04-15 11:50', Resource="Visitor", Number=6),

          ])

          fig = px.timeline(df_schedule, x_start="Start", x_end="Finish", y="Resource", color="Number", title="病房人员进出安排")
          st.plotly_chart(fig, use_container_width=True)
          col1, col2 = st.columns(2)

          with col1:

                    fig = px.line(df, x="Time", y="室内含热量(kJ)", title= "室内含热量预测(kJ)", height=300) 
                    st.plotly_chart(fig,use_container_width=True)

          with col2:

                    fig = px.line(df, x="Time", y="产生CO2浓度(ppm)", title= "CO2浓度预测(ppm)", height=300) 
                    st.plotly_chart(fig,use_container_width=True)

          st.markdown("# 设定值与能量需求")

          objectif_ppm = st.number_input("病房区域I ppm要求设定值", value=800, step=150)
          outdoor_ppm = st.number_input("病房区域I 室外CO2浓度估值", value = 300, step=150)
          objectif_T = st.number_input("病房区域I 温度设定值", value=25)

          #十分钟内需要达到的
          ##需求新风量= V * (前后室内浓度差/过去时长(秒))/(室外浓度-当前室内浓度)/ 那一时刻需要的新风量，而不是累计需要的新风量

          need_air = []
          for i in range(len(df['产生CO2浓度(ppm)'])):
                    need_air.append( room_V * ( (- df['产生CO2浓度(ppm)'][i] + objectif_ppm)/600) / (outdoor_ppm - df['产生CO2浓度(ppm)'][i]) )
          df['需求新风量(m3/h)'] = need_air 
          df['需求新风量(m3/h)'] = df['需求新风量(m3/h)'] * 3600

          #热量调节需求 = 

          df['热量调节需求(kW)'] = [ df['需求新风量(m3/h)'][i] * (df['室外温度(C)'][i] - df['Temperatures'][i])* 600 /3600 + (objectif_T - df['Temperatures'][i]) * 1.29 * 1.004 * room_V for i in range(len(df['室外温度(C)']))]

          col3, col4 = st.columns(2)


          with col3:
                    st.markdown('### 不同时刻需求新风量(m3/h)')
                    st.area_chart(df, y='需求新风量(m3/h)', use_container_width=True)


          with col4:
                    st.markdown('### 不同时刻热量调节需求(kW)')
                    st.area_chart(df, y='热量调节需求(kW)', use_container_width=True)

          df.to_csv("Patient_Zone_I_Thermal_Demand.csv")

with st.expander("病房区域II 空气质量设计"):
          room_V = st.number_input("病房区域II 空间体积(m3)", value=210)
          initial_T = st.number_input("病房区域II 初始温度(C)", value=23)
          initial_ppm = st.number_input("病房区域II 初始产生CO2浓度(ppm)", value=600)
          initial_W = st.number_input("病房区域II 初始循环风量(m3/h)", value=3000)#m3/h 
          df = pd.DataFrame(dict(
                    Time = ['08:00', '08:10', '08:20', '08:30', '08:40', '08:50', 
                    '09:00', '09:10', '09:20', '09:30', '09:40', '09:50', 
                    '10:00', '10:10', '10:20', '10:30', '10:40', '10:50', 
                    '11:00', '11:10', '11:20', '11:30', '11:40', '11:50'],
                    Temperatures = [20, 20.1, 20.1, 20.4, 20.5, 20.6,
                    21, 21.1, 20, 21.4, 20.5, 20.6,
                    22, 22, 21.6, 21.4, 22.5, 21.9,
                    22.5, 22.7, 22.3, 23, 23.2, 23.6],
                    Populations = [12, 12, 12, 16, 16, 16,
                    20, 20, 20, 16, 16, 16,
                    12, 12, 12, 12, 16, 12,
                    12, 12, 15, 15, 15, 12
                    ],


                    ))
          df['室外温度(C)'] = [20, 20.1, 20.1, 20.4, 20.5, 20.6, 21, 21.1, 20, 21.4, 20.5, 20.6, 22, 22, 21.6, 21.4, 22.5, 21.9, 22.5, 22.7, 22.3, 23, 23.2, 23.6]
          df['室外温度(C)'] = df['室外温度(C)'] + 4
          df['Temperatures'] = df['Temperatures'] + 3 
          df['产生CO2浓度(ppm)'] = 0.0144 * df['Populations'] / room_V * 10e6
          df['室内含热量(kJ)'] = initial_T * room_V * 1.003 * 1.29 + 0.44 * df['Populations'] * 154 * 600/1000 + initial_W/6 * (df['室外温度(C)'] - initial_T) * 1.29 * 1.004 #循环风项得先把风量单位调到十分钟

          #with st.expander("场景情况"):

          st.markdown('## 上午场景条件')
          df_schedule = pd.DataFrame([
          dict(Task="Patient", Start='2022-04-15 08:00', Finish='2022-04-15 12:00', Resource="Patient", Number=12),
          dict(Task="Nurse 1", Start='2022-04-15 08:30', Finish='2022-04-15 09:30', Resource="Nurse", Number=4),
          dict(Task="Doctor", Start='2022-04-15 9:00', Finish='2022-04-15 10:00', Resource="Doctor", Number=4),
          dict(Task="Nurse 2", Start='2022-04-15 10:40', Finish='2022-04-15 10:50', Resource="Nurse", Number=4),
          dict(Task="Visitor", Start='2022-04-15 11:30', Finish='2022-04-15 11:50', Resource="Visitor", Number=3),

          ])

          fig = px.timeline(df_schedule, x_start="Start", x_end="Finish", y="Resource", color="Number", title="病房人员进出安排")
          st.plotly_chart(fig, use_container_width=True)
          col1, col2 = st.columns(2)

          with col1:

                    fig = px.line(df, x="Time", y="室内含热量(kJ)", title= "室内含热量预测(kJ)", height=300) 
                    st.plotly_chart(fig,use_container_width=True)

          with col2:

                    fig = px.line(df, x="Time", y="产生CO2浓度(ppm)", title= "CO2浓度预测(ppm)", height=300) 
                    st.plotly_chart(fig,use_container_width=True)

          st.markdown("# 设定值与能量需求")

          objectif_ppm = st.number_input("病房区域II ppm要求设定值", value=800, step=150)
          outdoor_ppm = st.number_input("病房区域II 室外CO2浓度估值", value = 300, step=150)
          objectif_T = st.number_input("病房区域II 温度设定值", value=25)

          #十分钟内需要达到的
          ##需求新风量= V * (前后室内浓度差/过去时长(秒))/(室外浓度-当前室内浓度)/ 那一时刻需要的新风量，而不是累计需要的新风量

          need_air = []
          for i in range(len(df['产生CO2浓度(ppm)'])):
                    need_air.append( room_V * ( (- df['产生CO2浓度(ppm)'][i] + objectif_ppm)/600) / (outdoor_ppm - df['产生CO2浓度(ppm)'][i]) )
          df['需求新风量(m3/h)'] = need_air 
          df['需求新风量(m3/h)'] = df['需求新风量(m3/h)'] * 3600

          #热量调节需求 = 

          df['热量调节需求(kW)'] = [ df['需求新风量(m3/h)'][i] * (df['室外温度(C)'][i] - df['Temperatures'][i])* 600 /3600 + (objectif_T - df['Temperatures'][i]) * 1.29 * 1.004 * room_V for i in range(len(df['室外温度(C)']))]

          col3, col4 = st.columns(2)


          with col3:
                    st.markdown('### 不同时刻需求新风量(m3/h)')
                    st.area_chart(df, y='需求新风量(m3/h)', use_container_width=True)


          with col4:
                    st.markdown('### 不同时刻热量调节需求(kW)')
                    st.area_chart(df, y='热量调节需求(kW)', use_container_width=True)

          df.to_csv("Patient_Zone_II_Thermal_Demand.csv")

with st.expander("办公区域 空气质量设计"):
          room_V = st.number_input("办公区域 空间体积(m3)", value=1190)
          initial_T = st.number_input("办公区域 初始温度(C)", value=23)
          initial_ppm = st.number_input("办公区域 初始产生CO2浓度(ppm)", value=600)
          initial_W = st.number_input("办公区域 初始循环风量(m3/h)", value=3000)#m3/h 
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
          df['室外温度(C)'] = [20, 20.1, 20.1, 20.4, 20.5, 20.6, 21, 21.1, 20, 21.4, 20.5, 20.6, 22, 22, 21.6, 21.4, 22.5, 21.9, 22.5, 22.7, 22.3, 23, 23.2, 23.6]
          df['室外温度(C)'] = df['室外温度(C)'] + 4
          df['Temperatures'] = df['Temperatures'] + 3 
          df['产生CO2浓度(ppm)'] = 0.0144 * df['Populations'] / room_V * 10e6
          df['室内含热量(kJ)'] = initial_T * room_V * 1.003 * 1.29 + 0.44 * df['Populations'] * 154 * 600/1000 + initial_W/6 * (df['室外温度(C)'] - initial_T) * 1.29 * 1.004 #循环风项得先把风量单位调到十分钟

          st.markdown('## 上午场景条件')
          df_schedule = pd.DataFrame([
          dict(Task="Doctor 1", Start='2022-04-15 08:30', Finish='2022-04-15 09:30', Resource="Doctor", Number=6),
          dict(Task="Nurse 1", Start='2022-04-15 9:00', Finish='2022-04-15 10:00', Resource="Nurse", Number=7),
          dict(Task="Doctor 2", Start='2022-04-15 10:20', Finish='2022-04-15 10:50', Resource="Doctor", Number=6),
          dict(Task="Nurse 2", Start='2022-04-15 11:00', Finish='2022-04-15 11:50', Resource="Nurse", Number=9),
          ])

          fig = px.timeline(df_schedule, x_start="Start", x_end="Finish", y="Resource", color="Number", title="病房人员进出安排")
          st.plotly_chart(fig, use_container_width=True)
          col1, col2 = st.columns(2)

          with col1:

                    fig = px.line(df, x="Time", y="室内含热量(kJ)", title= "室内含热量预测(kJ)", height=300) 
                    st.plotly_chart(fig,use_container_width=True)

          with col2:

                    fig = px.line(df, x="Time", y="产生CO2浓度(ppm)", title= "CO2浓度预测(ppm)", height=300) 
                    st.plotly_chart(fig,use_container_width=True)

          st.markdown("# 设定值与能量需求")

          objectif_ppm = st.number_input("办公区域 ppm要求设定值", value=800, step=150)
          outdoor_ppm = st.number_input("办公区域 室外CO2浓度估值", value = 300, step=150)
          objectif_T = st.number_input("办公区域 温度设定值", value=25)

          #十分钟内需要达到的
          ##需求新风量= V * (前后室内浓度差/过去时长(秒))/(室外浓度-当前室内浓度)/ 那一时刻需要的新风量，而不是累计需要的新风量

          need_air = []
          for i in range(len(df['产生CO2浓度(ppm)'])):
                    need_air.append( room_V * ( (- df['产生CO2浓度(ppm)'][i] + objectif_ppm)/600) / (outdoor_ppm - df['产生CO2浓度(ppm)'][i]) )
          df['需求新风量(m3/h)'] = need_air 
          df['需求新风量(m3/h)'] = df['需求新风量(m3/h)'] * 3600

          #热量调节需求 = 

          df['热量调节需求(kW)'] = [ df['需求新风量(m3/h)'][i] * (df['室外温度(C)'][i] - df['Temperatures'][i])* 600 /3600 + (objectif_T - df['Temperatures'][i]) * 1.29 * 1.004 * room_V for i in range(len(df['室外温度(C)']))]

          col3, col4 = st.columns(2)


          with col3:
                    st.markdown('### 不同时刻需求新风量(m3/h)')
                    st.area_chart(df, y='需求新风量(m3/h)', use_container_width=True)


          with col4:
                    st.markdown('### 不同时刻热量调节需求(kW)')
                    st.area_chart(df, y='热量调节需求(kW)', use_container_width=True)

          df.to_csv("Office_Zone_Thermal_Demand.csv")

with st.expander("公共走廊区域 空气质量设计"):
          room_V = st.number_input("公共走廊 空间体积(m3)", value=1071)
          initial_T = st.number_input("公共走廊区域 空初始温度(C)", value=23)
          initial_ppm = st.number_input("公共走廊区域 空初始产生CO2浓度(ppm)", value=600)
          initial_W = st.number_input("公共走廊区域 空初始循环风量(m3/h)", value=3000)#m3/h 
          df = pd.DataFrame(dict(
                    Time = ['08:00', '08:10', '08:20', '08:30', '08:40', '08:50', 
                    '09:00', '09:10', '09:20', '09:30', '09:40', '09:50', 
                    '10:00', '10:10', '10:20', '10:30', '10:40', '10:50', 
                    '11:00', '11:10', '11:20', '11:30', '11:40', '11:50'],
                    Temperatures = [20, 20.1, 20.1, 20.4, 20.5, 20.6,
                    21, 21.1, 20, 21.4, 20.5, 20.6,
                    22, 22, 21.6, 21.4, 22.5, 21.9,
                    22.5, 22.7, 22.3, 23, 23.2, 23.6],
                    Populations = [8, 8, 5, 5, 5, 5,
                    5, 5, 5, 5, 5, 5,
                    6, 6, 8, 8, 10, 10,
                    6, 6, 6, 6, 7+6, 7+6
                    ],
                    ))
          df['室外温度(C)'] = [20, 20.1, 20.1, 20.4, 20.5, 20.6, 21, 21.1, 20, 21.4, 20.5, 20.6, 22, 22, 21.6, 21.4, 22.5, 21.9, 22.5, 22.7, 22.3, 23, 23.2, 23.6]
          df['室外温度(C)'] = df['室外温度(C)'] + 4
          df['Temperatures'] = df['Temperatures'] + 3 
          df['产生CO2浓度(ppm)'] = 0.0144 * df['Populations'] / room_V * 10e6
          df['室内含热量(kJ)'] = initial_T * room_V * 1.003 * 1.29 + 0.44 * df['Populations'] * 154 * 600/1000 + initial_W/6 * (df['室外温度(C)'] - initial_T) * 1.29 * 1.004 #循环风项得先把风量单位调到十分钟

          #with st.expander("场景情况"):

          st.markdown('## 上午场景条件')
          df_schedule = pd.DataFrame([
          dict(Task="Patient 1", Start='2022-04-15 08:00', Finish='2022-04-15 8:20', Resource="Patient", Number=3),
          dict(Task="Doctor 1", Start='2022-04-15 08:20', Finish='2022-04-15 09:30', Resource="Doctor", Number=2),
          dict(Task="Nurse 1", Start='2022-04-15 8:00', Finish='2022-04-15 10:00', Resource="Nurse", Number=3),
          dict(Task="Doctor 2", Start='2022-04-15 10:20', Finish='2022-04-15 10:50', Resource="Doctor", Number=2),
          dict(Task="Patient 2", Start='2022-04-15 10:00', Finish='2022-04-15 12:00', Resource="Patient", Number=6),
          dict(Task="Visitor 1", Start='2022-04-15 10:30', Finish='2022-04-15 10:50', Resource="Visitor", Number=2),
          dict(Task="Nurse 2", Start='2022-04-15 11:40', Finish='2022-04-15 11:50', Resource="Nurse", Number=7),
          dict(Task="Visitor 2", Start='2022-04-15 11:30', Finish='2022-04-15 11:50', Resource="Visitor", Number=6)
          ])

          fig = px.timeline(df_schedule, x_start="Start", x_end="Finish", y="Resource", color="Number", title="病房人员进出安排")
          st.plotly_chart(fig, use_container_width=True)
          col1, col2 = st.columns(2)

          with col1:

                    fig = px.line(df, x="Time", y="室内含热量(kJ)", title= "室内含热量预测(kJ)", height=300) 
                    st.plotly_chart(fig,use_container_width=True)

          with col2:

                    fig = px.line(df, x="Time", y="产生CO2浓度(ppm)", title= "CO2浓度预测(ppm)", height=300) 
                    st.plotly_chart(fig,use_container_width=True)

          st.markdown("# 设定值与能量需求")

          objectif_ppm = st.number_input("公共走廊区域 空ppm要求设定值", value=800, step=150)
          outdoor_ppm = st.number_input("公共走廊区域 空室外CO2浓度估值", value = 300, step=150)
          objectif_T = st.number_input("公共走廊区域 空温度设定值", value=25)

          #十分钟内需要达到的
          ##需求新风量= V * (前后室内浓度差/过去时长(秒))/(室外浓度-当前室内浓度)/ 那一时刻需要的新风量，而不是累计需要的新风量

          need_air = []
          for i in range(len(df['产生CO2浓度(ppm)'])):
                    need_air.append( room_V * ( (- df['产生CO2浓度(ppm)'][i] + objectif_ppm)/600) / (outdoor_ppm - df['产生CO2浓度(ppm)'][i]) )
          df['需求新风量(m3/h)'] = need_air 
          df['需求新风量(m3/h)'] = df['需求新风量(m3/h)'] * 3600

          #热量调节需求 = 

          df['热量调节需求(kW)'] = [ df['需求新风量(m3/h)'][i] * (df['室外温度(C)'][i] - df['Temperatures'][i])* 600 /3600 + (objectif_T - df['Temperatures'][i]) * 1.29 * 1.004 * room_V for i in range(len(df['室外温度(C)']))]

          col3, col4 = st.columns(2)


          with col3:
                    st.markdown('### 不同时刻需求新风量(m3/h)')
                    st.area_chart(df, y='需求新风量(m3/h)', use_container_width=True)


          with col4:
                    st.markdown('### 不同时刻热量调节需求(kW)')
                    st.area_chart(df, y='热量调节需求(kW)', use_container_width=True)

          df.to_csv("Public_Hallway_Zone_Thermal_Demand.csv")

with st.expander("娱乐活动区域 空气质量设计"):
          room_V = st.number_input("娱乐活动区域 空间体积(m3)", value=420)
          initial_T = st.number_input("娱乐活动区域 空初始温度(C)", value=23)
          initial_ppm = st.number_input("娱乐活动区域 空初始产生CO2浓度(ppm)", value=600)
          initial_W = st.number_input("娱乐活动区域 空初始循环风量(m3/h)", value=3000)#m3/h 
          df = pd.DataFrame(dict(
                    Time = ['08:00', '08:10', '08:20', '08:30', '08:40', '08:50', 
                    '09:00', '09:10', '09:20', '09:30', '09:40', '09:50', 
                    '10:00', '10:10', '10:20', '10:30', '10:40', '10:50', 
                    '11:00', '11:10', '11:20', '11:30', '11:40', '11:50'],
                    Temperatures = [20, 20.1, 20.1, 20.4, 20.5, 20.6,
                    21, 21.1, 20, 21.4, 20.5, 20.6,
                    22, 22, 21.6, 21.4, 22.5, 21.9,
                    22.5, 22.7, 22.3, 23, 23.2, 23.6],
                    Populations = [5, 5, 5, 5, 5, 1,
                    0, 0, 1, 1, 1, 1,
                    4, 2,2 , 2, 3, 3,
                    1, 1, 1, 3, 1+1, 1+1
                    ],
                    ))
          df['室外温度(C)'] = [20, 20.1, 20.1, 20.4, 20.5, 20.6, 21, 21.1, 20, 21.4, 20.5, 20.6, 22, 22, 21.6, 21.4, 22.5, 21.9, 22.5, 22.7, 22.3, 23, 23.2, 23.6]
          df['室外温度(C)'] = df['室外温度(C)'] + 4
          df['Temperatures'] = df['Temperatures'] + 3 
          df['产生CO2浓度(ppm)'] = 0.0144 * df['Populations'] / room_V * 10e6
          df['室内含热量(kJ)'] = initial_T * room_V * 1.003 * 1.29 + 0.44 * df['Populations'] * 154 * 600/1000 + initial_W/6 * (df['室外温度(C)'] - initial_T) * 1.29 * 1.004 #循环风项得先把风量单位调到十分钟

          #with st.expander("场景情况"):

          st.markdown('## 上午场景条件')
          df_schedule = pd.DataFrame([
          dict(Task="Patient 1", Start='2022-04-15 08:00', Finish='2022-04-15 8:40', Resource="Patient", Number=4),
          dict(Task="Nurse 1", Start='2022-04-15 8:00', Finish='2022-04-15 8:50', Resource="Nurse", Number=1),
          dict(Task="Patient 2", Start='2022-04-15 10:20', Finish='2022-04-15 10:50', Resource="Patient", Number=3),
          dict(Task="Visitor 1", Start='2022-04-15 9:30', Finish='2022-04-15 9:50', Resource="Visitor", Number=2),
          dict(Task="Nurse 2", Start='2022-04-15 11:20', Finish='2022-04-15 11:50', Resource="Nurse", Number=1),
          dict(Task="Visitor 2", Start='2022-04-15 10:45', Finish='2022-04-15 11:50', Resource="Visitor", Number=1)
          ])

          fig = px.timeline(df_schedule, x_start="Start", x_end="Finish", y="Resource", color="Number", title="病房人员进出安排")
          st.plotly_chart(fig, use_container_width=True)
          col1, col2 = st.columns(2)

          with col1:

                    fig = px.line(df, x="Time", y="室内含热量(kJ)", title= "室内含热量预测(kJ)", height=300) 
                    st.plotly_chart(fig,use_container_width=True)

          with col2:

                    fig = px.line(df, x="Time", y="产生CO2浓度(ppm)", title= "CO2浓度预测(ppm)", height=300) 
                    st.plotly_chart(fig,use_container_width=True)

          st.markdown("# 设定值与能量需求")

          objectif_ppm = st.number_input("娱乐活动区域 空ppm要求设定值", value=800, step=150)
          outdoor_ppm = st.number_input("娱乐活动区域 空室外CO2浓度估值", value = 300, step=150)
          objectif_T = st.number_input("娱乐活动区域 空温度设定值", value=25)

          #十分钟内需要达到的
          ##需求新风量= V * (前后室内浓度差/过去时长(秒))/(室外浓度-当前室内浓度)/ 那一时刻需要的新风量，而不是累计需要的新风量

          need_air = []
          for i in range(len(df['产生CO2浓度(ppm)'])):
                    need_air.append( room_V * ( (- df['产生CO2浓度(ppm)'][i] + objectif_ppm)/600) / (outdoor_ppm - df['产生CO2浓度(ppm)'][i]) )
          df['需求新风量(m3/h)'] = need_air 
          df['需求新风量(m3/h)'] = df['需求新风量(m3/h)'] * 3600

          #热量调节需求 = 

          df['热量调节需求(kW)'] = [ df['需求新风量(m3/h)'][i] * (df['室外温度(C)'][i] - df['Temperatures'][i])* 600 /3600 + (objectif_T - df['Temperatures'][i]) * 1.29 * 1.004 * room_V for i in range(len(df['室外温度(C)']))]

          col3, col4 = st.columns(2)


          with col3:
                    st.markdown('### 不同时刻需求新风量(m3/h)')
                    st.area_chart(df, y='需求新风量(m3/h)', use_container_width=True)


          with col4:
                    st.markdown('### 不同时刻热量调节需求(kW)')
                    st.area_chart(df, y='热量调节需求(kW)', use_container_width=True)

          df.to_csv("Activity_Zone_Thermal_Demand.csv")