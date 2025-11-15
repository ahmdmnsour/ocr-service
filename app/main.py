from fastapi import FastAPI, UploadFile, File
import tempfile, os
from utils import process_file

app = FastAPI()

@app.post("/files")
async def upload_file(file: UploadFile = File(...)):
    suffix = os.path.splitext(file.filename)[1].lower()
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name
    
    text = process_file(tmp_path)
    os.remove(tmp_path)
    return {"text": text}