import numpy as np 
import plotly.figure_factory as ff
import plotly.graph_objects as go
import pandas as pd
import streamlit as st 

def field(strength, X, Y, x, y):
    strength = strength                  # strength of the sink

    # compute the velocity on the mesh grid
    u = (strength / (2 * np.pi) *
            (X - x) / ((X - x)**2 + (Y - y)**2 + 0.01))
    v = (strength / (2 * np.pi) *
            (Y - y) / ((X - x)**2 + (Y - y)**2 + 0.01))
    
    return u,v
'''bundle = {}
    for i in range(len(u)):
        bundle['u' + str(i)] = u[i]
    for i in range(len(v)):
        bundle['v' + str(i)] = v[i]

    df = pd.DataFrame(bundle, index=list(range(len(bundle['u1']))))

    for col in df.columns:
        df[col] = df[col].fillna(0, inplace=True)
    
    new_u = [ df['u' + str(i)] for i in range(len(u)) ]
    new_v = [ df['v' + str(i)] for i in range(len(v))]

    return new_u, new_v'''
    

def get_velocity_doublet(strength, xd, yd, X, Y):
    
    u = (- strength / (2 * np.pi) *
         ((X - xd)**2 - (Y - yd)**2) /
         ((X - xd)**2 + (Y - yd)**2 + 0.001)**2)
    v = (- strength / (2 * np.pi) *
         2 * (X - xd) * (Y - yd) /
         ((X - xd)**2 + (Y - yd)**2 + 0.001)**2)
    
    return u, v

def get_stream_function_doublet(strength, xd, yd, X, Y):

    psi = - strength / (2 * np.pi) * (Y - yd) / ((X - xd)**2 + (Y - yd)**2 + 0.01)
    
    return psi

