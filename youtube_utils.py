import os
import requests
from requests.adapters import HTTPAdapter, Retry

from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound, VideoUnavailable
from youtube_transcript_api._api import TranscriptListFetcher
from pytube import YouTube
from pytube.exceptions import VideoUnavailable as PytubeVideoUnavailable
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Proxy 설정
proxies = {
    "http": "http://fuser:fpass@118.216.66.169:8888",
    "https": "http://fuser:fpass@118.216.66.169:8888",
}

# Custom Proxy Fetcher with timeout + retry
class ProxyTranscriptListFetcher(TranscriptListFetcher):
    def __init__(self):
        super().__init__()

        # Apply proxy settings
        self._session.proxies.update(proxies)

        # Set timeout for all requests
        self._timeout = 10  # 10 seconds

        # Configure retry strategy
        retries = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["GET", "POST"]
        )
        adapter = HTTPAdapter(max_retries=retries)
        self._session.mount("http://", adapter)
        self._session.mount("https://", adapter)

# Override YouTubeTranscriptApi Fetcher
YouTubeTranscriptApi._TranscriptListFetcher = ProxyTranscriptListFetcher

def get_transcript(video_id: str):
    """
    Retrieves the transcript for a given YouTube video ID using proxy, timeout, and retry settings.
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

