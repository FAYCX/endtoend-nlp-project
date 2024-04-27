import streamlit as st
import pandas as pd
import networkx as nx
from pyvis.network import Network
import tempfile
from itertools import cycle
import base64

#generate your own page

html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title></title>
    <script src="https://unpkg.com/vis-network/standalone/umd/vis-network.min.js"></script>
    <style>
        body, html {{
            margin: 0;
            padding: 0;
            height: 100%;
            width: 100%;
            overflow: hidden;
        }}

        /* Custom CSS to override Streamlit defaults */
        .css-1v3fvcr, .css-18e3th9, .css-1d391kg {{
            padding: 0;
            margin: 0;
        }}

        p {{
        font-family: 'Helvetica Neue', Arial, sans-serif !important;
        color:#fff;
        #font-weight: bold;
        font-stretch: condensed;
        font-size:18px;
    }}

        button {{
        background-color: #4CAF50; /* Green background */
        color: white; /* White text */
        border: none; /* No border */
        padding: 10px 20px; /* Some padding */
        border-radius: 5px; /* Rounded corners */
    }}



        h1 {{
            position: absolute;
            font-weight: bold;
            text-align: center;
            letter-spacing: 1.5px;
            left: 50px;
            top: 0px;
            font-color: white;
            font-size: 30px;
            z-index:10;
            font-family: 'Helvetica Neue', sans-serif;
            font-weight: bold;
            font-stretch:condensed; 

        }}
    </style>
</head>
<body>
<h1 style="color: #fff;">&lt;Alice in Wonderland&gt; Network</h1>
<div id="mynetwork"></div>
<script>
  
</script>
</body>
</html>
"""


def main_pipe():



    # Check if interactions are in the session state and if they contain data
    if 'interactions' not in st.session_state or not st.session_state.interactions:
        st.error('Please add some interactions on the sidebar before creating the graph.')
        for _ in range(3):
            st.write("")

        st.title("Create Your Social Network Visualization! ")
        st.write("Discover the power of Graph Neural Network by adding at least 3 (the more the merry) interactions between characters. Simply enter the names and how often you interact with them in the sidebar, and watch as a dynamic graph of your social network comes to life! This visualization uses GNN to illustrate the strength and depth of relationships. It's a fantastic way to see a unique map of your very own social connections!")

        for _ in range(3):
            st.write("")


        st.write("`Important Notice`: Your data will be discarded immediately once you leave this page. To keep a copy of your graph, please make sure to download it once it's been generated.")


        return  # Exit the function if no interactions

    if st.button('Create Graph'):
        create_graph()  # Function that creates and displays the graph
        
def get_image_as_base64(filename):
    with open(filename, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()
    return encoded_string


def create_graph():
   

    st.markdown('<div style="height: 80px;"></div>', unsafe_allow_html=True)
    

    # Define colors and create a color cycle
    colors = ['#e6b1deCC', '#b89706CC', '#13870bCC', '#9c051eCC', '#b89706CC', '#d9d0d2CC']
    color_cycle = cycle(colors)

    # Prepare data for graph creation
    if 'interactions' in st.session_state:
        df = pd.DataFrame(list(st.session_state.interactions.items()), columns=['source_target', 'weight'])
        df[['source', 'target']] = pd.DataFrame(df['source_target'].tolist(), index=df.index)
        df.drop(columns='source_target', inplace=True)

        # Create the graph
        G = nx.from_pandas_edgelist(df, source='source', target='target', edge_attr='weight', create_using=nx.Graph())

        # Apply color cycle to nodes
        color_map = {node: next(color_cycle) for node in G.nodes()}

        # Use Pyvis to visualize the network
        net = Network(height="750px", bgcolor="#000", font_color="white")
        
        some_scaling_factor = 0.5  # Define a scaling factor for node sizes

        net.options.physics.enabled = True
        net.options.physics.barnesHut = {
        "gravitationalConstant": -2380,
        "centralGravity": 0.025,
        "springLength": 30,
        "springConstant": 0.01}

        for node in G.nodes():
            interaction_count = sum(df[df['source'] == node]['weight']) + sum(df[df['target'] == node]['weight'])
            size = interaction_count * some_scaling_factor
            net.add_node(node, title=node, color=color_map[node], size=size)

        for edge in G.edges(data=True):
            net.add_edge(edge[0], edge[1], value=edge[2]['weight'])


      # Convert the logo to base64
    logo_base64 = get_image_as_base64("AI_logo.png")

    # Generate the graph HTML
    tmpfile = tempfile.NamedTemporaryFile(delete=False, suffix=".html", mode='w+')
    net.save_graph(tmpfile.name)

    # Read the generated HTML
    with open(tmpfile.name, 'r', encoding='utf-8') as file:
        html_content = file.read()

    # Embed the logo
    logo_html = f"""
    <div style='position: absolute; top: 20px; right: 20px; z-index: 1000;'>
        <img src='data:image/png;base64,{logo_base64}' alt='App logo' style='height: 100px; width: auto;'>
    </div>
    """
    html_content = html_content.replace('<body>', f'<body>{logo_html}')

    # Save the modified HTML content back to the file for download
    with open(tmpfile.name, 'w', encoding='utf-8') as file:
        file.write(html_content)


    # Provide a download button for the HTML file
    with open(tmpfile.name, 'r', encoding='utf-8') as file:
        download_button_html = file.read()


    st.download_button(
        label="Download Your Graph as HTML",
        data=download_button_html,
        file_name="interactive_graph.html",
        mime="text/html"
    )     

        # Display the graph in Streamlit
    st.components.v1.html(html_content, height=800)

