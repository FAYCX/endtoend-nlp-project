import streamlit as st
import pandas as pd
from pyvis.network import Network
from itertools import cycle
import os
import re

# Ensure the directory for saving the network exists
os.makedirs('networks', exist_ok=True)


# CSS styling
st.markdown("""
<style>
iframe {
    position: absolute;
    border: none; /* Remove border */
    margin: 0px; /* Remove margin */
    width: 100%; /* Full width */
    height: 100%; /* Full height */
}

#root {
    margin: 0px; /* Remove margin around the root container */
    padding: 0px; /* Remove padding around the root container */
}

body, html {
    margin: 0px; /* Ensure no margin for body and html */
    padding: 0px; /* Ensure no padding for body and html */
    overflow: hidden; /* Hide scrollbars */
    background-color: black; /* Ensure background is black */
}

#loadingBar {
    position: absolute;
    top: 0px;
    left: 0px;
    width: 80%;
    height: 700px;
    background-color: rgba(0, 0, 0, 0.8);
    -webkit-transition: all 0.5s ease;
    -moz-transition: all 0.5s ease;
    -ms-transition: all 0.5s ease;
    -o-transition: all 0.5s ease;
    transition: all 0.5s ease;
    opacity: 1;
}

div.outerBorder {
    position: relative;
    /* top: 400px; */
    width: 500px;
    height: 30px;
    margin: auto auto auto auto;
    border: 0px solid rgba(0, 0, 0, 0.1);
    background: rgb(252, 252, 252);
    background: -moz-linear-gradient(top, rgba(252, 252, 252, 1) 0%, rgba(0, 0, 0, 1) 100%);
    background: -webkit-gradient(linear, left top, left bottom, color-stop(0%, rgba(252, 252, 252, 1)), color-stop(100%, rgba(237, 237, 237, 1)));
    background: -webkit-linear-gradient(top, rgba(252, 252, 252, 1) 0%, rgba(237, 237, 237, 1) 100%);
    background: -o-linear-gradient(top, rgba(252, 252, 252, 1) 0%, rgba(237, 237, 237, 1) 100%);
    background: -ms-linear-gradient(top, rgba(252, 252, 252, 1) 0%, rgba(237, 237, 237, 1) 100%);
    background: linear-gradient(to bottom, rgba(252, 252, 252, 1) 0%, rgba(237, 237, 237, 1) 100%);
    filter: progid:DXImageTransform.Microsoft.gradient( startColorstr='#fcfcfc', endColorstr='#ededed',GradientType=0 );
    border-radius: 0px;
    box-shadow: 0px 0px 0px rgba(0,0,0,0.2);
}

::-webkit-scrollbar {
    /* background: transparent; */
    /* border-radius: 100px; */
    /* height: 6px; */
    /* width: 6px; */
}

</style>
""", unsafe_allow_html=True)



@st.cache_data
def load_data_fb():
    # Load the data
    data = pd.read_csv("facebook_combined.txt", sep=" ", header=None)
    data.columns = ["person1", "person2"]
    sample = data.sample(1000, random_state=1)
    return sample

sampled_data = load_data_fb()

@st.cache_data
def create_network(sample):
    # Create a Pyvis network
    net = Network(height="1000px", width="100%", bgcolor="#000000", font_color="white")

    # Set up nodes and colors
    nodes = set(sample['person1']).union(set(sample['person2']))
    colors = ['#c1e1f5', '#f2cee0', '#7f47ad', '#71bd62', '#428036', '#b5f5d9','#094dad','#f5d5ea','#edc7ce']
    color_cycle = cycle(colors)

    # Add nodes to the network with unique colors
    for node in nodes:
        net.add_node(node, label=str(node), color=next(color_cycle))

    # Add edges to the network
    for edge in sample.values.tolist():
        net.add_edge(edge[0], edge[1])

    # Display controls and save to a temporary HTML file
    net.show_buttons(filter_="physics")
    path = "facebook_network.html"
    net.save_graph(path)
    return path

@st.cache_data
def show_app():
    sample = load_data_fb()
    path = create_network(sample)
    
    # Use Streamlit components to display the HTML file
    HtmlFile = open(path, 'r', encoding='utf-8')
    source_code = HtmlFile.read() 
    st.components.v1.html(source_code, height=800, scrolling=True)  # Adjust height as needed




