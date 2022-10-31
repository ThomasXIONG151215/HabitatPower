import streamlit as st 

st.markdown("# 🖊 研究案例")
st.sidebar.markdown("# 🖊 Study Case")

col1, col2 = st.columns(2)

with col1:
          st.image("案例原图.png", use_column_width=True, caption="案例原图")
          st.image("案例简化图.png", use_column_width=True, caption="案例简化图")
          
with col2:
          st.markdown("本研究中我们参考了上海闸北某医院的护理单元的俯瞰图来设计案例")

          st.markdown("为了能够方便地进行演示，我们将案例简化成五个主要区域。分别有病房区I，病房区II，办公区，公共走廊和娱乐活动区。")

          st.markdown("病房区I和II各自包含三间二床房与两间三床房，办公区则包含一间医生办公室，护士办公室，值班室，治疗室和设备库房")

          st.markdown("每个空间类型的具体尺寸如下: 首先所有房间统一高度为3.5米")

          df = { '空间类型': ["二床房", "三床房","医生办公室", "护士办公室", "值班室", "治疗师", "设备库房", "走廊", "活动区"], 
          "面积": [70, 100, 80, 80, 40, 60, 80, 306, 120],
          "周长": [34, 40, 36, 36, 26, 32, 36, 108, 44]
          }
          st.table(df)

          st.markdown("案例的主要任务就是向各位展示研屋调源的用法!")
          
