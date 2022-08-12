import streamlit as st 

import sys
sys.path.append('/Users/wuzhenxiong/主营科研/红宝石项目/plotly_dirgraph_master')
from addEdge import addEdge, addEdge_3D
import plotly.graph_objects as go

def main():
    st.header('Scene Creation')
    col1, col2 = st.columns((1,2))
    import networkx as nx 
    G = nx.MultiDiGraph() # System Graph
    with col1:
        tab1,tab2 = st.tabs(["System nodes", "System edges"])
        chillers = {}
        cooling_pumps = {}
        exchangers = {}
        chilled_pumps = {}
        with tab1:
            with st.expander("Chillers settings"):
                number_of_chillers = st.number_input('number of chillers', step = 1, min_value=0, value=1)
                #chillers = {}

                for i in range(1, int(number_of_chillers) + 1):
                    value = st.number_input('Chiller ' + str(i) + ' capacity (kW)', value = 200, min_value=100, max_value=800, step = 20)

                    chillers['Chiller ' + str(i) + ' capacity'] = value
            

            with st.expander("Cooling Pumps settings"):
                number_of_pumps = st.number_input('number of cooling pumps', step = 1, min_value=0, value=1)
                #pumps = {}

                for i in range(1, int(number_of_pumps) + 1):
                    value = st.number_input('Cooling Pump ' + str(i) + ' head size (m)', value = 2, min_value=1, max_value=8, step = 1)

                    cooling_pumps['Cooling Pump ' + str(i) + ' head size (m)'] = value
            


            with st.expander("Chilled Pumps settings"):
                number_of_pumps = st.number_input('number of chilled pumps', step = 1,min_value=0, value=1)
                #pumps = {}

                for i in range(1, int(number_of_pumps) + 1):
                    value = st.number_input('Chilled Pump ' + str(i) + ' head size (m)', value = 2, min_value=1, max_value=8, step = 1)

                    chilled_pumps['Chilled Pump ' + str(i) + ' head size (m)'] = value
            

            with st.expander("Exchanger settings"):
                number_of_exchangers = st.number_input('number of exchangers', step = 1,min_value=0, value=1)
                #exchangers = {}

                for i in range(1, int(number_of_exchangers) + 1):
                    value = st.number_input('Exchanger ' + str(i) + ' efficieny', value = 1.0, min_value=0.0, max_value=3.0, step = 0.2)

                    exchangers['Exchanger ' + str(i) + ' capacity'] = value
            


            #绘图
            

            for key in chillers:
                G.add_node(key[:9], capacity = chillers[key])
            for key in exchangers:
                G.add_node(key[:11], efficiency = exchangers[key])
            for key in cooling_pumps:
                G.add_node(key[:12], head_size = cooling_pumps[key])
            for key in chilled_pumps:
                G.add_node(key[:12], head_size = chilled_pumps[key])


        
        with tab2:
            starts = []
            start_choices = list(G.nodes())
            ends = []
            import random
            number_of_edges = st.number_input('number of edges', step = 1)
            with st.expander('Edges Connecting'):
                for i in range(int(number_of_edges)):                
                    if i >= len(start_choices):
                        temporal_start_choices = [c for c in start_choices if c!=start_choices[i - len(start_choices)]]
                        temporal_start_choices.append(start_choices[i - len(start_choices)])

                        temporal_start_choices.remove(start_choices[i-int(len(start_choices)/2)-1])
                        temporal_start_choices.append(start_choices[i-int(len(start_choices)/2)-1])

                    else:
                        temporal_start_choices = [c for c in start_choices if c!=start_choices[i]]
                        temporal_start_choices.append(start_choices[i])
                
                    a = temporal_start_choices[0]
                    b = temporal_start_choices[2]

                    start, end = st.select_slider('Edge ' + str(i),  options = temporal_start_choices, value = (a,b))
                    G.add_edge(start, end)
                    #st.write((start,end))

    
                
    with col2: #draw graph
       # st.header("Graph Drawing")
        pos = nx.spring_layout(G)
        node_x = []
        node_y = []
        for node in G.nodes:
            x, y = pos[node]
            node_x.append(x)
            node_y.append(y)

        edge_x = []
        edge_y = []

        for edge in G.edges():
            start = pos[edge[0]]
            end = pos[edge[1]]
            edge_x, edge_y = addEdge(start, end, edge_x, edge_y, .8, 'end', .04, 30, 2)
        lineWidth = 2

        edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=lineWidth, color='#000000'),
        hoverinfo='none',
        mode='lines+markers')

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
                    title='The network graph of your system',
                    titlefont_size=16,
                    showlegend=False,
                    hovermode='closest',
                    margin=dict(b=20,l=5,r=5,t=40),
                    annotations=[ dict(
                        text="Reference <a href='https://plotly.com/ipython-notebooks/network-graphs/'> https://plotly.com/ipython-notebooks/network-graphs/</a>",
                        showarrow=False,
                        xref="paper", yref="paper",
                        x=0.005, y=-0.002 ) ],
                    xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))

                    )
        #make the arrow symmetrical
        fig.update_layout(autosize = False, height = 800, width = 600,yaxis = dict(scaleanchor = "x", scaleratio = 1), plot_bgcolor='rgb(255,255,255)')

        
        

        st.plotly_chart(fig, use_container_width=True)
        
    updateg = st.button('Update your graph')
    if updateg:
        import json 
        from networkx.readwrite import json_graph
        graph_data = json_graph.node_link_data(G)
        json_object = json.dumps(graph_data, indent = 5)
        #/Users/wuzhenxiong/业余初创项目/研屋调源/streamlit_app_1.2/streamlit_gallery/data
        #with open("../../../data/created_scene.json","w") as outfile:
        with open("/Users/wuzhenxiong/业余初创项目/研屋调源/streamlit_app_1.2/streamlit_gallery/data/created_scene.json","w") as outfile:
            outfile.write(json_object)
if __name__ == "__main__":
    #st.set_page_config(layout="wide")
    main()