def app():
    st.markdown('# Wind Field Simulation')
    st.markdown('Have a look on the influence of passengers position to the two-dimensional wind field')


    st.markdown('## Environment Settings')
    N = 50
    st.write('Number of points in each direction', N)        
                            # number of points in each direction
    col1, col2 = st.columns(2)

    with col1:
        x_start = -2
        st.write('x-start: ', x_start)    
        x_end = 2
        st.write('x-end: ',x_end)             # boundaries in the x-direction
    with col2:
        y_start = -1 
        st.write('y-start: ', y_start)  
        y_end = 1
        st.write('y-end:', y_end)   
               # boundaries in the y-direction
    x = np.linspace(int(x_start), int(x_end), int(N))    # creates a 1D-array with the x-coordinates
    y = np.linspace(y_start, y_end, int(N))    # creates a 1D-array with the y-coordinates

    X, Y = np.meshgrid(x, y)  

    strength_source = st.number_input('Air outlet source strength', value = 5)                      # source strength
    x_source, y_source = -2.0, 0.0             # location of the source
    st.write('source coordinates', (x_source, y_source))

    u_source1, v_source1 = field(strength_source, X, Y, -2, 0)
    u_source2, v_source2 = field(strength_source, X, Y, 2, 0)

    strength_sink = st.number_input('Small sink strength', value = -3) 

    u_sink1, v_sink1 = field(strength_sink, X, Y,2, 1)
    u_sink2, v_sink2 = field(strength_sink, X, Y,2, -1)
    u_sink3, v_sink3 = field(strength_sink, X, Y,-2, -1)
    u_sink4, v_sink4 = field(strength_sink, X, Y,-2, 1)

    strenght_sink_2 = st.number_input('Major sink strength', value = -5) 

    u_sink5, v_sink5 = field(strenght_sink_2 , X, Y,0.5, 0)
    u_sink6, v_sink6 = field(strenght_sink_2 , X, Y,-0.5, 0)


    #仿doublet障碍物
    st.markdown('## Passengers position settings')
    st.markdown('*assuming we have 6 passengers*')
    kappa = 0.2 #strength of the doublet
    col1, col2, col3 = st.columns(3)
    with col1:
        x_doublet = st.number_input('passenger 1 x', value = float(-1), min_value=float(x_start), max_value=float(x_end))
        y_doublet = st.number_input('passenger 1 y', value = -0.5, min_value=float(y_start), max_value=float(y_end))
    with col2:
        xpass_1 = st.number_input('passenger 2 x', value = 0.7, min_value=float(x_start), max_value=float(x_end))
        ypass_1 = st.number_input('passenger 2 y', value = 0.8, min_value=float(y_start), max_value=float(y_end))
    with col3:
        xpass_2 = st.number_input('passenger 3 x', value = float(-0.7), min_value=float(x_start), max_value=float(x_end))
        ypass_2 = st.number_input('passenger 3 y', value = -0.9, min_value=float(y_start), max_value=float(y_end))
    col4, col5, col6 = st.columns(3)
    with col4:
        xpass_3 = st.number_input('passenger 4 x', value = -0.4, min_value=float(x_start), max_value=float(x_end))
        ypass_3 = st.number_input('passenger 4 y', value = 0.2, min_value=float(y_start), max_value=float(y_end))
    with col5:
        xpass_4 = st.number_input('passenger 5 x', value = float(-1), min_value=float(x_start), max_value=float(x_end))
        ypass_4 = st.number_input('passenger 5 y', value = -0.2, min_value=float(y_start), max_value=float(y_end))
    with col6:
        xpass_5 = st.number_input('passenger 6 x', value = float(-1.2), min_value=float(x_start), max_value=float(x_end))
        ypass_5 = st.number_input('passenger 6 y', value = -0.6, min_value=float(y_start), max_value=float(y_end))
    # compute the velocity field on the mesh grid
    u_doublet, v_doublet = get_velocity_doublet(kappa, x_doublet, y_doublet, X, Y)
    u_doublet1, v_doublet1 = get_velocity_doublet(kappa, xpass_1, ypass_1, X, Y)
    u_doublet2, v_doublet2 = get_velocity_doublet(kappa, xpass_2, ypass_2, X, Y)
    u_doublet3, v_doublet3 = get_velocity_doublet(kappa, xpass_3, ypass_3, X, Y)
    u_doublet4, v_doublet4 = get_velocity_doublet(kappa, xpass_4, ypass_4, X, Y)
    u_doublet5, v_doublet5 = get_velocity_doublet(kappa, xpass_5, ypass_5, X, Y)

    #freestream speed
    u_inf = 1.0

    R = np.sqrt(kappa / (2 * np.pi * u_inf))

    x_tests = np.linspace(-2, 2, 200)
    wall_field = []
    for i in x_tests:
        wall_field.append(get_velocity_doublet(kappa, i, 1, X, Y))


    # compute the velocity of the pair source/sink by superposition
    u = u_source1 + u_source2 + u_sink1 + u_sink2 + u_sink3 + u_sink4 + u_doublet
    v = v_source1 + v_source2 + v_sink1 + v_sink2 + v_sink3 + v_sink4 + v_doublet

    for stuff in wall_field:
        u += stuff[0]
        v += stuff[1]

    for (up, vp) in [(u_doublet1, v_doublet1),(u_doublet2, v_doublet2),(u_doublet3, v_doublet3),(u_doublet4, v_doublet4), (u_doublet5, v_doublet5)]:
        u += up
        v += vp


    # plot the streamlines of the pair source/sink
    width = 10.0
    height = (y_end - y_start) / (x_end - x_start) * width

    # Create streamline figure
    fig = ff.create_streamline(x, y, u, v,
                            name='streamline',density = 2)

    fig.add_trace(go.Scatter(
        x = [xpass_1, xpass_2, xpass_3, xpass_4],
        y = [ypass_1, ypass_2, ypass_3, ypass_4],
        mode = "text",
        )
        )

    for (x,y) in [(x_doublet, y_doublet),(xpass_1, ypass_1), (xpass_2, ypass_2), (xpass_3, ypass_3), (xpass_4, ypass_4), (xpass_5, ypass_5)]:
        fig.add_shape(type = "circle",
            xref = "x", yref = "y",
            line_color = "LightSeaGreen",
            fillcolor="PaleTurquoise",
            x0 = x - 0.11, y0 = y - 0.11, x1 = x+ 0.11, y1 = y + 0.11
        )
    
    st.plotly_chart(fig)
