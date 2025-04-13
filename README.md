# YouTube API Server (FastAPI + Railway)

A lightweight and secure RESTful API server for extracting YouTube video data including transcripts, metadata, channel info, thumbnails, and channel ID resolution.

## 🌐 Live API
Deploying via [Railway](https://railway.app)

> Example base URL: `https://your-project.up.railway.app`

## 🔐 Authentication
All endpoints require an API key header:

x-api-key: your-secret-key


---

## ✅ Features

| Endpoint               | Description                                               |
|------------------------|-----------------------------------------------------------|
| `/transcript`          | Get video transcripts by `video_id`                      |
| `/video_info`          | Get metadata like title, author, publish date            |
| `/channel_info`        | Retrieve channel name, subscribers, and more by `channel_id` |
| `/thumbnail_link`      | Generate thumbnail & embed links from video URL          |
| `/resolve_channel_id`  | Resolve the channel ID and name from a given `video_id`  |

---

## 🚀 Tech Stack

- **Framework**: FastAPI
- **Deployment**: Railway
- **YouTube Data**:
  - `youtube-transcript-api` (captions)
  - `google-api-python-client` (metadata, channel info, video resolution)

---

## 📦 Example Usage

```bash
# 1. Get Transcript
curl -X GET "https://your-project.up.railway.app/transcript?video_id=dQw4w9WgXcQ" \
     -H "x-api-key: your-secret-key"

# 2. Get Video Info
curl -X GET "https://your-project.up.railway.app/video_info?video_id=dQw4w9WgXcQ" \
     -H "x-api-key: your-secret-key"

# 3. Get Channel Info
curl -X GET "https://your-project.up.railway.app/channel_info?channel_id=UC_x5XG1OV2P6uZZ5FSM9Ttw" \
     -H "x-api-key: your-secret-key"

# 4. Get Thumbnail + Embed Links
curl -X GET "https://your-project.up.railway.app/thumbnail_link?video_id=dQw4w9WgXcQ" \
     -H "x-api-key: your-secret-key"

# 5. Resolve Channel ID from Video ID
curl -X GET "https://your-project.up.railway.app/resolve_channel_id?video_id=dQw4w9WgXcQ" \
     -H "x-api-key: your-secret-key"
🛠️ Local Development

# 1. Install dependencies
pip install -r requirements.txt

# 2. Set environment variables
echo "API_KEY=your-secret-key" > .env
echo "YOUTUBE_API_KEY=your-google-api-key" >> .env

# 3. Run locally
uvicorn main:app --reload
📁 Project Structure

.
├── main.py            # API entry point
├── youtube_utils.py   # YouTube-related logic
├── auth.py            # API key middleware
├── requirements.txt   # Dependencies
├── Procfile           # For Railway deployment
└── .env               # Environment variables (not committed)
📄 License

MIT License © 2025