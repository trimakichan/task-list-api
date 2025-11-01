from datetime import datetime
from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Text, DateTime
from ..db import db

class Task(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]= mapped_column(String(255))
    description: Mapped[str] 
    completed_at: Mapped[Optional[datetime]] 

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
        return cls(   
            title=task_dict["title"],
            description=task_dict["description"],
            )
    
    @classmethod
    def sort_by_title(cls, query, sort_param):
        if sort_param == 'asc':
            return query.order_by(cls.title)
        elif sort_param == 'desc':
            return query.order_by(cls.title.desc())

        return query
    


        
