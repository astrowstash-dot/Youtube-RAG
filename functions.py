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










