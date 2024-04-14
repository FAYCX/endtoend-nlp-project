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
from facebook import load_data_fb, create_network, show_app
from socialnet import social_network
from timeline import display_network
import base64
from facebook2 import load_network_data, facebook_network

alt.themes.enable("dark")

st.markdown('<style>div.block-container{padding-top:1rem;}</style>',unsafe_allow_html=True)

font_css = """
<style>
    h1 {
        font-family: 'Helvetica Neue', Arial, sans-serif !important;
        font-size: 32px;
        font-weight: bold;
        font-stretch: condensed;
    }

    h2 {
        font-family: 'Helvetica Neue', Arial, sans-serif !important;
        font-size: 26px;
        font-weight: bold;
        font-stretch: condensed;
        color:#fff;
        letter-spacing: 1px;
    }

    h3 {
        font-family: 'Helvetica Neue', Arial, sans-serif !important;
        font-size: 18px;
        font-weight: bold;
        font-stretch: condensed;
        color:#fff;
        letter-spacing: 1px;
    }


    h5 {
        font-family: 'Helvetica Neue', Arial, sans-serif !important;
        color:#85888c;
        font-weight: bold;
        font-stretch: condensed;
    }

    p {
        font-family: 'Helvetica Neue', Arial, sans-serif !important;
        color:#85888c;
        #font-weight: bold;
        font-stretch: condensed;
        font-size:18px;
    }
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
    top: 19px;
    right:0;
    z-index: 999;
    transition: top 0.3s;
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
    
    explore = ["Sentiment Analyzer", "Character Interaction","Facebook Network", "AI Vision", "Timeline",]

    book = ["Pride and Prejudice","Alice's Adventures in Wonderland","A Tale of Two Cities"]


    choice = st.sidebar.selectbox("Explore", explore)
    st.sidebar.markdown("<br><br>", unsafe_allow_html=True)
    book_choice = st.sidebar.selectbox("Book",book)

    st.sidebar.markdown("<br><br>", unsafe_allow_html=True)



   # File upload
    st.subheader("Upload your own file for Analysis and Visualization:")
    uploaded_file = st.file_uploader("Choose a file", type=['txt'])

    if uploaded_file is not None:
        # Check if the file size is within the 10MB limit
        file_size = uploaded_file.size
        if file_size <= 10 * 1024 * 1024:  # Convert 10 MB to bytes
            if uploaded_file.type == "text/plain":
                # Handling text files
                st.write("Filename:", uploaded_file.name)
                st.write("File type:", uploaded_file.type)
                st.write("File size:", file_size, "bytes")
                
                # Read the content of the file
                string_data = uploaded_file.getvalue().decode("utf-8")  # assuming UTF-8 encoding for text files
                st.text_area("File content", string_data, height=300)
            else:
                st.error("Please upload a .txt file only.")
        else:
            # If the file is larger than 10MB
            st.error("The file you are trying to upload is too large. Maximum file size is 10MB.")

def main():
    
    if choice == "Character Interaction":
       #st.title("Visualization")
       social_network()
        

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

    elif choice == "Facebook Network":
        st.title("Facebook Social Network Visualization")
        facebook_network()
        


    elif choice == "AI Vision":

        NER, chapters, text = load_data()

        read_AI(NER, chapters, text)



    else:
        display_network()
        


if __name__ == '__main__':
    main()