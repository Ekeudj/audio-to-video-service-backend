from fastapi import FastAPI, UploadFile, File, HTTPException
from database import engine, create_db_and_tables, SessionDep
from models import AudioProject
import shutil
import os

app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.get('/')
def root():
    return{"message":"We're live!!"}

#route for actual audio upload
@app.post('/upload')
async def upload_audio(session: SessionDep, file: UploadFile = File(...)):
    upload_dir = "uploads"
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)

    file_location = f"{upload_dir}/{file.filename}"
    with open(file_location, "wb+") as file_object:
        shutil.copyfileobj(file.file, file_object)

    new_project = AudioProject(title=file.filename, file_path=file_location)
    session.add(new_project)
    session.commit()
    session.refresh(new_project)
