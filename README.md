# YouTube API Server · FastAPI + Railway

A lightweight, production-ready RESTful API to extract YouTube video data: transcripts, metadata, channel info, thumbnails, and more.  
Ideal for content automation, research pipelines, or custom media tools.

---

## 🌐 Live Deployment

> `https://your-project.up.railway.app`  
(deployed via [Railway](https://railway.app))

---

## 🔐 Authentication

All endpoints require an API key via header:

x-api-key: your-secret-key


---

## ✅ Available Endpoints

| Endpoint                 | Params                | Description                                      |
|--------------------------|-----------------------|--------------------------------------------------|
| `/transcript`            | `video_id`            | Fetch subtitles using `youtube-transcript-api`  |
| `/video_info`            | `video_id`            | Retrieve title, author, publish date, thumbnail |
| `/channel_info`          | `channel_id`          | Get channel name, subscriber count, description |
| `/thumbnail_link`        | `video_id`            | Return multiple thumbnail URLs + embed iframe   |
| `/resolve_channel_id`    | `video_id`            | Resolve the `channel_id` from a video ID        |

---

## 📦 Quick Example (curl)

```bash
curl -X GET "https://your-project.up.railway.app/video_info?video_id=dQw4w9WgXcQ" \
     -H "x-api-key: your-secret-key"
🛠️ Local Development Setup

# 1. Install Python dependencies
pip install -r requirements.txt

# 2. Set up local environment
echo "API_KEY=your-secret-key" > .env
echo "YOUTUBE_API_KEY=your-google-api-key" >> .env

# 3. Run the FastAPI server
uvicorn main:app --reload
📁 Project Structure

.
├── main.py            # FastAPI entry point
├── youtube_utils.py   # All API logic (YouTube data handling)
├── auth.py            # Header-based API key middleware
├── requirements.txt   # Python dependencies
├── Procfile           # Railway deployment instruction
└── .env               # Local environment variables
📘 Tech Stack

FastAPI – for blazing-fast REST API
Railway – instant cloud deployment
YouTube APIs:
youtube-transcript-api (captions)
google-api-python-client (official YouTube data)
📄 License

MIT License © 2025

🧪 Coming Soon (optional)

 Search by keyword or channel name
 Bulk transcript downloader
 n8n-ready webhook API for automation