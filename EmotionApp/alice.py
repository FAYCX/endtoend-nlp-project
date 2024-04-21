import streamlit as st
import json
import os




# Path to JSON data
json_file_path = 'alicewonder_data.json' 


# Read the JSON graph data
with open(json_file_path, 'r') as json_file:
    alice_data = json.load(json_file)


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
<h1 style="color: #fff;">&lt;Alice in Wonderland&gt; Network</h1>
<div id="mynetwork"></div>
<script>
    document.addEventListener('DOMContentLoaded', function () {{
        const container = document.getElementById('mynetwork');
 
        const data = {json.dumps(alice_data)};
        data.nodes.forEach(node => {{
            node.size = node.value; // Ensure that the node size is set from the 'value' attribute
        }});
        const options = {{
              nodes: {{
        shape: 'dot',
        scaling: {{
            min: 10,    // Minimum size of nodes
            max: 800,    // Maximum size of nodes
            label: {{
                enabled: true,
                min: 10,
                max: 500,
                maxVisible: 100,
                drawThreshold: 50
            }},
            customScalingFunction: function (min,max,total,value) {{
                return value/total;
            }}
        }},
        font: {{
            size: 12,
            color: 'white'
        }}
    }},
            edges: {{
                width: 2
            }},
            physics: {{
                barnesHut: {{
                    gravitationalConstant: -27380,
                    centralGravity: 0.025,
                    springLength: 425,
                    springConstant: 0.05
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
def alice_network():
    st.components.v1.html(html_content, height=800, scrolling=True)

alice_network()