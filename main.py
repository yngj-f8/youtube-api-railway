from fastapi import FastAPI, Query
from auth import AuthMiddleware
from youtube_utils import get_transcript
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize FastAPI application
app = FastAPI()
# Add authentication middleware to the application
app.add_middleware(AuthMiddleware)

@app.get("/transcript")
def transcript(video_id: str = Query(...)):
    """
    Endpoint to retrieve YouTube video transcript.
    
    Args:
        video_id (str): YouTube video ID (required query parameter)
        
    Returns:
        dict: Transcript data or error message
    """
    return get_transcript(video_id)

@app.get("/video_info")
def video_info(video_id: str):
    """
    Endpoint to retrieve YouTube video information.
    
    Args:
        video_id (str): YouTube video ID
        
    Returns:
        dict: Video information (title, author, publish date, thumbnail URL) or error message
    """
    return get_video_info(video_id)
