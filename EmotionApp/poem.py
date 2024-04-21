import streamlit as st
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import random


model_name = 'gpt2'
tokenizer = GPT2Tokenizer.from_pretrained(model_name)
model = GPT2LMHeadModel.from_pretrained(model_name)

font_css = """
<style>
    p {
        font-family: 'Helvetica Neue', Arial, sans-serif !important;
        color:#a6a4a4;
        font-weight: regular;
        
        font-size:18px;
    }
</style>
"""
st.markdown(font_css, unsafe_allow_html=True)


def generate_text(prompt, length=100, temperature=0.7):
    inputs = tokenizer.encode(prompt, return_tensors='pt')
    outputs = model.generate(inputs, max_length=length, temperature=temperature, no_repeat_ngram_size=2)
    text = tokenizer.decode(outputs[0], skip_special_tokens=True)

    return text


Beginning = ["As the leaves started turning golden", "On a rainy Sunday", "On the eve of a great adventure", "It's the most wonderful season of the year", "Under a starlit sky", "During the last days of summer", "When the first snow began to fall", "While the town slept soundly", "On the busiest day of the year"]


genre_keywords = {
    "Fantasy": ["wizard", "spell", "dragon", "kingdom", "enchantment", "beast", "elf", "dwarf", 
    "goblin", "unicorn", "alicorn", "phoenix", "troll", "mermaid", "magic", "alien"],

    "Horror": ["vampire", "ghost", "fear", "death", "curse","demon", "zombie", "possession", "phantom", "cult", "nightmare", "graveyard", "cemetery"],

    "Romantic": ["candlelight", "love", "heart", "romance", "passion", "kiss", "crush","desire", "honeymoon", "valentine", "wedding", "party", "date"]
}


def app():

    # User inputs for the story
    st.sidebar.subheader("Configure Your Story")
    genre = st.sidebar.selectbox("Genre", ["Fantasy", "Horror", "Romantic"])
    main_character = st.sidebar.text_input("Main Character", "Alex")
    secondary_character = st.sidebar.text_input("Secondary Character", "Eleanor")
    setting = st.sidebar.text_input("Setting", "an enchanted forest")
    #plot2 =  st.sidebar.text_area("Plot"," ")

    story_length = st.sidebar.slider("Story Length", 100, 500, 300)
    temperature = st.sidebar.slider("Creativity Temperature", 0.2, 1.0, 0.5)

    if setting == "an enchanted forest":  # Default plot message is unchanged
        st.error('Please use the left sidebar to set the Setting elements. You can choose your genre, characters, and setting elements. Every choice you make actively shapes the course of the story.')

    st.title("Welcome to the Interactive Story Generator!")

    for _ in range(4):
            st.write("")

    st.write("Dive into the world of bespoke storytelling, where each story unfolds uniquely based on your imagination. This app leverages the powerful GPT-2 model from the transformers library, drawing inspiration from tracery-like grammar which dynamically constructs story frameworks, enabling you to customize narratives in ways that blend structured creativity with the element of surprise. ")


    if st.sidebar.button("Generate Story"):

        create_story(genre, main_character, secondary_character, setting, story_length, temperature)


def create_story(genre, main_character, secondary_character, setting, story_length, temperature):

    #plot = plot2
    #plot = random.choice(plot_elements[genre])  
    Begin = random.choice(Beginning)
    keywords = random.sample(genre_keywords[genre], 2) 
    prompt = f"{Begin}, {main_character} and {secondary_character} found themselves in {setting}. The story unfolds with {keywords[0]} and {keywords[1]}, "

    story = generate_text(prompt, length=story_length, temperature=temperature)
        
    for _ in range(3):
            st.write("")
        
    st.subheader("Your Generated Story:")
    for _ in range(2):
        st.write("")

    st.write(story)

