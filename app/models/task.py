from datetime import datetime
from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Text, DateTime
from ..db import db

class Task(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]= mapped_column(String(255))
    description: Mapped[str] = mapped_column(Text)
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    # Consider moving these methods into Base class after wave 3
    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "is_complete": self.completed_at is not None
        }
    
    @classmethod
    def from_dict(cls,task_dict):
        title = task_dict["title"]
        description = task_dict["description"]
        
        return cls(   
            title=title,
            description=description,
            )
        
