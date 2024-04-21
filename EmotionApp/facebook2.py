import streamlit as st
import json
import os


# Facebook network GNN

# Read the JSON graph data
@st.cache_data 
def load_network_data():
    json_file_path = 'network_data.json'
    with open(json_file_path, 'r') as json_file:
        network_data = json.load(json_file)
    return network_data

network_data = load_network_data()

# Convert JSON data to string and insert it directly into the HTML template
html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Facebook Social Network</title>
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

        h1 {{
            position: absolute;
            font-weight: bold;
            text-align: center;
            left: 50px;
            top: 0px;
            color: white;
            font-size: 30px;
            z-index:10;
            font-family: 'Helvetica Neue', sans-serif;
            font-weight: bold;
            font-stretch: condensed; 
        }}

        .spinner {{
            border: 16px solid #f3f3f3; /* Light grey */
            border-top: 16px solid #dab6db; /* Pink */
            border-radius: 50%;
            width: 80px;
            height: 80px;
            animation: spin 2s linear infinite;
            position: absolute;
            left: 50%;
            top: 50%;
            transform: translate(-50%, -50%);
        }}

        @keyframes spin {{
            0% {{ transform: translate(-50%, -50%) rotate(0deg); }}
            100% {{ transform: translate(-50%, -50%) rotate(360deg); }}
        }}


        .progress {{
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            font-size: 20px;
            color: white;
            z-index: 1000;
        }}


    </style>
</head>
<body>
<div class="spinner"></div> <!-- Spinner added here -->
<div class="progress">0%</div> <!-- Added this div -->
<div id="mynetwork"></div>
<script>
    document.addEventListener('DOMContentLoaded', function () {{
        const container = document.getElementById('mynetwork');
        const spinner = document.querySelector('.spinner'); // Access the spinner
        const progressText = document.querySelector('.progress');
        const data = {json.dumps(network_data)};
        const options = {{
            nodes: {{
                shape: 'dot',
                size: 40,
                font: {{
                    size: 22,
                    color: 'white',
                }}
            }},
            edges: {{
                width: 5
            }},
            physics: {{
                barnesHut: {{
                    gravitationalConstant: -30000
                }}
            }}
        }};

        // Initialize the network
        const network = new vis.Network(container, data, options);

       // Hide spinner when the network is ready
        network.on("stabilizationIterationsDone", function () {{
            spinner.style.display = 'none';
        }});

        let progress = 0;
            const interval = setInterval(() => {{
                progress += 10;
                if (progress <= 100) {{
                    progressText.innerText = `${{progress}}%`;
                }} else {{
                    clearInterval(interval);
                }}
            }}, 300);

            network.on("stabilizationIterationsDone", function () {{
                clearInterval(interval);
                progressText.style.display = 'none';
            }});

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
def facebook_network():
    st.components.v1.html(html_content, height=800, scrolling=True)

facebook_network()