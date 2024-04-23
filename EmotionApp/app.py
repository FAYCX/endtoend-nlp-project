import sys
import subprocess
import os

# Print Python executable path
#print("Python executable:", sys.executable)

# List installed packages
#subprocess.run(["pip", "list"])


#print("Current working directory:", os.getcwd())
#print("Files in the current directory:", os.listdir())

import streamlit as st

st.set_page_config(
    page_title="The Mosaic Mind of AI",   # Set the page title here
    layout="wide",
    initial_sidebar_state="expanded",
)


import pandas as pd
import numpy as np
import joblib
import altair as alt
from datavis import read_AI, load_data
from socialnet import social_network
from timeline import display_network
import base64
from facebook2 import load_network_data, facebook_network

from alice import alice_network
from pipeline import main_pipe

import tempfile
from itertools import cycle

from poem import generate_text, app

#alt.themes.enable("dark")

# Read the CSS file
with open('style.css', 'r') as f:
    css = f.read()

# Embed the CSS in the Streamlit app
st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)

st.markdown('<style>div.block-container{padding-top:1rem;}</style>',unsafe_allow_html=True)

white_color = "#fff"
h1 = "1.9rem"
h2 = "1.6rem" 
h3 = "1.2rem" 
p = "1rem"

font_css = f"""
<style>
    /* Base styles */
    body {{
        margin: 0;
        padding: 0;
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100vh;
    }}

    .title-box {{
        padding: 10px;
        margin: 10px;
        background-color: #333;  /* Dark background for the title box */
        color: {white_color};
        border-radius: 10px;
        box-shadow: 0.4px 6px rgba(0,0,0,0.1);
        transition: all 0.3s ease-in-out;
    }}

    h1 {{
        font-family: 'Helvetica Neue', Arial, sans-serif !important;
        font-size: {h1};
        font-weight: bold;
        font-stretch: condensed;
        margin: 0;
        letter-spacing: 0.08rem;
    }}

     h2 {{
        font-family: 'Helvetica Neue', Arial, sans-serif !important;
        font-size: {h2};
        font-weight: bold;
        font-stretch: condensed;
        letter-spacing: 0.02rem;
    }}

    h3 {{
        font-family: 'Helvetica Neue', Arial, sans-serif !important;
        font-size: {h3};
        font-weight: bold;
        font-stretch: condensed;
        letter-spacing: 0.01rem;
        color: #edcce8;
    }}

    h5, p {{
        font-family: 'Helvetica Neue', Arial, sans-serif !important;
        color: #85888c;
        font-size: {p};
    }}

    /* Adjustments for smaller screens */
    @media (max-width: 480px) {{
        .title-box {{
            padding: 10px;
            margin: 10px;
        }}

        h1 {{
            font-size: 1.4rem;
        }}

   
    }}

    h2 {{
        font-family: 'Helvetica Neue', Arial, sans-serif !important;
        font-size: {h2};
        font-weight: bold;
        font-stretch: condensed;
        letter-spacing: 0.02rem;
    }}

    h3 {{
        font-family: 'Helvetica Neue', Arial, sans-serif !important;
        font-size: {h3};
        font-weight: bold;
        font-stretch: condensed;
        letter-spacing: 0.01rem;
        
    }}

    h5, p {{
        font-family: 'Helvetica Neue', Arial, sans-serif !important;
        color: #dbdbdb;
        font-size: {p};
    }}
</style>
"""

st.markdown(font_css, unsafe_allow_html=True)


