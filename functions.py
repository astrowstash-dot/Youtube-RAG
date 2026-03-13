import time 

from dotenv import load_dotenv
import re
import streamlit as st

from youtube_transcript_api import YouTubeTranscriptApi

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

def extract_vid_id(url):

    """To extract video id from Youtube URL"""

    pattern = r"(?:v=|/)([A-Za-z0-9_-]{11})"   # either v= or / but (?:) dont capture the group
    match_obj = re.search(pattern,url)

    if match_obj:
        return match_obj.group(1)
    st.error("Invalid Youtube URL. Please enter a valid URL")
    return None 


# function to get transcript of the video
def get_transcript(video_id,language):
    YT_api = YouTubeTranscriptApi()

    try:
        transcript = YT_api.fetch(video_id,language[language])
        full_transcript = " ".join([i.text for i in transcript])
        time.sleep(8)
        return full_transcript
    except Exception as e:
        st.error(f'Error fetching video transcript {e}')

# initialize the gemini model 

llm = ChatGoogleGenerativeAI(
    model = "gemini-2.5-flash-lite",
    temperature = 0.2     
)

# function to translate transcript into eng language

def translate_transcript(transcript):

    try:
        Prompt = ChatPromptTemplate().from_template("""
        You are an expert translator with deep cultural and linguistic knowledge.
        I will provide you with a transcript. Your task is to translate it into English with absolute accuracy, preserving:
        - Full meaning and context (no omissions, no additions).
        - Tone and style (formal/informal, emotional/neutral as in original).
        - Nuances, idioms, and cultural expressions (adapt appropriately while keeping intent).
        - Speaker’s voice (same perspective, no rewriting into third-person).
        Do not summarize or simplify. The translation should read naturally in the target language but stay as close as possible to the original intent.
        
        transcript : {transcript} """)

        chain = Prompt|llm

        # Run chain
        result = chain.invoke({"transcript":transcript})
        return result.content
    
    except Exception as e :
        st.error (f'Fetching Error: {e}')

 # function to get imp topics
def get_important_topics(transcript):
    try:
        prompt = ChatPromptTemplate.from_template("""
               You are an assistant that extracts the 5 most important topics discussed in a video transcript or summary.

               Rules:
               - Summarize into exactly 5 major points.
               - Each point should represent a key topic or concept, not small details.
               - Keep wording concise and focused on the technical content.
               - Do not phrase them as questions or opinions.
               - Output should be a numbered list.
               - show only points that are discussed in the transcript.
               Here is the transcript:
               {transcript}
               """)

        # Runnable chain
        chain = prompt | llm

        # Run chain
        response = chain.invoke({"transcript": transcript})

        return response.content

    except Exception as e:
        st.error(f"Error fething topics {e}")


# functions to generate notes from video
def get_notes(transcript):
    try:
        prompt = ChatPromptTemplate().from_template("""
            You are an AI note-taker. Your task is to read the following YouTube video transcript 
                and produce well-structured, concise notes.

                ⚡ Requirements:
                - Present the output as **bulleted points**, grouped into clear sections.
                - Highlight key takeaways, important facts, and examples.
                - Use **short, clear sentences** (no long paragraphs).
                - If the transcript includes multiple themes, organize them under **subheadings**.
                - Do not add information that is not present in the transcript.
                
            Here is the transcript:
            {transcript}""")
        
        # Runnable chain
        chain = prompt | llm
        result = chain.invoke({"transcript":transcript})

    except Exception as e:
        st.error ("Fetching notes failed: {e}")

# **chunk to rag **

# function to create chunks
def create_chunks(transcript):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap= 1000)
    docs = text_splitter.create_documents([transcript])
    return docs


# function to create embedding and store it into an vector space.

def create_vector_store(transcript):
    embedding = GoogleGenerativeAIEmbeddings(model="gemini-embedding-001")  
    embedding.embed_query(transcript)