
import streamlit as st
import pandas as pd
st.markdown("# 🌅 新能源发电装配模块")
st.sidebar.markdown("# 🌅 Power Generation Settings")
st.markdown("在这里设计屋顶光伏发电场的装配方案，衡量不同产品选项各自的长期效益")
#STC 1000 W/m2 电池温度25C，大气质量1.5
KNOWN_DEVICE = [
        { "品牌 产品型号": "阿特斯 CS7L-580MB-AG", "最大功率(W)": 580, "组件面积(m2)": 2.83,  "重量(kg)": 34.6, "组件效率(%)": 20.5},
        { "品牌 产品型号": "晶科 JKM355N-6TL3-B", "最大功率(W)": 355, "组件面积(m2)": 1.74,  "重量(kg)": 19.0, "组件效率(%)": 20.38},
        { "品牌 产品型号": "隆基 LR5-72HPH-540M", "最大功率(W)": 540, "组件面积(m2)": 2.58,  "重量(kg)": 27.5, "组件效率(%)": 20.9},
        { "品牌 产品型号": "天合 TSM-DE09", "最大功率(W)": 405, "组件面积(m2)": 1.92,  "重量(kg)": 21, "组件效率(%)": 21.1},
        { "品牌 产品型号": "晶澳 JAM60S10-350/MR", "最大功率(W)": 350, "组件面积(m2)": 1.68,  "重量(kg)": 18.7, "组件效率(%)": 20.8},
    ]

df_installation = pd.DataFrame(KNOWN_DEVICE)
#光伏组件容量目标
#医院楼顶空余面积
with st.expander("装配场景设定"):
    st.markdown('##### 装配目标与场景面积 ')
    objectif = st.number_input("容量目标(kW)", value=50, step=10)
    space_available = st.number_input("屋顶空余面积(m2)", value=400, step=50)
    st.markdown("##### 已知品牌产品")
    st.table(KNOWN_DEVICE)

with st.expander("装配选项产能对比"):
###组件数量
###选项占地面积
###选项理论最大功率
###总安装成本（8元/瓦)
###屋顶承重梁(tonnes)
    df_installation["产品系列代号"] = ["CS7L", "JKM355N", "LR5", "TSM", "JAM60S10"]
    df_installation['方案组件数量'] = objectif*1000 / df_installation["最大功率(W)"]+1
    df_installation['方案占地面积(m2)'] = df_installation["组件面积(m2)"] * df_installation["方案组件数量"]
    df_installation['方案理论装配容量(kW)'] = df_installation["方案组件数量"] * df_installation["最大功率(W)"]/1000
    df_installation['安装总成本(¥)'] = 8 * df_installation['方案理论装配容量(kW)'] * 1000
    df_installation['屋顶承重量(t)'] = df_installation['方案组件数量'] * df_installation['重量(kg)']/1000

    st.dataframe(df_installation[["产品系列代号","方案组件数量","方案占地面积(m2)","方案理论装配容量(kW)","安装总成本(¥)","屋顶承重量(t)"]], use_container_width=True)

with st.expander("工程经济性评估"):
    df_year = pd.DataFrame(dict(
                    Time = [i for i in range(1,25)],
                    ))
