from turtle import width
from cv2 import ROTATE_180
import streamlit as st 

from models.System_Models import Chiller, Pump, Fan, Tower, Exchanger, AHU
from models.Environment_Models import Water_Node, Air_Node, Room, Outdoor
import plotly.graph_objects as go

import sys
sys.path.append('./plotly_digraph_master')
from plotly_dirgraph_master.addEdge import addEdge, addEdge_3D

def app():

    st.markdown('# System modelling test')

    st.markdown('## Input parameters/ Direct Testing')

    pumping_head = 10

    Chiller_Evaporator_Cooling_Rate = 666 #kW
    Chiller_LS_A1 = Chiller(Chiller_Evaporator_Cooling_Rate)
    Chiller_LS_A2 = Chiller(Chiller_Evaporator_Cooling_Rate)

    Chiller_LS_A1.T_w_e_E = 12
    Chiller_LS_A2.T_w_e_E = 12
    Chiller_LS_A1.T_w_e_L = 7
    Chiller_LS_A2.T_w_e_L = 7

    Chiller_LS_A1.T_w_c_E = 32
    Chiller_LS_A2.T_w_c_E = 32
    Chiller_LS_A1.T_w_c_L = 37
    Chiller_LS_A2.T_w_c_L = 37

    #得有cooling pump和chilled pump
    #额定还是设计还是最小还是某频率下的？
    Cooling_Pump_G = 320.5 #t/h/ #过了全程谁处理仪后好像又变成160.2t/h?
    Chilled_Pump_G = 320.5 #t/h
    Cooling_Pump_LD_A1 = Pump(pumping_head)
    Cooling_Pump_LD_A2 = Pump(pumping_head)
    Cooling_Pump_LD_A1.flow_rate = Cooling_Pump_G
    Cooling_Pump_LD_A2.flow_rate = Cooling_Pump_G

    Chilled_Pump_LQ_A1 = Pump(pumping_head)
    Chilled_Pump_LQ_A2 = Pump(pumping_head)
    Chilled_Pump_LQ_A1.flow_rate = Chilled_Pump_G
    Chilled_Pump_LQ_A2.flow_rate = Chilled_Pump_G


    Tower_LT_A1 = Tower()
    Tower_LT_A2 = Tower()

    Tower_LT_A1.Pump = Pump(pumping_head)
    Tower_LT_A2.Pump = Pump(pumping_head)

    Exchanger_1 = Exchanger()
    Exchanger_2 = Exchanger()
    Chilling_Water = Water_Node()
    Supply_Water = Water_Node()
    Return_Water = Water_Node()
    Water_Assembling = Water_Node()
    Water_Distributor = Water_Node()

    Mix_Air_1 = Air_Node()
    Mix_Air_2 = Air_Node()

    Recirculating_Air_A = Air_Node()
    Recirculating_Air_B = Air_Node()

    Air_Distributor_1 = Air_Node()
    Air_Distributor_2 = Air_Node()

    Exhaust_Air = Air_Node()

    Return_Air_A = Air_Node()
    Return_Air_B = Air_Node()

    Supply_Air = Air_Node()

    Outdoor_TK = Outdoor()
    Outdoor_Tower = Outdoor()

    #组合式空调风机情况
    
    G_KT = 88385
    Fan_1 = Fan(G_KT)
    Fan_2 = Fan(G_KT)
    AHU_KT_A1 = AHU(Exchanger_1, Fan_1)
    AHU_KT_A2 = AHU(Exchanger_2, Fan_2)


    #排风凉全都得大雨7200m3/h

    #回排风机 50Hz下设计风量 70385m3/h

    G_HPF = 70385 # 50Hz额定值
    Fan_HPF_A1 = Fan(G_HPF)
    Fan_HPF_B1 = Fan(G_HPF)


    #小新风机50Hz运行工况 18000m3/h
    G_KXF = 18000
    Fan_KXF_A1 = Fan(G_KXF)
    Fan_KXF_B1 = Fan(G_KXF)


    #站厅公共区 86400
    G_PY = 86400 #额定值，具体排量需计算
    Fan_PY_A1 = Fan(G_PY)


    Hall = Room()
    Platform = Room()

    #手动输入运行参数
    #输入参数
    ## 回风温湿度 
    ## 新风温湿度
    ## 水塔温湿度+焓值
    ## 水塔风速
    ## 站内人数分布
    ## 需求制冷量

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('### Demand')
        hall_Q = st.number_input('Hall cooling demand (kW)', step = 10, value = 300) #500#kW 
        platform_Q = st.number_input('Platform cooling demand (kW)', step = 10, value = 300) #kw
    #夸大值

    #总负荷就是两者加起来，虽然只有站台的热量会参与换热

    with col2:
        st.markdown('### Phenomenon')
        ahu_1_T_w_L = st.number_input('Water coming from the heat exchanger (C)', min_value=18, max_value=30, value = 25) #从末端过来的水
        ahu_2_T_w_L = st.number_input('Water coming from the heat exchanger (C)', min_value=18, max_value=30, value = 27) #从末端过来的水

    #室外环境or
    with col3:
        st.markdown('### Outdoor')
        h_a_E = st.number_input('air enthalpy in kW', step = 20, value = 400)#400
        h_as_E = st.number_input('moist air enthalpy in kW', step = 20, value = 500)#500
    G_tower_a = 1000

    if hall_Q + platform_Q < Chiller_LS_A1.Qe_max * 0.85:#暂时只考虑站台和站厅
        #这里是多部件联合控制/因为它们之间存在一定联系
        st.markdown('## Opening One Chiller')


        Chiller_LS_A1.T_w_e_E = 0.5 * (ahu_1_T_w_L + ahu_2_T_w_L) #假设全都往它走
        Chiller_LS_A1.Qe = hall_Q + platform_Q
        #计算出合适的冷冻水泵水速 / 之后可能得换成频率/ 具体需要跟那边人了解
        st.write('LS 1 evaporating water entry temperature (C)', Chiller_LS_A1.T_w_e_E )
        st.write('LS 1 Qe (kW)', hall_Q + platform_Q)
        

        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown('### Cooling Water Control')
            Cooling_Pump_LD_A1.flow_rate = st.slider('Cooling Pump LD 1 flow rate (t/h)', min_value = 150, max_value = 360, value = 281)#280.5 #t/h

            
            #跑一个即可
            Chiller_LS_A1.G_w_e = Cooling_Pump_LD_A1.flow_rate 
            Tower_LT_A1.G_w = Cooling_Pump_LD_A1.flow_rate
            Chiller_LS_A1.Tower = Tower_LT_A1
        with col2:
            st.markdown('### Chiller Control')
            r1 = Chiller_LS_A1.Qe / Chiller_LS_A1.Qe_max
            st.write('LS 1 load ratio', ROTATE_180)
            #estimated最佳Te 和 r
            Te = st.slider('Evaporation Temperature (C)', min_value = 25, max_value = 35, value = 27)
            
        
        
        with col3:
            st.markdown('### Chilled Water Control')
            #estimated最适合T_tower_w_E
            
            T_tower_w_E = 26
            T_tower_w_L = 23

            st.write('Tower entry water temperature (C)', T_tower_w_E)
            st.write('Tower exit water temperature (C)', T_tower_w_L)

            #estimated best Gw,c
            G_w_c = st.slider('Chilled Pump flow rate (t/h)', min_value = 150, max_value = 360, value = 289)

            Chilled_Pump_LQ_A1.flow_rate = G_w_c * 1.2
            Chiller_LS_A1.G_w_c = G_w_c * 1.2

        Cooling_Pump_LD_A1.run_pump(Cooling_Pump_LD_A1.flow_rate)
        Chiller_LS_A1.simple_run(r1, Te, T_tower_w_E, T_tower_w_L)
        Chilled_Pump_LQ_A1.run_pump(Chilled_Pump_LQ_A1.flow_rate)
        #Chilled_Pump_LQ_A2.flow_rate = G_w_c * 0.9
        
        #Chiller_LS_A1.run_core(r1, Te, T_tower_w_E, h_a_E, h_as_E, G_tower_a, Tower_LT_A1.G_w, epsilon = 0.1)

        st.write('Cooling pump power consumption (kW)', Cooling_Pump_LD_A1.Npump )
        st.write('Chiller power consumption (kW)', Chiller_LS_A1.Ncom)
        st.write('Chilled pump power consumption (kW)', Chilled_Pump_LQ_A1.Npump)    
        st.write('Total power consumption (kW)', Cooling_Pump_LD_A1.Npump + Chiller_LS_A1.Ncom + Chilled_Pump_LQ_A1.Npump)    

    elif hall_Q + platform_Q >= Chiller_LS_A1.Qe_max * 0.85:
        st.markdown('## Opening Both Chillers')

        Chiller_LS_A1.T_w_e_E = 0.5 * (ahu_1_T_w_L + ahu_2_T_w_L) #可能需要结合上一时刻的流量
        Chiller_LS_A2.T_w_e_E = 0.5 * (ahu_1_T_w_L + ahu_2_T_w_L)

        Chiller_LS_A1.Qe = 0.5 * (hall_Q + platform_Q)
        Chiller_LS_A2.Qe = 0.5 * (hall_Q + platform_Q)
        col1, col2 = st.columns(2)
        with col1:
            st.markdown('### Chillers Settings')
            st.write('LS 1 evaporating water entry temperature (C)', Chiller_LS_A1.T_w_e_E )
            Chiller_LS_A1.Qe = st.number_input('LS 1 Qe (kW)', value = 0.5 * (hall_Q + platform_Q), min_value = float(0), max_value = float(hall_Q + platform_Q), step = float(10))

            st.write('LS 2 evaporating water entry temperature (C)', Chiller_LS_A2.T_w_e_E )
            st.number_input('LS 2 Qe (kW)', value = (hall_Q + platform_Q) - Chiller_LS_A1.Qe, min_value= float(0), max_value = float(hall_Q + platform_Q), step =float(10))
        with col2:
            st.markdown('### Towers Settings')
             #estimated Gw,c and T_tower_w_E
            T_tower_w_E_1 = 27
            T_tower_w_E_2 = 28
            T_tower_w_L_1 = 24
            T_tower_w_L_2 = 25
            st.write('Tower 1 entry water temperature (C)', T_tower_w_E_1)
            st.write('Tower 1 exit water temperature (C)', T_tower_w_L_1)
            st.write('Tower 2 entry water temperature (C)', T_tower_w_E_2)
            st.write('Tower 2 exit water temperature (C)', T_tower_w_L_2)

        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown('### Cooling Water Control')
            #estimeted最佳Gwe
            Cooling_Pump_LD_A1.flow_rate = st.slider('Cooling Pump LD 1 flow rate (t/h)', min_value = 150, max_value = 360, value = 289)#289
            Cooling_Pump_LD_A2.flow_rate = st.slider('Cooling Pump LD 2 flow rate (t/h)', min_value = 150, max_value = 360, value = 270)#270

        with col2:
            st.markdown('### Chiller Control')
        #假设冷冻水泵Gwe与制冷机和水塔的水速无损失相同/ 与Te，Ncomp息息相关 + 限制条件：最低水速or频率 + 热损失 + 性能曲线
            Chiller_LS_A1.G_w_e = Cooling_Pump_LD_A1.flow_rate 
            Chiller_LS_A2.G_w_e = Cooling_Pump_LD_A2.flow_rate

            Tower_LT_A1.G_w = Cooling_Pump_LD_A1.flow_rate
            Tower_LT_A2.G_w = Cooling_Pump_LD_A2.flow_rate

            # Te 与 r
            Te1 = st.slider('Evaporation Temperature LS 1 (C)', min_value= 25, max_value = 35, value=28)#28
            Te2 = st.slider('Evaporation Temperature LS 2 (C)', min_value = 25, max_value = 35, value = 26)#26
            r1 = Chiller_LS_A1.Qe / Chiller_LS_A1.Qe_max
            r2 = Chiller_LS_A2.Qe / Chiller_LS_A2.Qe_max
            st.write('Resulting LS 1 load ratio', r1)
            st.write('Resulting LS 2 load ratio', r2)

        with col3:
            st.markdown('### Chilled Water Control')

           

            G_w_c_1 = st.slider('Chilled Pump 1 flow rate (t/h)', min_value = 150, max_value = 360, value = 290)
            G_w_c_2 = st.slider('Chilled Pump 3 flow rate (t/h)', min_value = 150, max_value = 360, value = 300)

            Chiller_LS_A1.Tower = Tower_LT_A1
            Chiller_LS_A2.Tower = Tower_LT_A2

            Chilled_Pump_LQ_A1.flow_rate = G_w_c_1
            Chilled_Pump_LQ_A2.flow_rate = G_w_c_2
            Chiller_LS_A1.G_w_c = G_w_c_1
            Chiller_LS_A2.G_w_c = G_w_c_2
        st.markdown('## Power Consumptions')
        Cooling_Pump_LD_A1.run_pump(Cooling_Pump_LD_A1.flow_rate)
        Cooling_Pump_LD_A2.run_pump(Cooling_Pump_LD_A2.flow_rate)
        Chilled_Pump_LQ_A1.run_pump(Chilled_Pump_LQ_A1.flow_rate)
        Chilled_Pump_LQ_A2.run_pump(Chilled_Pump_LQ_A2.flow_rate)

        Chiller_LS_A1.simple_run(r1, Te1, T_tower_w_E_1, T_tower_w_L_1)
        Chiller_LS_A2.simple_run(r2, Te2, T_tower_w_E_2, T_tower_w_L_2)
        col1, col2 = st.columns(2)
        
        with col1:
            st.write('Cooling pump 1 power consumption (kW)', Cooling_Pump_LD_A1.Npump )
            st.write('Chiller 1 power consumption (kW)', Chiller_LS_A1.Ncom)
            st.write('Chilled pump 1 power consumption (kW)', Chilled_Pump_LQ_A1.Npump)   
        with col2:
            st.write('Cooling pump 2 power consumption (kW)', Cooling_Pump_LD_A2.Npump )
            st.write('Chiller 2 power consumption (kW)', Chiller_LS_A2.Ncom)
            st.write('Chilled pump 2 power consumption (kW)', Chilled_Pump_LQ_A2.Npump)   

        One =  Cooling_Pump_LD_A1.Npump + Chiller_LS_A1.Ncom + Chilled_Pump_LQ_A1.Npump
        Two = Cooling_Pump_LD_A2.Npump + Chiller_LS_A2.Ncom + Chilled_Pump_LQ_A2.Npump
        st.write('Total power consumption (kW)', One + Two)    



   
    # 控制变量
    ## 冷冻，冷却，水塔水泵频率
    ## 回排，新风风机频率
    ## 负载分配
    ## 蒸发温度

    # 被动变量
    ## 水塔进水温度
    ## 蒸发器进水温度 / ahu回水温度
    ## 冷凝器进出水温度
    ## 冷凝器整体水温


    # 结果
    ## 水塔排放热量 ～ 冷凝排放热量
    ## 冷水机组耗能
    ## 水泵耗能
    ## 风机耗能
    ## 环境效应

    st.markdown('## Digital Twin Graph')

    #画图

    icons = {
        "chiller": "icons/zhilengshebei.png",
        "pump": "icons/shuibeng.png",
        "fan": "icons/fengji.png",
        "tower": "icons/shuita.png",
        "air": "icons/wenshiduchuanganqi.png",
        "room": "icons/wodefangjian.png",
        "ahu": "icons/quanrejiaohuan-.png",
        "outside": "icons/tianqikongqizhishu.png",
        "guide": "icons/yk_yuanquan_fill.png"
    }

    import PIL
    import matplotlib.pyplot as plt

    images = {k: PIL.Image.open(fname) for k, fname in icons.items()}


    import networkx as nx

    #ahus = {'ahu 1': AHU_1, 'ahu 2': AHU_2, 'ahu 3': AHU_3}
    #chilled_pumps = {'chilled_pump 1': Chilled_Pump_1, 'chilled_pump 2': Chilled_Pump_2, 'chilled_pump 3': Chilled_Pump_3}
    #chillers = {'Chiller 1': Chiller_1, 'Chiller 2': Chiller_2}
    #towers = {'tower 1': Tower_1, 'tower 2': Tower_2, 'tower 3': Tower_3}
    #cooling_pumps = {'cooling pump 1': Cooling_Pump_1, 'cooling pump 2': Cooling_Pump_2, 'cooling pump 3': Cooling_Pump_3}

    G = nx.MultiDiGraph()

    G.add_node('Tower_LT_A1', pos = (0, 10), type = 'Tower', image = images['tower'], object = Tower_LT_A1)
    G.add_node('Tower_LT_A2', pos = (0, 9), type = 'Tower', image = images['tower'], object = Tower_LT_A2)
    G.add_node('Chilled_Pump_LQ_A1', pos = (1, 10), type = 'Pump', image = images['pump'], object = Chilled_Pump_LQ_A1)
    G.add_node('Chilled_Pump_LQ_A2', pos = (1, 9), type = 'Pump', image = images['pump'], object = Chilled_Pump_LQ_A2)

    G.add_node('Chiller_LS_A1', pos = (2,10), type = 'Chiller', image = images['chiller'], object = Chiller_LS_A1)
    G.add_node('Chiller_LS_A2', pos = (2,9), type = 'Chiller', image = images['chiller'], object = Chiller_LS_A2)


    G.add_node('Chilling_Water', pos = (0.5, 9.5), type = "Guide", image = images['guide'], object = Chilling_Water)

    G.add_node('Supply_Water', pos = (2.5, 9.5), type = "Guide", image = images['guide'], object = Supply_Water)

    G.add_node('Cooling_Pump_LD_A1', pos = (3, 10), type = "Pump", image = images['pump'], object = Cooling_Pump_LD_A1)
    G.add_node('Cooling_Pump_LD_A2', pos = (3, 10), type = "Pump", image = images['pump'], object = Cooling_Pump_LD_A2)

    G.add_node('Return_Water', pos = (4, 9.5), type = 'Guide', image = images['guide'], object = images['guide'])

    G.add_node('Water_Assembling', pos = (4, 9), type = 'Guide', image = images['guide'], object = Water_Assembling)

    G.add_node('Water_Distributor', pos = (3, 9), type = 'Guide', image = images['guide'], object = Water_Distributor)

    G.add_node('AHU_KT_A1', pos = (3, 8), type = 'AHU', image = images['ahu'], object = AHU_KT_A1)
    G.add_node('AHU_KT_A2', pos = (4, 8), type = 'AHU', image = images['ahu'], object = AHU_KT_A2)

    G.add_edges_from([('Tower_LT_A1', 'Chilled_Pump_LQ_A1'),('Chilled_Pump_LQ_A1', 'Chiller_LS_A1'), ('Chiller_LS_A1', 'Supply_Water'),
    ('Tower_LT_A2', 'Chilled_Pump_LQ_A2'),('Chilled_Pump_LQ_A2', 'Chiller_LS_A2'), ('Chiller_LS_A2', 'Supply_Water'), 
    ('Chiller_LS_A1', 'Chilling_Water'), ('Chilling_Water', 'Tower_LT_A1'),
    ('Chiller_LS_A2', 'Chilling_Water'), ('Chilling_Water', 'Tower_LT_A2'),
    ('Supply_Water', 'Water_Distributor'),
    ('AHU_KT_A1', 'Water_Assembling'), ('Water_Distributor', 'AHU_KT_A1'),
    ('AHU_KT_A2', 'Water_Assembling'), ("Water_Distributor", "AHU_KT_A2"),
    ('Water_Assembling', 'Return_Water'), ('Return_Water', 'Cooling_Pump_LD_A1'), ('Return_Water', 'Cooling_Pump_LD_A2'),
    ('Cooling_Pump_LD_A1', 'Chiller_LS_A1'), ('Cooling_Pump_LD_A2', 'Chiller_LS_A2'),
    ('Outdoor_Tower', 'Tower_LT_A1'), ('Outdoor_Tower', 'Tower_LT_A2') 
    ])



    G.add_node('Mix_Air_1', pos = (3.5, 7), type = 'Guide', image = images['guide'], object = Mix_Air_1)
    G.add_node('Mix_Air_2', pos = (4.5, 7), type = 'Guide', image = images['guide'], object = Mix_Air_2)

    G.add_node('Recirculating_Air_A', pos = (3, 6.5), type = 'Guide', image = images['guide'], object = Recirculating_Air_A)
    G.add_node('Recirculating_Air_B', pos = (4, 6.5), type = 'Guide', image = images['guide'], object = Recirculating_Air_B)

    G.add_node('Air_Distributor_1', pos = (1, 7), type = 'Guide', image = images['guide'], object = Air_Distributor_1)
    G.add_node('Air_Distributor_2', pos = (2, 7), type = 'Guide', image = images['guide'], object = Air_Distributor_2)

    G.add_node('Fan_HPF_A1', pos = (3, 6), type = 'Fan', image = images['fan'], object = Fan_HPF_A1)
    G.add_node('Fan_HPF_B1', pos = (4, 6), type = 'Fan', image = images['fan'], object = Fan_HPF_B1)

    G.add_node('Return_Air_A', pos = (2.7, 5.5), type = 'Guide', image = images['guide'], object = Return_Air_A)
    G.add_node('Return_Air_B', pos = (3.7, 5.5), type = 'Guide', image = images['guide'], object = Return_Air_B)

    G.add_node('Exhaust_Air', pos = (4.5, 4), type = 'Guide', image = images['guide'], object = Exhaust_Air)

    #车厅 hall
    #车台 platform
    G.add_node('Hall', pos = (1.5, 4.5), type = 'Environment', image = images['room'], object = Hall)
    G.add_node('Platform', pos = (2.5, 4.5), type = 'Environment', image = images['room'], object = Platform)

    G.add_node('Fan_KXF_A1', pos = (6, 6), type = 'Fan', image = images['fan'], object = Fan_KXF_A1)
    G.add_node('Fan_KXF_B1', pos = (5, 6), type = 'Fan', image = images['fan'], object = Fan_KXF_B1)

    G.add_node('Supply_Air', pos = (5.5, 4), type = 'Guide', image = images['guide'], object = Supply_Air)

    G.add_node('Outdoor_TK', pos = (5, 3), type = 'Environment', image = images['outside'], object = Outdoor_TK)

    G.add_node('Outdoor_Tower', pos = (-1, 9.5), type = 'Environment', image = images['outside'], object = Outdoor_Tower)

    G.add_node('Fan_PY_A1', pos = (2.3, 3.5), type = 'Fan', image = images['fan'], object = Fan_PY_A1)

    G.add_edges_from([ ('Mix_Air_1', 'AHU_KT_A1'), ('Mix_Air_2', 'AHU_KT_A2'),
    ('AHU_KT_A1', 'Air_Distributor_1'), ('AHU_KT_A2', 'Air_Distributor_2'),
    ('Air_Distributor_1', 'Hall'), ('Air_Distributor_2', 'Hall'),
    ('Air_Distributor_1', 'Platform'), ('Air_Distributor_2', 'Platform'),
    ('Hall', 'Fan_PY_A1'), ('Fan_PY_A1', 'Exhaust_Air'), 
    ('Fan_HPF_A1', 'Exhaust_Air'), ('Fan_HPF_B1', 'Exhaust_Air'),
    ('Exhaust_Air', 'Outdoor_TK'),
    ('Platform', 'Return_Air_A'), ('Platform', 'Return_Air_B'),
    ('Return_Air_A', 'Fan_HPF_A1'), ('Return_Air_B', 'Fan_HPF_B1'),
    ('Fan_HPF_A1', 'Recirculating_Air_A'), ('Fan_HPF_B1', 'Recirculating_Air_B'),
    ('Recirculating_Air_A', 'Mix_Air_1'), ('Recirculating_Air_B','Mix_Air_2'),
    ('Outdoor_TK', 'Supply_Air'), ('Supply_Air', 'Fan_KXF_A1'), ('Supply_Air', 'Fan_KXF_B1'),
    ('Fan_KXF_A1', 'Mix_Air_1'), ('Fan_KXF_B1', 'Mix_Air_2'),



    ])

    pos = G.nodes('pos')

    #三类连接线

