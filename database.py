from typing import Annotated
from fastapi import Depends
import os
from sqlmodel import create_engine, Session, SQLModel
from dotenv import load_dotenv

# loads the .env file
load_dotenv()

# Get the database URL from the environment variable
DATABASE_URL = os.getenv("DATABASE_URL")

# Create the database engine
engine = create_engine(DATABASE_URL)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

# The session dependency alias
# This is what we'll use to communicate with the DB in main.py routes
SessionDep = Annotated[Session, Depends(get_session)]
