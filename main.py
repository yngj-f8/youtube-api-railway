from fastapi import FastAPI, Query
from dotenv import load_dotenv
from auth import AuthMiddleware
from youtube_utils import (
    get_transcript,
    get_video_info,
    get_channel_info,
    get_thumbnail_and_links,
)

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
        dict: A dictionary containing either:
            - transcript: List of transcript entries with text and timing information
            - error: Error message if transcript is unavailable or an exception occurs
    """
    return get_transcript(video_id)

@app.get("/video_info")
def video_info(video_id: str = Query(...)):
    """
    Endpoint to retrieve YouTube video information.
    
    Args:
        video_id (str): YouTube video ID
        
    Returns:
        dict: A dictionary containing either:
            - title: Video title
            - author: Video author/channel name
            - publish_date: Video publish date
            - thumbnail_url: Video thumbnail URL
            - error: Error message if video is unavailable or an exception occurs
    """
    return get_video_info(video_id)

@app.get("/channel_info")
def channel_info(channel_id: str = Query(...)):
    """
    Endpoint to retrieve YouTube channel information.
    
    Args:
        channel_id (str): YouTube channel ID
        
    Returns:
        dict: A dictionary containing either:
            - title: Channel title
            - description: Channel description
            - thumbnail_url: Channel thumbnail URL
            - subscriber_count: Number of subscribers
            - video_count: Total number of videos
            - error: Error message if channel is not found or an exception occurs
    """
    return get_channel_info(channel_id)

@app.get("/thumbnail_link")
def thumbnail_link(video_id: str = Query(...)):
    """
    Endpoint to retrieve YouTube video links and thumbnail URLs.
    
    Args:
        video_id (str): YouTube video ID
        
    Returns:
        dict: A dictionary containing either:
            - video_url: Direct link to the YouTube video
            - embed_code: HTML iframe embed code for the video
            - thumbnails: Dictionary of different quality thumbnail URLs
                - default: Default quality thumbnail
                - medium: Medium quality thumbnail
                - high: High quality thumbnail
                - maxres: Maximum resolution thumbnail
            - error: Error message if an exception occurs
    """
    return get_thumbnail_and_links(video_id)

@app.get("/resolve_channel_id")
def resolve_channel_id_route(video_id: str):
    """
    Endpoint to retrieve the channel ID and title associated with a YouTube video.
    
    Args:
        video_id (str): YouTube video ID
        
    Returns:
        dict: A dictionary containing either:
            - channel_id: The unique identifier of the channel that uploaded the video
            - channel_title: The name of the channel that uploaded the video
            - error: Error message if:
                - API key is missing
                - Video is not found
                - An exception occurs during API call
    """
    from youtube_utils import resolve_channel_id
    return resolve_channel_id(video_id)