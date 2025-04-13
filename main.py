from fastapi import FastAPI, Query
from auth import AuthMiddleware
from youtube_utils import get_transcript
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()
app.add_middleware(AuthMiddleware)

@app.get("/transcript")
def transcript(video_id: str = Query(...)):
    return get_transcript(video_id)

