from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import FileResponse
from TTS.api import TTS
import uuid
import os

app = FastAPI()
tts_model = TTS(model_name="tts_models/multilingual/multi-dataset/xtts_v1", progress_bar=False)

class TTSRequest(BaseModel):
    text: str
    lang: str

@app.post("/speak")
def speak(data: TTSRequest):
    try:
        os.makedirs("audio", exist_ok=True)
        filename = f"{uuid.uuid4().hex}.wav"
        path = os.path.join("audio", filename)
        tts_model.tts_to_file(text=data.text, file_path=path)
        return FileResponse(path, media_type="audio/wav")
    except Exception as e:
        return {"error": str(e)}
