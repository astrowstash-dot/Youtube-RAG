import streamlit as st 
from streamlit import spinner
import time

from functions import (
    extract_vid_id, 
    get_transcript,
    translate_transcript,
    get_important_topics,
    get_notes,
    create_chunks,
    create_vector_store,
    rag_answer
)

# sidebar inputs 


st.title("Homie AI 🎞️🎬")
st.markdown("----")

st.markdown("Homie can transform Youtube videos into key Topics, generate notes or can be your chat buddy.")

youtube_url = st.text_input(":material/youtube: :material/url:",
            placeholder= "https://www.youtube.com/watch?v=")

languages = st.selectbox("**Select a language**:",
            placeholder="en",
            options= ["en", "hi", "sa", "ml", "te", "mr", "or","ar"])

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
            
            if selection == "Chat💬":
                
               with st.spinner("2/3: creating chunks and vector_store..... "):
                   
                   chunks = create_chunks(transcript)
                   vectorstore = create_vector_store(chunks)
                   st.session_state.vector_store = vectorstore
               st.session_state.messages = []
               st.success("Video is ready for chat....")


# chatbot session 
if selection == "Chat💬" and "vector_store" in st.session_state:
    st.divider()
    st.subheader("Chat with video")

   # displaying entire history
    for message in st.session_state.get("messages", []):
        with st.chat_message(message["role"]):
            st.write(message["content"])
    
    # user input 
    prompt = st.chat_input("Ask me anything about the video.")
    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)

        with st.chat_message("assistant"):
           response = rag_answer(prompt, st.session_state.vector_store)
           st.write(response)
        st.session_state.messages.append({"role": "assistant", "content": response})

                











