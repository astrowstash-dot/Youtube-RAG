import time 

from dotenv import load_dotenv
import re
import streamlit as st

from youtube_transcript_api import YouTubeTranscriptApi

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_chroma import Chroma
from langchain_core.prompts import PromptTemplate

load_dotenv()

def extract_vid_id(url):

    """To extract video id from Youtube URL"""

    pattern = r"(?:v=|/)([A-Za-z0-9_-]{11})"   # either v= or / but (?:) dont capture the group
    match_obj = re.search(pattern,url)

    if match_obj:
        return match_obj.group(1)
    st.error("Invalid Youtube URL. Please enter a valid URL")
    return None








