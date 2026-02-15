from services.audio import transcribe_audio
from fastapi import FastAPI, UploadFile, File, HTTPException, BackgroundTasks
from database import engine, create_db_and_tables, SessionDep
from models import AudioProject
import shutil
import os
from sqlmodel import create_engine, Session, SQLModel

app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.get('/')
def root():
    return{"message":"We're live!!"}

# @app.post tells FastAPI this is a "Sending" route (User -> Server)
# '/upload' is the URL address where the user sends the file
@app.post('/upload')
async def upload_audio(
    # background_tasks lets us finish the upload but keep working in secret
    background_tasks: BackgroundTasks,
    # session is our "phone line" to talk to the Supabase database
    session: SessionDep,
    # UploadFile is a special FastAPI container for the audio data
    file: UploadFile = File(...)
    ):
    
    # 1. Prepare the folder on your PC
    upload_dir = "uploads"
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir) # Creates the folder if you don't have it

    # 2. Create the full path (e.g., "uploads/my_voice.mp3")
    file_location = f"{upload_dir}/{file.filename}"

    # 3. Save the actual "Binary" data of the audio to your hard drive
    # "wb+" = Write Binary mode (needed for audio, not just text)
    with open(file_location, "wb+") as file_object:
        # Shutil streams the data so your RAM doesn't get full
        shutil.copyfileobj(file.file, file_object)

    # 4. Tell Supabase: "I have a new project!"
    # We use the filename as the title for now
    new_project = AudioProject(title=file.filename, file_path=file_location)
    session.add(new_project) # Put it in the "To-Do" list for the DB
    session.commit()         # Actually push it to the cloud
    session.refresh(new_project) # Get the unique ID Supabase just gave it

    # 5. TRIGGER THE SECRET WORKER
    # We tell FastAPI: "Go run the transcription function while I talk to the user"
    background_tasks.add_task(run_transcription_pipeline, new_project.id, file_location)

    # 6. Give the user an instant "High-Five" so they aren't waiting
    return {"message": "Uploaded successful! Transcription started.", "project_id": new_project.id}



# This runs "off-screen". The user doesn't see this happening.
def run_transcription_pipeline(project_id: int, file_path: str):
    
    # Step 1: Open a fresh connection to the database
    # (Since this is a separate task, it needs its own connection)
    with Session(engine) as session:
        
        # Step 2: Send the file to Groq (The AI)
        # This is where the audio turns into text
        text = transcribe_audio(file_path)

        # Step 3: Find that specific project in Supabase using the ID
        project = session.get(AudioProject, project_id)
        
        # Step 4: If we found it, update the info!
        if project:
            project.transcription = text # Fill in the empty transcription column
            project.status = "Transcribed" # Change status from "uploaded" to "Transcribed"
            
            session.add(project) # Prepare the update
            session.commit()     # Save the words to Supabase forever
