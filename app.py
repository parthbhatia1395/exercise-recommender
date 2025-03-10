import streamlit as st
import google.generativeai as genai
import tempfile
import time


# Calling the google api key
google_api_key = st.secrets["general"]["api_key"]

genai.configure(api_key=google_api_key)


# Main app design starts from here

## Header -> Exercise is all you need
html_content = """
<h1 style='text-align: left;'>
    <span style="font-size: 48px; font-style: italic; 
                 background: linear-gradient(to right, #8B0000, #FF8C00, #FFD700); 
                 -webkit-background-clip: text;
                 -webkit-text-fill-color: transparent;">
        Exercise is all you Need
    </span>
    <span style="font-size: 70px;">&#127939;</span>
</h1>
"""

st.markdown(html_content, unsafe_allow_html=True)

# Initializing session state for the selected model and conversation history
if 'selected_model' not in st.session_state:
    st.session_state.selected_model = "gemini-1.5-flash"  # Default model

if 'conversation' not in st.session_state:
    st.session_state.conversation = []

# function to reset chat conversation history once model is changed
def reset_conversation():
    st.session_state.conversation = []

# function to save chat history during successive api calls
def add_to_conversation(prompt, response):
    st.session_state.conversation.append({"prompt": prompt, "response": response})

# Model to be chosen for running the app
selected_model = st.sidebar.selectbox(label='Choose your model',options=['gemini-2.0-flash','gemini-1.5-flash','gemini-1.5-pro'],key='model_selector')

# Checking if the model has been changed by the end user
if selected_model != st.session_state.selected_model:
    st.session_state.selected_model = selected_model
    reset_conversation()  # Resetting the conversation history

# Temperature setting to be used for the models
# if selected_model == 'gemini-1.0-pro (supports text only)':
#     temp = st.sidebar.select_slider('Temperature, *(increasing this will get you more creative outputs)*',options=[0.0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0,1.2],value=0.0)
# else:
#     temp = st.sidebar.select_slider('Temperature, *(increasing this will get you more creative outputs)*',options=[0.0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0,1.2,1.5,1.7,2.0],value=0.0)

# Temperature setting to be used for the models
temp = st.sidebar.select_slider('Temperature, *(increasing this will get you more creative outputs)*',options=[0.0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0,1.2,1.5,1.7,2.0],value=0.0)


# Defining which model to be used and storing it in a variable which will then be fed into the api
# model_to_use = 'gemini-1.0-pro' if selected_model == 'gemini-1.0-pro (supports text only)' else selected_model
model_to_use = selected_model

# This is the video file which needs to be uploaded to a temp path so that it can be fed into the gemini api,
# works only when gemini-2.0-flash, gemini-1.5-flash or gemini-1.5-pro is selected
# if model_to_use != 'gemini-1.0-pro':
vfile = st.sidebar.file_uploader("Upload your workout video for suggestion")

if vfile is not None:
    # Saving the video file uploaded from streamlit to a temporary directory
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_file:
        temp_file.write(vfile.read())
        video_path = temp_file.name
    
        # uploading the video file to a temp path and saving it in a variable which the gemini api can call later 
        video_file = genai.upload_file(path=video_path)


        # sanity checks
        while video_file.state.name == "PROCESSING":
            print('.', end='')
            time.sleep(10)
            video_file = genai.get_file(video_file.name)
        
        if video_file.state.name == "FAILED":
            raise ValueError(video_file.state.name)



#Prompt list below
            
# Starting prompt for gemini-2.0-flash, gemini-1.5-flash and gemini-1.5-pro          
start_prompt ="Introduce yourself as a fitness buddy"

# # Starting prompt for gemini-1.0-pro 
# start_prompt2 = "Introduce yourself as a fitness buddy in short and crisp manner"


