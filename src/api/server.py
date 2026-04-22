from fastapi import FastAPI, Request, Response
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import cv2
import json
from src.database.db_manager import DBManager, Person, Profile, Transcript

app = FastAPI(title="ARGOS Dashboard")
db = DBManager()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Global engine reference (will be set from main)
engine = None

@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/api/people")
async def get_people():
    session = db.get_session()
    try:
        people = session.query(Person).all()
        return [
            {
                "id": p.id,
                "name": p.full_name or p.alias,
                "created_at": p.created_at.isoformat()
            } for p in people
        ]
    finally:
        session.close()

@app.get("/api/person/{person_id}")
async def get_person_details(person_id: int):
    session = db.get_session()
    try:
        person = session.query(Person).filter_by(id=person_id).first()
        if not person:
            return {"error": "Not found"}
        
        profiles = {pr.category: pr.content for pr in person.profiles}
        transcripts = [
            {"text": t.text, "timestamp": t.timestamp.isoformat()} 
            for t in person.transcripts[-10:] # Last 10
        ]
        
        return {
            "id": person.id,
            "name": person.full_name or person.alias,
            "profile": profiles,
            "transcripts": transcripts
        }
    finally:
        session.close()

def gen_frames():
    cap = cv2.VideoCapture(0)
    while True:
        success, frame = cap.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.get("/video_feed")
async def video_feed():
    return StreamingResponse(gen_frames(),
                            media_type='multipart/x-mixed-replace; boundary=frame')
