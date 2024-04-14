import streamlit as st
import json
import os

# Path to JSON data
json_file_path = 'graph_data.json'  

# Read the JSON graph data
with open(json_file_path, 'r') as json_file:
    graph_data = json.load(json_file)

# Convert JSON data to string and insert it directly into the HTML template
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

        #mynetwork {{
            width: 100%;
            height: 100vh;
            border: none;
        }}

        /* Custom CSS to override Streamlit defaults */
        .css-1v3fvcr, .css-18e3th9, .css-1d391kg {{
            padding: 0;
            margin: 0;
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
<h1 style="color: #fff;">&lt;Pride and Prejudice&gt; Network</h1>
<div id="mynetwork"></div>
<script>
    document.addEventListener('DOMContentLoaded', function () {{
        const container = document.getElementById('mynetwork');
        const data = {json.dumps(graph_data)};
        const options = {{
            nodes: {{
                shape: 'dot',
                size: 20,
                font: {{
                    size: 15,
                    color: 'white',
                }}
            }},
            edges: {{
                width: 2
            }},
            physics: {{
                barnesHut: {{
                    gravitationalConstant: -30000
                }}
            }}
        }};

        // Initialize the network
        const network = new vis.Network(container, data, options);

        // Ensure that the network fits well within the container when resized
        window.addEventListener('resize', function () {{
            network.fit(); 
        }});
    }});
</script>
</body>
</html>
"""

# Function to display the HTML in Streamlit
def social_network():
    #st.subheader("<Pride and Prejudice> Network")
    st.components.v1.html(html_content, height=800, scrolling=True)

social_network()