# Prompt for gemini-2.0-flash, gemini-1.5-flash and gemini-1.5-pro
p4 = """
Hi Gemini! You are a Gym instructor and you need to give suggestions based on which type of exercise the person is doing or asking about.
The person may give a video of their workout and ask suggestion about it or they might just ask about an exercise without giving the workout video,
you need to handle both the cases effectively.
You may ask follow up questions, but try to give your best response based on a single user input

Only tell that you are a Gym Instructor if the person asks you about yourself.
Also if the person asks about on how to use the app, tell the person that they can upload their workout video
and an input prompt to get suggestion about their exercise or just ask something related to an exercise.
Also try to give the correct duration of the exercise in the video if the user asks about it. 
"""

# # Prompt for gemini-1.0-pro 
# p7 = """
# Role: Fitness Buddy

# Guidelines:
# 1. Provide exercise suggestions based on user queries without asking follow-up questions.
# 2. Mention theat you are a Virtual Fitness Buddy if asked.
# 3. If asked about app usage, explain that users can inquire about workouts or exercises for
# suggestions.
# 4. If asked about dietary requirements you need to provide the same.
# """


# Chat Completion Logic

# # Chat completion code logic when the gemini-1.0-pro model is selected
# if model_to_use == 'gemini-1.0-pro':
#     model = genai.GenerativeModel(
#     model_to_use,
#     generation_config=genai.GenerationConfig(
#         max_output_tokens=2000,
#         temperature=temp,
#     ))
#     starting_response = model.generate_content(start_prompt2)
#     st.markdown("<b style='color:#01D78D;'>Fitness Buddy: </b>" + starting_response.text, unsafe_allow_html=True)

#     user_prompt = st.chat_input("Ask anything about your workout...")

#     if user_prompt is not None:
#         chat_history = "\n".join([f"{entry['prompt']}\n{entry['response']}" for entry in st.session_state.conversation])
#         full_prompt = f"{p7}\n{chat_history}\n{user_prompt}"
#         response = model.generate_content(full_prompt)
#         add_to_conversation(user_prompt,response.text)

#     # Displaying the conversation history for gemini-1.0-pro
#     for entry in st.session_state.conversation:
#         st.markdown(f"<b style='color:#2491F9;'>Me:</b> {entry['prompt']}", unsafe_allow_html=True)
#         st.markdown(f"<b style='color:#01D78D;'>Fitness Buddy:</b> {entry['response']}", unsafe_allow_html=True)

# Chat completion code logic when the gemini-2.0-flash, gemini-1.5-flash or gemini-1.5-pro model is selected

model = genai.GenerativeModel(
model_to_use,
system_instruction=p4,
generation_config=genai.GenerationConfig(
    max_output_tokens=2000,
    temperature=temp,
))
starting_response = model.generate_content(start_prompt)
st.markdown("<b style='color:#01D78D;'>Fitness Buddy: </b>" + starting_response.text, unsafe_allow_html=True)

user_prompt = st.chat_input("Ask anything about your workout...")

if user_prompt is not None and vfile is None:
    chat_history = "\n".join([f"{entry['prompt']}\n{entry['response']}" for entry in st.session_state.conversation])
    full_prompt = f"{chat_history}\n{user_prompt}"
    response = model.generate_content(full_prompt)
    add_to_conversation(user_prompt,response.text)

elif user_prompt is not None and vfile is not None:
    chat_history = "\n".join([f"{entry['prompt']}\n{entry['response']}" for entry in st.session_state.conversation])
    full_prompt = f"{chat_history}\n{user_prompt}"
    response = model.generate_content([full_prompt, video_file], request_options={"timeout": 600})
    add_to_conversation(user_prompt,response.text)

# Displaying the conversation history for the models gemini-2.0-flash, gemini-1.5-flash and gemini-1.5-pro
for entry in st.session_state.conversation:
    st.markdown(f"<b style='color:#2491F9;'>Me:</b> {entry['prompt']}", unsafe_allow_html=True)
    st.markdown(f"<b style='color:#01D78D;'>Fitness Buddy:</b> {entry['response']}", unsafe_allow_html=True)










