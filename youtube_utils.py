from youtube_transcript_api import YouTubeTranscriptApi
from pytube import YouTube

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
    except Exception as e:
        return {"error": str(e)}