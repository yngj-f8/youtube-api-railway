import os
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound, VideoUnavailable
from pytube import YouTube
from pytube.exceptions import VideoUnavailable as PytubeVideoUnavailable
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

def get_transcript(video_id: str):
    """
    Retrieves the transcript for a given YouTube video ID.
    
    Args:
        video_id (str): The YouTube video ID to fetch the transcript for
        
    Returns:
        dict: A dictionary containing either:
            - transcript: List of transcript entries with text and timing information
            - error: Error message if transcript is unavailable or an exception occurs
            
    Raises:
        TranscriptsDisabled: If the video has transcripts disabled
        NoTranscriptFound: If no transcript is available for the video
        VideoUnavailable: If the video is unavailable
    """
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        return {"transcript": transcript}
    except (TranscriptsDisabled, NoTranscriptFound, VideoUnavailable):
        return {"error": "Transcript is unavailable for this video."}
    except Exception as e:
        return {"error": f"Exception: {str(e)}"}

def get_video_info(video_id: str):
    """
    Retrieves basic information about a YouTube video using the YouTube Data API.
    
    Args:
        video_id (str): The YouTube video ID to fetch information for
        
    Returns:
        dict: A dictionary containing either:
            - title: Video title
            - author: Channel title of the video
            - publish_date: Video publish date in ISO 8601 format
            - thumbnail_url: High quality thumbnail URL of the video
            - error: Error message if:
                - API key is missing
                - Video is not found
                - An exception occurs during API call
    """
    try:
        api_key = os.getenv("YOUTUBE_API_KEY")
        if not api_key:
            return {"error": "Missing YOUTUBE_API_KEY"}

        youtube = build("youtube", "v3", developerKey=api_key)
        request = youtube.videos().list(
            part="snippet",
            id=video_id
        )
        response = request.execute()

        if not response["items"]:
            return {"error": "Video not found"}

        item = response["items"][0]
        snippet = item["snippet"]

        return {
            "title": snippet["title"],
            "author": snippet["channelTitle"],
            "publish_date": snippet["publishedAt"],
            "thumbnail_url": snippet["thumbnails"]["high"]["url"]
        }

    except Exception as e:
        return {"error": f"Exception: {str(e)}"}

def get_channel_info(channel_id: str):
    """
    Retrieves detailed information about a YouTube channel using the YouTube Data API.
    
    Args:
        channel_id (str): The YouTube channel ID to fetch information for
        
    Returns:
        dict: A dictionary containing either:
            - title: Channel title
            - description: Channel description
            - thumbnail_url: Channel thumbnail URL
            - subscriber_count: Number of subscribers
            - video_count: Total number of videos
            - error: Error message if channel is not found or an exception occurs
            
    Raises:
        HttpError: If there's an error with the YouTube API request
    """
    try:
        api_key = os.getenv("YOUTUBE_API_KEY")
        if not api_key:
            return {"error": "Missing YOUTUBE_API_KEY"}
        youtube = build("youtube", "v3", developerKey=api_key)
        request = youtube.channels().list(
            part="snippet,statistics",
            id=channel_id
        )
        response = request.execute()
        if not response["items"]:
            return {"error": "Channel not found"}

        item = response["items"][0]
        snippet = item["snippet"]
        stats = item["statistics"]

        return {
            "title": snippet["title"],
            "description": snippet["description"],
            "thumbnail_url": snippet["thumbnails"]["default"]["url"],
            "subscriber_count": stats.get("subscriberCount"),
            "video_count": stats.get("videoCount"),
        }
    except HttpError as e:
        return {"error": f"YouTube API error: {e.resp.status} {e._get_reason()}"}
    except Exception as e:
        return {"error": f"Exception: {str(e)}"}

def get_thumbnail_and_links(video_id: str):
    """
    Retrieves various YouTube video links and thumbnail URLs for a given video ID.
    
    Args:
        video_id (str): The YouTube video ID to fetch links and thumbnails for
        
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
    try:
        return {
            "video_url": f"https://www.youtube.com/watch?v={video_id}",
            "embed_code": f'<iframe width="560" height="315" src="https://www.youtube.com/embed/{video_id}" frameborder="0" allowfullscreen></iframe>',
            "thumbnails": {
                "default": f"https://img.youtube.com/vi/{video_id}/default.jpg",
                "medium": f"https://img.youtube.com/vi/{video_id}/mqdefault.jpg",
                "high": f"https://img.youtube.com/vi/{video_id}/hqdefault.jpg",
                "maxres": f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg"
            }
        }
    except Exception as e:
        return {"error": f"Exception: {str(e)}"}
    
def resolve_channel_id(video_id: str):
    """
    Retrieves the channel ID and title associated with a YouTube video.
    
    Args:
        video_id (str): The YouTube video ID to fetch channel information for
        
    Returns:
        dict: A dictionary containing either:
            - channel_id: The unique identifier of the channel that uploaded the video
            - channel_title: The name of the channel that uploaded the video
            - error: Error message if:
                - API key is missing
                - Video is not found
                - An exception occurs during API call
    """
    try:
        api_key = os.getenv("YOUTUBE_API_KEY")
        if not api_key:
            return {"error": "Missing YOUTUBE_API_KEY"}

        youtube = build("youtube", "v3", developerKey=api_key)
        request = youtube.videos().list(
            part="snippet",
            id=video_id
        )
        response = request.execute()

        if not response["items"]:
            return {"error": "Video not found"}

        snippet = response["items"][0]["snippet"]
        return {
            "channel_id": snippet["channelId"],
            "channel_title": snippet["channelTitle"]
        }

    except Exception as e:
        return {"error": f"Exception: {str(e)}"}

