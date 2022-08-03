from turtle import bgcolor
import streamlit as st
import cv2
import networkx as nx
from PIL import Image
from streamlit_drawable_canvas import st_canvas
import pandas as pd
import streamlit.components.v1 as components
import matplotlib.pyplot as plt
from pyvis import network as net
from IPython.core.display import display, HTML

st.markdown('# Physics Block Modeling DEMO')
st.markdown('## Localise blocks')
block_center_coor = []

drawing_mode = st.sidebar.selectbox("Drawing tool:", ("point", "rectangle"))
upload_image = st.sidebar.file_uploader("Design 2d:", type = ["jpeg", "png", "jpg"])

stroke_color = st.sidebar.color_picker("Stroke color hex: ")
bg_color = st.sidebar.color_picker("Background color hex: ", "#eee")

drawing_mode = st.sidebar.selectbox("Drawing tool:", ("point", "line", "rect", "circle", "transform"))

if drawing_mode == 'point':
    point_display_radius = st.sidebar.slider("Point display radius: ", 1, 10, 1)

st.write('use node to assign block centers, use line to connect nodes, use rectangle to assign surface horizon to block')
if upload_image is not None:
    canvas_result = st_canvas(
        fill_color = "rgba(255,120,3,2)",
        stroke_width = 5,
        stroke_color = stroke_color,
        background_color = bgcolor,
        background_image = Image.open(upload_image) if upload_image else None,
        update_streamlit = st.sidebar.checkbox("Update in realtime", True),
        height = 150,
        drawing_mode = drawing_mode,
        point_display_radius =  point_display_radius if drawing_mode == 'point' else 0,
        key = "canvas",
    )


    #if canvas_result.image_data is not None:
    #    st.image(canvas_result.image_data)

    if canvas_result.json_data is not None:
        objects = pd.json_normalize(canvas_result.json_data["objects"])
        for col in objects.select_dtypes(include = ['object']).columns:
            objects[col] = objects[col].astype("str")
        
        st.dataframe(objects)

    g = nx.Graph()

    for i in range(len(objects)):
        g.add_node(i, pos = (int(objects['left'][i]), int(-objects['top'][i])))
    

    fig, ax = plt.subplots()
    pos = g.nodes('pos')

    nx.draw(g, pos, with_labels = True)
    st.pyplot(fig)

    
    st.image(canvas_result.image_data)
    #html = open('ex.html','r',encoding = 'utf-8')
    #source = html.read()
    #components.html(source, scrolling = True)


    st.markdown('## Draw Edges')
    edges = []
    start = st.number_input('From ', step=1, max_value = len(g.nodes()))
    end = st.number_input('To ', step=1, max_value = len(g.nodes()))

    edges.append((start, end))

    #if st.button('Confirm'):
     #   edges.append((start, end))
        

    if st.button('Show'):
        st.write(edges)
    
    
    g.add_edges_from(edges)
    
    #g.add_edge(edges,v_of_edge=)
    st.write(g.edges)

    nx.draw(g, pos, with_labels = True)
    st.pyplot(fig)