#### 预估每年性能衰减率
    year_radiation = st.slider("地区年日照数", value=1600, max_value=2000, min_value=0)
    year_attenuation = st.slider("性能衰减率(%)", value=0.55, max_value = 5.00, min_value = 0.00)
    CS7L = [ year_radiation * df_installation["方案理论装配容量(kW)"][0] ]
    JKM355N = [ year_radiation * df_installation["方案理论装配容量(kW)"][1] ]
    LR5 = [ year_radiation * df_installation["方案理论装配容量(kW)"][2] ]
    TSM = [ year_radiation * df_installation["方案理论装配容量(kW)"][3] ]
    JAM60S10 = [ year_radiation * df_installation["方案理论装配容量(kW)"][4] ]

    CS7L_profit = [  year_radiation * df_installation["方案理论装配容量(kW)"][0] * 0.617 ]
    JKM355N_profit = [  year_radiation * df_installation["方案理论装配容量(kW)"][1] * 0.617 ]
    LR5_profit = [  year_radiation * df_installation["方案理论装配容量(kW)"][2] * 0.617 ]
    TSM_profit = [  year_radiation * df_installation["方案理论装配容量(kW)"][3] * 0.617 ]
    JAM60S10_profit = [  year_radiation * df_installation["方案理论装配容量(kW)"][4] * 0.617 ]

    CS7L_cover_date = 0
    JKM355N_cover_date = 0
    LR5_cover_date = 0
    TSM_cover_date = 0
    JAM60S10_cover_date = 0

    for i in range(1, 24):
        CS7L.append( (1- year_attenuation/100) * CS7L[i-1] )
        CS7L_profit.append( (1- year_attenuation/100) * CS7L[i-1] * 0.617 + CS7L_profit[i-1] )

        if CS7L_profit[i] >= df_installation["安装总成本(¥)"][0] and CS7L_cover_date == 0:
                      CS7L_cover_date = i

        JKM355N.append( (1 - year_attenuation/100) * JKM355N[i-1] )
        JKM355N_profit.append(  (1 - year_attenuation/100) * JKM355N[i-1] * 0.617 + JKM355N_profit[i-1] )

        if JKM355N_profit[i] >= df_installation["安装总成本(¥)"][1] and JKM355N_cover_date == 0:
                      JKM355N_cover_date = i

        LR5.append( (1-year_attenuation/100) * LR5[i-1] )
        LR5_profit.append( (1-year_attenuation/100) * LR5[i-1] * 0.617 + LR5_profit[i-1] )

        if LR5_profit[i] >= df_installation["安装总成本(¥)"][2] and LR5_cover_date == 0:
                      LR5_cover_date = i

        TSM.append( (1-year_attenuation/100) * TSM[i-1])
        TSM_profit.append( (1-year_attenuation/100) * TSM[i-1] * 0.617 + TSM_profit[i-1])
        
        if TSM_profit[i] >= df_installation["安装总成本(¥)"][3] and TSM_cover_date == 0:
                      TSM_cover_date = i

        JAM60S10.append( (1-year_attenuation/100) * JAM60S10[i-1] )
        JAM60S10_profit.append( (1-year_attenuation/100) * JAM60S10[i-1] * 0.617 + JAM60S10_profit[i-1] )

        if JAM60S10_profit[i] >= df_installation["安装总成本(¥)"][4] and JAM60S10_cover_date == 0:
                      JAM60S10_cover_date = i

    df_year["CS7L产能(kW)"] = CS7L
    df_year["JKM355N产能(kW)"] = JKM355N
    df_year["LR5产能(kW)"] = LR5
    df_year["TSM产能(kW)"] = TSM
    df_year["JAM60S10产能(kW)"] = JAM60S10

    df_year["CS7L节能收益(¥)"] = CS7L_profit
    df_year["JKM355N节能收益(¥)"] = JKM355N_profit
    df_year["LR5节能收益(¥)"] = LR5_profit
    df_year["TSM节能收益(¥)"] = TSM_profit
    df_year["JAM60S10节能收益(¥)"] = JAM60S10_profit

    st.line_chart(df_year, x="Time", y = ["CS7L产能(kW)", "JKM355N产能(kW)", "LR5产能(kW)", "TSM产能(kW)", "JAM60S10产能(kW)"], use_container_width=True)

    st.bar_chart(df_year, x="Time", y=["CS7L节能收益(¥)", "JKM355N节能收益(¥)", "LR5节能收益(¥)", "TSM节能收益(¥)", "JAM60S10节能收益(¥)"])

    df_installation["成本回收期"] = [CS7L_cover_date, JKM355N_cover_date, LR5_cover_date, TSM_cover_date, JAM60S10_cover_date]

    st.table(df_installation[["产品系列代号", "成本回收期"]])

#### 地区年日照数设定

##### 每年发电量，节能收益(火电对比), 累计收益, 对比收益
#### 成本回收期