def get_image_as_base64(path):
    """ Convert image file to base64 string """
    with open(path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()

# Load the image file and convert to base64
logo_base64 = get_image_as_base64("AI_logo.png")

# Define custom HTML to display the image
logo_html = f"""
<style>
#logo {{
    position: absolute;
    top: 1vw;
    right:0;
    height:5w;
    max-height:150px;
    width:auto;
    z-index: 999;
    transition: top 0.3s;
}}

@media (max-width:768px){{
    #logo {{
    top: 0.5vw;
    height:8vw;

    }}
}}
</style>
<img id="logo" src="data:image/png;base64,{logo_base64}" alt="App logo" style="height: 150px; width: auto;">
"""

# Display the logo
st.markdown(logo_html, unsafe_allow_html=True)





# Load your trained model
pipe_lr = joblib.load(open("models/emotion_classifier_pipe_lr_Mar29_2024.pkl", "rb"))

# Prediction Function
def predict_emotions(docx):
    results = pipe_lr.predict([docx])
    return results[0]  # Return the first and only item

# Get Prediction Probabilities
def get_prediction_proba(docx):
    results = pipe_lr.predict_proba([docx])
    return results

# Emoji Dictionary for Emotions
emotions_emoji_dict = {"anger": "😤", "disgust": "🤢", "fear": "😨", "joy": "😸", "surprise": "😻", "neutral": "😶", "sadness": "😭", "shame":"🫣"}




# Sidebar
with st.sidebar:
    st.header("Explore the Distant Reading Journey with AI")
    
    explore = ["Social Network Visualization", "Sentiment Analyzer", "Generate Your Own", "AI Vision"]

    net = ["Pride and Prejudice", "Facebook Social Net", "Alice's Adventures in Wonderland"]

    create = ["Your Social Graph", "Your Own Story"]


    choice = st.sidebar.selectbox("Explore", explore)
    st.sidebar.markdown("<br><br>", unsafe_allow_html=True)

    #create_choice = st.sidebar.selectbox("Generate", create)




def collect_interactions():
    with st.sidebar.form(key='interaction_form'):
        st.write("Add Character Interaction")
        source = st.text_input("Character One", help="Name of the source character.")
        target = st.text_input("Character Two", help="Name of the target character.")
        interaction_count = st.number_input("Interaction Frequency", min_value=1, max_value=100, help="How many times have these characters interacted?")
        submit_button = st.form_submit_button(label='Add Interaction')

        if submit_button:
            # Initialize the interactions dictionary in session state if it doesn't exist
            if 'interactions' not in st.session_state:
                st.session_state.interactions = {}
            
            # Key for interactions is the tuple (source, target)
            interaction_key = (source, target)
            
            # Update the interaction count or set it if not present
            if interaction_key in st.session_state.interactions:
                st.session_state.interactions[interaction_key] += interaction_count
            else:
                st.session_state.interactions[interaction_key] = interaction_count
            
            # Confirm addition of the interaction
            st.success(f"Added interaction: {source} - {target} ({st.session_state.interactions[interaction_key]} times)")

def display_interactions():
    if 'interactions' in st.session_state and st.session_state.interactions:
        for (source, target), count in st.session_state.interactions.items():
            st.sidebar.write(f"{source} - {target}, {count} times")

  

def main():
    
    if choice == "Social Network Visualization":
        net_choice = st.sidebar.selectbox("Choose dataset", net)

        if choice == "Social Network Visualization" and net_choice == "Pride and Prejudice":
            st.title("<Pride and Prejudice> Social Architecture")

            social_network()

        if choice == "Social Network Visualization" and net_choice == "Facebook Social Net":

            st.title("Facebook Social Network Visualization")
            facebook_network()

        if choice == "Social Network Visualization" and net_choice == "Alice's Adventures in Wonderland":
            alice_network()





    elif choice == "Sentiment Analyzer":
        st.title("Sentiment Analyzer Bot")
        st.write("🤖:'Trying my best to understand human emotion'")

        for _ in range(3):
            st.write("")

        with st.form(key='emotion_clf_form'):
            raw_text = st.text_area("Please Type any text here")
            submit_text = st.form_submit_button(label='submit')

        if submit_text:
            col1, col2 = st.columns(2)

            prediction = predict_emotions(raw_text)
            probability = get_prediction_proba(raw_text)

            with col1:
                st.success("Your Text")
                st.write(raw_text)

                st.success("My Prediction")
                emoji_icon = emotions_emoji_dict.get(prediction, "😶")  # Safely get the emoji, default to neutral if not found
                st.write(f"{prediction} {emoji_icon}")
                st.write("My Confidence:{}".format(np.max(probability)))

            with col2:
                st.success("Prediction Probability")
                # You might want to improve this to display it better
                #st.write(probability)
                proba_df = pd.DataFrame(probability,columns=pipe_lr.classes_)
                #st.write(proba_df.T)
                proba_df_clean = proba_df.T.reset_index()
                proba_df_clean.columns = ["emotions","probability"]

                fig = alt.Chart(proba_df_clean).mark_bar().encode(x='emotions',y='probability',color='emotions')
                st.altair_chart(fig,use_container_width=True)
        


    elif choice == "AI Vision":

        NER, chapters, text = load_data()

        read_AI(NER, chapters, text)



    elif choice == "Generate Your Own":
        create_choice = st.sidebar.selectbox("Choose type", create)

        if choice == "Generate Your Own" and create_choice == "Your Social Graph":

            collect_interactions()
            display_interactions()

            main_pipe()

        elif choice == "Generate Your Own" and create_choice == "Your Own Story":

            app()
            




if __name__ == '__main__':
    main()