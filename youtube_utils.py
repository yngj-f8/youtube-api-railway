import os
import requests
from requests.adapters import HTTPAdapter, Retry
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound, VideoUnavailable
from youtube_transcript_api import _api
from pytube import YouTube
from pytube.exceptions import VideoUnavailable as PytubeVideoUnavailable
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# =============================
# 1. Global Proxy + Retry + Timeout Setup
# =============================

# Define proxy server with authentication
proxies = {
    "http": "http://fuser:fpass@118.216.66.169:8888",
    "https": "http://fuser:fpass@118.216.66.169:8888",
}

# Create a session for proxy requests
session = requests.Session()
session.proxies.update(proxies)

# Configure retry strategy for transient errors
retries = Retry(
    total=3,  # Maximum retry attempts
    backoff_factor=1,  # Exponential backoff factor
    status_forcelist=[429, 500, 502, 503, 504],  # HTTP statuses that trigger a retry
    allowed_methods=["GET", "POST"],  # Retry on GET and POST
)

# Mount the retry logic to HTTP and HTTPS adapters
adapter = HTTPAdapter(max_retries=retries)
session.mount("http://", adapter)
session.mount("https://", adapter)

# Patch YouTubeTranscriptApi's internal session to use the configured proxy session
_api._session = session

# =============================
# 2. API Functions
# =============================

def get_transcript(video_id: str):
    """
    Retrieves the transcript for a given YouTube video ID.
    All requests will use the global proxy session.
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
    This function does not use proxy since Google API client has its own request handling.
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
    Retrieves multiple thumbnail URLs and video links for a given YouTube video ID.
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
    Retrieves the channel ID and channel title for a given YouTube video.
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
