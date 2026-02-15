from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class AudioProject(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    # uploaded, cleaning, transcribing, completed we'll also use it for tarcking later on
    file_path: Optional[str] = None
    # Where we store the text groq sends back!!
    transcription: Optional[str] = None

    status: str = Field(default="uploaded") 
    created_at: datetime = Field(default_factory=datetime.utcnow)