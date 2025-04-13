import os
from youtube_transcript_api import YouTubeTranscriptApi
from pytube import YouTube
from googleapiclient.discovery import build

def get_transcript(video_id: str):
    """
    Retrieves the transcript for a given YouTube video ID.
    
    Args:
        video_id (str): The YouTube video ID to fetch the transcript for
        
    Returns:
        dict: A dictionary containing either the transcript data or an error message
    """
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        return {"transcript": transcript}
    except Exception as e:
        return {"error": str(e)}

def get_video_info(video_id: str):
    """
    Retrieves basic information about a YouTube video.
    
    Args:
        video_id (str): The YouTube video ID to fetch information for
        
    Returns:
        dict: A dictionary containing video details (title, author, publish date, thumbnail URL) or an error message
    """
    try:
        yt = YouTube(f"https://www.youtube.com/watch?v={video_id}")
        return {
            "title": yt.title,
            "author": yt.author,
            "publish_date": str(yt.publish_date),
            "thumbnail_url": yt.thumbnail_url
        }
    
    except VideoUnavailable:
        return {"error": "Video is unavailable or has been removed."}
    
    except Exception as e:
        return {"error": str(e)}
    
def get_channel_info(channel_id: str):
    """
    Retrieves detailed information about a YouTube channel using the YouTube Data API.
    
    Args:
        channel_id (str): The YouTube channel ID to fetch information for
        
    Returns:
        dict: A dictionary containing channel details including:
            - title: Channel title
            - description: Channel description
            - thumbnail_url: Channel thumbnail URL
            - subscriber_count: Number of subscribers
            - video_count: Total number of videos
        Returns an error message if the channel is not found or if an error occurs
    """
    try:
        api_key = os.getenv("YOUTUBE_API_KEY")
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

    except Exception as e:
        return {"error": str(e)}
    
def get_thumbnail_and_links(video_id: str):
    """
    Retrieves various YouTube video links and thumbnail URLs for a given video ID.
    
    Args:
        video_id (str): The YouTube video ID to fetch links and thumbnails for
        
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
        return {"error": str(e)}
