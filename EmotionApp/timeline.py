import streamlit as st

# this is for some customized fun nodes GNN

html_content = """
<!DOCTYPE html>
<html style="height:100%; margin:0;">
<head>
<meta charset="UTF-8">
<title>Network Graph</title>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/vis-network/9.1.2/dist/vis-network.min.css" />
<script src="https://cdnjs.cloudflare.com/ajax/libs/vis-network/9.1.2/dist/vis-network.min.js"></script>
<style>
    html, body, #mynetwork {
        height: 100%;
        width:100%
        margin: 0;
        padding: 0;
        overflow: hidden;
    }
</style>
</head>
<body>
<div id="mynetwork"></div>
<script>
    // Define nodes and edges for the graph
    
    var nodes = new vis.DataSet([
        {id: 1, label: 'Node 1'},
        {id: 2, label: 'Node 2'},
        {id: 3, label: 'Node 3'},
        {id: 4, label: 'Node 4'}
    ]);

    var edges = new vis.DataSet([
        {from: 1, to: 2},
        {from: 2, to: 3},
        {from: 3, to: 4},
        {from: 4, to: 1}
    ]);

    var container = document.getElementById('mynetwork');
    var data = {
        nodes: nodes,
        edges: edges
    };
    var options = {};

    // Initialize network
    var network = new vis.Network(container, data, options);

    // Ensure that the network fits well within the container when resized
    window.addEventListener('resize', function () {
        network.fit(); // Automatically adjust view to fit the network
    });
</script>
</body>
</html>
"""

# Streamlit function to display the HTML
def display_network():
    st.title("Network Visualization")
    st.components.v1.html(html_content, height=800, scrolling=True)


