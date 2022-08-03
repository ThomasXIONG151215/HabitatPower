import streamlit as st 

from models.heat_transfer_models import air_rho_cp, source_coordinates, structure, heat_transfer

from models.gas_jet import Gas_Jet

import plotly.express as px

def app():
    st.markdown('# Environment heat transfer simulation')

    # 出风口参数
    d0 = 1 #直径 #m

    T0 = st.slider('Outlet air temperature',min_value=20, max_value=28, step = 1, value = 20) #ahu出来的风温度 #K

    Te = st.slider('Environment Temperature', min_value=24, max_value=35, step= 1, value = 28) #地铁内当前所有点温度

    v0 = st.number_input('A-C air velocity', value = 2.3)#m/s

    a = 0.12 #紊流系数，带有导板的直流式风机
    st.write('coefficient of turbulence', a)
    alpha = st.number_input('outlet angle', step = 5, value = 45) #导板角度，假设向上向下45度

    air = Gas_Jet()

    lamb = 0.03 #假设的空气热导率
    st.write('coefficient of heat conduction', lamb)

    col1, col2, col3 = st.columns(3)

    with col1:
        xs = st.number_input('x length', step = 1, value = 72)
        ax = st.slider('x meshes', step = 1, value = 72)
    with col2:
        ys = st.number_input('y length', step= 1, value = 8)
        bx = st.slider('y meshes', step = 1, value = 8)
    with col3:
        zs = st.number_input('z length', step = 1, value = 5)
        cx = st.slider('z meshes', step = 1, value = 10)

    C = 0.1 # Courant Number

    dx = xs/(ax+0.01) #总长度 / 节点处亩
    dt = C * dx / v0 #
    st.write('dx:', dx)
    st.write('dt:', dt)

    passengers = [(1 * ax/xs ,2 * bx/ys), (4 * ax/xs, 3 * bx/ys), (8 * ax/xs, 2 * bx/ys ), (9 * ax/xs, 12 * bx/ys), (5 * ax/xs, 0 * bx/ys), (2 * ax/xs, 4 * bx/ys)]

    st.write('passgengers coordinates', passengers)

    
    #xs, ys, zs = 36*2, 15*2, 5*2 #xs*2 = x轴长度(米）

    #ax, bx, cx = 36, 15, 5 #ax = 网格数目
    air_outlets = []
    #z固定4.4，y固定1.3, x 36米内每4.6米有一个
    #每0.5米一个网格点情况下，误差会较小
    B = st.number_input('meters on x per air outlet', step = 0.1, value = 4.5, max_value=float(xs)) #每隔多少米有一个出风口
    C =  st.number_input('position of air outlet on y', step = 0.1, value = 1.5, max_value=float(ys))
    D =  st.number_input('position of air outlet on z', step = 0.1, value = 4.5, max_value=float(zs))
    air_outlets.append((0, bx * C / ys, cx * D / zs))
    co = 1
    while air_outlets[-1][0] <= ax: #x轴上每个出风口位置不同，y和z轴上则都是固定的
        air_outlets.append((co * B * ax / xs, bx * C / ys, cx * D / zs))
        co += 1
        

#    for x in range(int(xs/ (xs/ax) /(B))):
 #       air_outlets.append((x*(B)*(xs/ax), C*(ys/bx), D*(zs/cx)))

    st.write('outlet_real_locations', air_outlets)
    coors, outlet_projections = source_coordinates(xs, ys, zs, ax, bx, cx, air_outlets)

    st.write('outlet_projections on meshes', outlet_projections)
    structure_state = 0
    
    df, Temperatures, cooling_umbrella, Receive_or_not = structure(coors, outlet_projections, d0, a, Te, T0, v0, cx, zs, alpha)
    structure_state += 1
        
    #except:
     #   st.write('Error: the outlet projection does not fit the environment grid mesh')

    st.markdown('## Heat Transfer Simulation')
    #st.write(structure_state)
    #try:
    total_time_of_simulation = st.number_input('Input total seconds of simulations', step = 1, value = 60)

    df2 = heat_transfer(df, ax, bx, cx, zs, dt, dx, lamb, d0, T0, passengers, v0, total_time_of_simulation, Temperatures, cooling_umbrella, Receive_or_not)

    n = 0
    A = n * len(coors[0]) * len(coors[0][0]) #5 * 8 = len(z) * len(y) 

    moment = st.number_input('Choose the moment of visualisation', max_value= int(total_time_of_simulation), step = 1)

    fig = px.scatter_3d(data_frame=df2[A:], x = df2['x'][A:], y = df2['y'][A:], z = df2['z'][A:],
    color = 'moment ' + str(int(moment))+ ' T', opacity=0.5)
    st.plotly_chart(fig)
    #except:
     ##   st.markdown('*Please solve the air outlet projected to the mesh grid problem first*')