import streamlit as st
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import random
import json


model_name = 'gpt2'
tokenizer = GPT2Tokenizer.from_pretrained(model_name)
model = GPT2LMHeadModel.from_pretrained(model_name)

font_css = """
<style>
    p {{
        font-family: 'Helvetica Neue', Arial, sans-serif !important;
        color:#013605;
        font-weight: regular;
        font-size:18px;
    }}
</style>
"""
st.markdown(font_css, unsafe_allow_html=True)


def generate_text(prompt, length=300, temperature=0.65):
    inputs = tokenizer.encode(prompt, return_tensors='pt')
    outputs = model.generate(inputs, max_length=length, temperature=temperature, no_repeat_ngram_size=2)
    text = tokenizer.decode(outputs[0], skip_special_tokens=True)

    return text


books = json.load(open("books.json"))

celebrities = json.load(open("celebrities.json"))

president_quotes = json.load(open("president_quote.json"))



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
        "scientist",
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
    setting = st.sidebar.text_input("Place", "coffee shop")
    #plot2 =  st.sidebar.text_area("Plot"," ")

    story_length = st.sidebar.slider("Story Length", 100, 500, 300)
    temperature = st.sidebar.slider("Creativity Temperature", 0.3, 0.9, 0.65)

    if setting == "an enchanted forest":  # Default plot message is unchanged
        st.error('Please use the left sidebar to set the parameters. Your selected genre, characters, and setting elements will actively shapes the course of the story.')

    st.title("Welcome to the Electronic Story Generator!")

    for _ in range(5):
            st.write("")

    st.write("Dive into the world of bespoke storytelling with our generator, crafted in two distinct parts. First two-thirds of each narrative is meticulously shaped using a tracery-like grammar structure personally curated by me, weaving elements like real book titles, presidential quotes, and celebrity names into the fabric of the storytelling. The remaining third leverages the power of the GPT-2 model to generate the rest, based on the clues from the prompt we collaboratively create in the initial sentences. Each narrative unfolds uniquely based on your input, providing a tailored experience that ignites the imagination and curiosity, fostering innovative storytelling through electronic text and the mathematical algorithms within the AI mind.")


    if st.sidebar.button("Generate Story"):

        create_story(genre, main_character, secondary_character, setting, story_length, temperature)


def create_story(genre, main_character, secondary_character, setting, story_length, temperature):
    
    # Random selections for story elements
    Begin = random.choice(Beginning)
    keywords = random.sample(genre_keywords[genre], 2)

    selected_personality = random.choice(character_traits["personality"])
    selected_occupation = random.choice(character_traits["occupation"])
    selected_book = random.choice(books)
    selected_book2 = random.choice(books)
    selected_celebrities = random.choice(celebrities)
    selected_president = random.choice(president_quotes)
    selected_name = selected_president['name']
    selected_quote = random.choice(selected_president['quotes'])
    selected_personality2 = random.choice(character_traits["personality"])
    selected_occupation2 = random.choice(character_traits["occupation"])


    # Generate the prompt
    prompt = f"""
{Begin}, {main_character}, a {selected_personality} {selected_occupation}, settled into a quiet nook with the book, '{selected_book}', at the most enchanting {setting} in town. 
Next to her, {secondary_character}, a {selected_personality2} {selected_occupation2}, was engrossed in '{selected_book2}' at the neighboring nook. 
Suddenly, a distinct voice in the distance began reciting "{selected_quote}". 
"Could that possibly be the President {selected_name}?" {main_character} mused, her gaze still fixed on her page. 
As the voice drew nearer, {main_character} finally looked up to see none other than {selected_celebrities} approaching! 
This story is all about {keywords[0]} and {keywords[1]}. 
Why was {selected_celebrities} there, and what adventures await in this magical {setting}?
"""



    story = generate_text(prompt, length=story_length, temperature=temperature)
        
    for _ in range(3):
            st.write("")
        
    st.subheader("Your Generated Story:")
    for _ in range(2):
        st.write("")

    st.write(story)

