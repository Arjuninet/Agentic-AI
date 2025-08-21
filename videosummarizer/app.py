import streamlit as st
from phi.agent import Agent
from phi.model.google import Gemini
from phi.tools.duckduckgo import DuckDuckGo
from google.generativeai import get_file, upload_file
import google.generativeai as genai
import time
from pathlib import Path
import tempfile
import os
from dotenv import load_dotenv
load_dotenv()

API_KEY = os.getenv("GOOGLE_API_KEY")

if API_KEY:
    genai.configure(api_key = API_KEY)

#Page Configuration
st.set_page_config(
    page_title="Video Summarizer",
    page_icon=":movie_camera:",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("AI Video Summarizer Agent")
st.header("Powered by Gemini and DuckDuckGo")

@st.cache_resource
def initialize_agent():
    return Agent(
            name="Video Summarizer Agent",
            model=Gemini(id="gemini-2.0-flash-exp"),
            tools=[DuckDuckGo()],
            markdown=True
            )

#Initialize the agent
mutimodel_agent = initialize_agent()

#File Uploader
video_file = st.file_uploader("Upload a video file", type=["mp4", "avi", "mov", "mkv"])

if video_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_file:
        temp_file.write(video_file.read())
        temp_file_path = temp_file.name
    
    st.video(temp_file_path, format="video/mp4", start_time=0)

    user_query = st.text_area(
        "What insight are you seeking from this video?",
        placeholder="Ask about the content, key points, or any specific details you want to know about the video.",
        help = "Provide specific question or insight you want from the video.",
    )

    if st.button("Summarize Video", key="Analyze_video_button"):
        if not user_query:
            st.warning("Please enter a query to summarize the video.")
        else:
            try:
                with st.spinner("Analyzing Video..."):
                    #Upload and analyze the video
                    processed_video = upload_file(temp_file_path)
                    while processed_video.state.name == "PROCESSING":
                        time.sleep(1)
                        processed_video = get_file(processed_video.name)
                    
                    #Anasyses prompt
                    analysis_prompt = (
                    f"""
                    Analysez the uploaded video for the content and context.
                    Provide a detailed summary of the video content, key points, and any relevant insights.
                    Use the following query to guide your analysis: {user_query}

                    Provide a detailed, user-friendly and actionable response.                    
                    """)
                    response  = mutimodel_agent.run(
                        analysis_prompt,
                        files=[processed_video]
                    )
                
                #Display the response
                st.subheader("Video Summary")
                st.markdown(response.content)
            except Exception as error:
                st.error(f"An error occurred while processing the video: {error}")
            finally:
                Path(temp_file_path).unlink(missing_ok=True)  # Clean up the temporary file\
    else:
        st.info("Upload a video and enter a query to get started.")

#customize text area height
st.markdown(
    """
    <style>
    .stTextArea textarea {
        height: 100px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

    

