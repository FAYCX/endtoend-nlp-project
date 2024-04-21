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


def generate_text(prompt, length=300, temperature=0.65):
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



character_traits = {
    "personality": [
        "curious and brave",
        "sweet and lovely"
        "lovely and gentle",
        "witty and sarcastic",
        "kind and thoughtful",
        "optimistic and energetic",
        "philosophical and introspective",
        "nervous and always in a hurry",
        "reckless and adventurous", 
        "reserved and meticulous",  
        "charming and persuasive",  
        "practical and no-nonsense",  
        "cynical and world-weary",  
        "trusting and naive",  
        "driven and ambitious",  
        "creative and imaginative", 
        "skeptical and inquisitive",  
        "compassionate and empathetic",  
        "haughty and arrogant",  
        "loyal and devoted", 
        "playful and adventurous"
    ],

    "occupation": [  
        "timekeeper",
        "gardener",  
        "journalist", 
        "scientist"
        "merchant", 
        "scholar",  
        "teacher",  
        "nurse",  
        "diplomat", 
        "doctor", 
        "spy", 
        "chief",  
        "wizard",  
        "blacksmith", 
        "navigator", 
        "celebrity", 
        "librarian", 
        "farmer",  
        "sailor",  
        "philosopher",  
        "painter",
        "professor",
        "student",
        "politician",
        "engineer"
    ]
}



def app():

    # User inputs for the story
    st.sidebar.subheader("Configure Your Story")
    genre = st.sidebar.selectbox("Genre", ["Fantasy", "Horror", "Romantic"])
    main_character = st.sidebar.text_input("Main Character", "Alice")
    secondary_character = st.sidebar.text_input("Secondary Character", "Eleanor")
    setting = st.sidebar.text_input("Place", "enchanted forest")
    #plot2 =  st.sidebar.text_area("Plot"," ")

    story_length = st.sidebar.slider("Story Length", 100, 500, 300)
    temperature = st.sidebar.slider("Creativity Temperature", 0.3, 0.9, 0.65)

    if setting == "an enchanted forest":  # Default plot message is unchanged
        st.error('Please use the left sidebar to set the parameters. Your selected genre, characters, and setting elements will actively shapes the course of the story.')

    st.title("Welcome to the Electronic Story Generator!")

    for _ in range(4):
            st.write("")

    st.write("Dive into the world of bespoke storytelling, this generator leverages the transformer model from Hugging Face. Inspired by tracery-like grammar, it dynamically constructs story frameworks, enabling you to customize narratives in ways that expertly blend structured creativity with elements of surprise. Each story unfolds uniquely based on your input prompt, offering a tailored experience that ignites imagination and fosters innovative storytelling. ")


    if st.sidebar.button("Generate Story"):

        create_story(genre, main_character, secondary_character, setting, story_length, temperature)


def create_story(genre, main_character, secondary_character, setting, story_length, temperature):

    #plot = plot2
    #plot = random.choice(plot_elements[genre])  
    Begin = random.choice(Beginning)
    keywords = random.sample(genre_keywords[genre], 2) 

    selected_personality = random.choice(character_traits["personality"])
    selected_occupation = random.choice(character_traits["occupation"])


    selected_personality2 = random.choice(character_traits["personality"])
    selected_occupation2 = random.choice(character_traits["occupation"])
   
  

    prompt = f"""{Begin}, {main_character}, a {selected_personality} {selected_occupation}, found herself in {setting}.
        Alongside her was {secondary_character}, a {selected_personality2} {selected_occupation2}. It unfolds with {keywords[0]} and {keywords[1]}, How will their adventure unfold in this magical {setting}? """

    story = generate_text(prompt, length=story_length, temperature=temperature)
        
    for _ in range(3):
            st.write("")
        
    st.subheader("Your Generated Story:")
    for _ in range(2):
        st.write("")

    st.write(story)

