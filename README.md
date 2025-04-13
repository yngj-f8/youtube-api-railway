# YouTube API Server (FastAPI + Railway)

A lightweight and secure RESTful API server for extracting YouTube video data including transcripts, metadata, channel info, and thumbnails.

## 🌐 Live API
Deploying via [Railway](https://railway.app)

> Example base URL: `https://your-project.up.railway.app`

## 🔐 Authentication
All endpoints require an API key header:

x-api-key: your-secret-key


---

## ✅ Features

| Endpoint | Description |
|----------|-------------|
| `/transcript` | Get video transcripts by `video_id` |
| `/video_info` | Get metadata like title, author, publish date |
| `/channel_info` | Retrieve channel name, subscribers, and more |
| `/thumbnail_link` | Generate thumbnail & embed links from video URL |

---

## 🚀 Tech Stack

- **Framework**: FastAPI
- **Deployment**: Railway
- **YouTube Data**:
  - `youtube-transcript-api` (captions)
  - `pytube` (basic metadata)
  - `google-api-python-client` (channel info)

---

## 📦 Example Usage

```bash
curl -X GET "https://your-project.up.railway.app/transcript?video_id=dQw4w9WgXcQ" \
     -H "x-api-key: your-secret-key"
🛠️ Local Development

# 1. Install dependencies
pip install -r requirements.txt

# 2. Set environment variable
echo "API_KEY=your-secret-key" > .env

# 3. Run locally
uvicorn main:app --reload
📁 Project Structure

.
├── main.py            # API entry point
├── youtube_utils.py   # YouTube-related logic
├── auth.py            # API key middleware
├── requirements.txt   # Dependencies
├── Procfile           # For Railway deployment
└── .env               # Environment variable (API key)
📄 License

MIT License © 2025
