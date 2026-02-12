from fastapi import FastAPI
from database import engine, create_db_and_tables, SessionDep
from models import AudioProject

app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.get('/')
def root():
    return{"message":"We're live!!"}

#temporary test to make sure supabase is receving
@app.post('/test_db')
def test_db(project_title: str,session:SessionDep):
    new_project = AudioProject(title=project_title)
    session.add(new_project)
    session.commit()
    session.refresh(new_project)
    return {"message": f"Project '{new_project.title}' created with ID {new_project.id}."}