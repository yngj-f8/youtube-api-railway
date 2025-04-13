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

@app.get("/channel_info")
def channel_info(channel_id: str):
    """
    Endpoint to retrieve detailed information about a YouTube channel.
    
    Args:
        channel_id (str): YouTube channel ID
        
    Returns:
        dict: Channel information including:
            - title: Channel title
            - description: Channel description
            - thumbnail_url: Channel thumbnail URL
            - subscriber_count: Number of subscribers
            - video_count: Total number of videos
        Returns an error message if the channel is not found or if an error occurs
    """
    return get_channel_info(channel_id)

@app.get("/thumbnail_link")
def thumbnail_link(video_id: str):
    """
    Endpoint to retrieve YouTube video links and thumbnail URLs.
    
    Args:
        video_id (str): YouTube video ID
        
    Returns:
        dict: A dictionary containing:
            - video_url: Direct link to the YouTube video
            - embed_code: HTML iframe embed code for the video
            - thumbnails: Dictionary of different quality thumbnail URLs:
                - default: Default quality thumbnail
                - medium: Medium quality thumbnail
                - high: High quality thumbnail
                - maxres: Maximum resolution thumbnail
        Returns an error message if an error occurs
    """
    return get_thumbnail_and_links(video_id)