# 待冷却
# 已冷却
# 处理空气中

#也可以后期运行的时候分成，有运行和没运行的差别
    #air_treatment = [(u,v) for (u, v) in graph.edges() if v in ['return air', 
    #'recirculating air', 'fresh air', 'exhaust air', 'exhaust fan', 'fresh air', 'mix air', 'room_to_ahu'] 
    #or (u, v) in [('room_to_ahu', 'ahu 1'), ('room_to_ahu', 'ahu 2'), ('room_to_ahu', 'ahu 3')]]

    #cooling_flow = [(u, v) for (u, v) in graph.edges() if v in ['ahu_to_chiller_evaporator', "chiller_to_cooling_pump", "cooling_pump 1",
    #"cooling_pump 2", "cooling_pump 3", "cooling_pump_to_tower", "tower_to_chiller"] or 
    #(u, v) in [('ahu_to_chiller_evaporator', 'Chiller 1'), ('ahu_to_chiller_evaporator', 'Chiller 2'), ('cooling_pump_to_tower', 'tower 1'),
    #('cooling_pump_to_tower', 'tower 2'), ('cooling_pump_to_tower', 'tower 3'), ("tower_to_chiller", "Chiller 1"),
    #("tower_to_chiller", "Chiller 2")]]

    #chilled_flow = [(u, v) for (u, v) in graph.edges() if v in [ "chiller_evaporator_to_chilled_pump", "chilled_pump 1",
    #"chilled_pump 2", "chilled_pump 3", "chilled_pump_to_ahu", "ahu_to_room", "supply air", "Room"] or (u, v) in [ ("chilled_pump_to_ahu", "ahu 1"), ("chilled_pump_to_ahu", "ahu 2"), ("chilled_pump_to_ahu", "ahu 3")]]

    #pos = graph.nodes('pos')


    #render the networkx graph to a plotly format

    #spring_3D = nx.spring_layout(G, dim = 3)
    #st.write(spring_3D)
    edge_x = []
    edge_y = []
    edge_z = []
    nodeSize = 2
    for edge in G.edges():
        start= G.nodes[edge[0]]['pos']
        end = G.nodes[edge[1]]['pos']
        #start = spring_3D[edge[0]]
        #end = spring_3D[edge[1]]
        #edge_x, edge_y, edge_z = addEdge_3D(start, end, edge_x, edge_y, edge_z, .8, 'end', .04, 30, nodeSize)
        edge_x, edge_y = addEdge(start, end, edge_x, edge_y, .8, 'end', .04, 30, nodeSize)
   
        #edge_x.append(x0)
        #edge_x.append(x1)
        #edge_x.append(None)
        #edge_y.append(y0)
        #edge_y.append(y1)
        #edge_y.append(None)

    lineWidth = 2
    lineColor = '#000000'

    #不同的edge trace

    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=lineWidth, color='#000000'),
        hoverinfo='none',
        mode='lines+markers')

    #edge_trace = go.Scatter3d(x = edge_x, 
    #    y = edge_y, z = edge_z,
    #    mode = 'lines', line = dict(color = lineColor, width = lineWidth),
    #    hoverinfo = 'none')

    node_x = []
    node_y = []
    node_z = []
    for node in G.nodes():
        x, y = G.nodes[node]['pos']
        node_x.append(x)
        node_y.append(y)

    #node_x = [spring_3D[i][0] for i in G.nodes]
    #node_y = [spring_3D[i][1] for i in G.nodes]
    #node_z = [spring_3D[i][2] for i in G.nodes]
    
    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers',
        hoverinfo='text',
        marker=dict(
            showscale=True,
            # colorscale options
            #'Greys' | 'YlGnBu' | 'Greens' | 'YlOrRd' | 'Bluered' | 'RdBu' |
            #'Reds' | 'Blues' | 'Picnic' | 'Rainbow' | 'Portland' | 'Jet' |
            #'Hot' | 'Blackbody' | 'Earth' | 'Electric' | 'Viridis' |
            colorscale='YlGnBu',
            reversescale=True,
            color=[],
            size=10,
            colorbar=dict(
                thickness=15,
                title='Node Connections',
                xanchor='left',
                titleside='right'
            ),
            line_width=2))
    
    '''
    node_trace = go.Scatter3d(x = node_x,
            y = node_y, z = node_z, mode = 'markers', marker=dict(
            showscale=True,
            # colorscale options
            #'Greys' | 'YlGnBu' | 'Greens' | 'YlOrRd' | 'Bluered' | 'RdBu' |
            #'Reds' | 'Blues' | 'Picnic' | 'Rainbow' | 'Portland' | 'Jet' |
            #'Hot' | 'Blackbody' | 'Earth' | 'Electric' | 'Viridis' |
            colorscale='YlGnBu',
            reversescale=True,
            color=[],
            size=10,
            colorbar=dict(
                thickness=15,
                title='Node Connections',
                xanchor='left',
                titleside='right'
            ),
            line_width=2)
            )
    '''
    
        #coloring node points
    node_adjacencies = []
    node_text = []
    for node, adjacencies in enumerate(G.adjacency()):
        node_adjacencies.append(len(adjacencies[1]))
        #node_text.append('# of connections: '+str(len(adjacencies[1])))
    for n in G.nodes:
        node_text.append(n)

    node_trace.marker.color = node_adjacencies
    node_trace.text = node_text

    # create network graph
    fig = go.Figure(data=[edge_trace, node_trace],
             layout=go.Layout(
                title='<br>Network graph made with Python',
                titlefont_size=16,
                showlegend=False,
                hovermode='closest',
                margin=dict(b=20,l=5,r=5,t=40),
                annotations=[ dict(
                    text="Python code: <a href='https://plotly.com/ipython-notebooks/network-graphs/'> https://plotly.com/ipython-notebooks/network-graphs/</a>",
                    showarrow=False,
                    xref="paper", yref="paper",
                    x=0.005, y=-0.002 ) ],
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                )
    #make the arrow symmetrical
    fig.update_layout(yaxis = dict(scaleanchor = "x", scaleratio = 1), plot_bgcolor='rgb(255,255,255)')



    st.plotly_chart(fig)


        
    