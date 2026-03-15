import streamlit as st 
from streamlit import spinner
import time

from functions import (
    extract_vid_id, 
    get_transcript,
    translate_transcript,
    get_important_topics,
    get_notes
)

# sidebar inputs 


st.title("Homie AI 🎞️🎬")
st.markdown("----")

st.markdown("Homie can transform Youtube videos into key Topics, generate notes or can be your chat buddy.")

youtube_url = st.text_input(":material/youtube: :material/url:",
            placeholder= "https://www.youtube.com/watch?v=")

languages = st.selectbox("**Select a language**:",
            placeholder="en",
            options= ["en", "hi", "sa", "ml", "te", "mr", "or"])

selection = st.radio ("what you would like HomieAI to do ?",
           options=["Notes📝", "Chat💬"],
           captions= ["Generate notes from video", "Chat with the video"],
           index=None)

button = st.button("Generate", icon="🛸", type="primary")
if button:
    with st.spinner("loading", show_time=True):
       time.sleep(2)

# flow---------

if button:
    if youtube_url and languages:
        video_id = extract_vid_id(youtube_url)
        if video_id:
            with st.spinner("step 1/3: fetching transcript..."):
               transcript = get_transcript(video_id,languages)

            if languages!="en":
                with spinner("step 1.5/3: translating transcript into English, This may take a few moments...."):
                   transcript = translate_transcript(transcript)

            if selection == "Notes📝":
                with st.spinner("step 2/3: Extracting important topics..."):
                   topics = get_important_topics(transcript)
                   st.write (topics)
                   st.markdown("----")

                with st.spinner("step 3/3: generating notes...."):
                   notes = get_notes(transcript)

                # addd the loding bar -----------------
                   st.write (notes)
                   st.markdown("-----")
                st.success("Summary and Notes Generated.")
            
         #   if selection == "Chat💬":










