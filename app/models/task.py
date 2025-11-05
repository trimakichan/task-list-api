from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey
from datetime import datetime
from typing import Optional, TYPE_CHECKING
from ..db import db

if TYPE_CHECKING:
    from .goal import Goal
class Task(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]= mapped_column(String(255))
    description: Mapped[str] 
    completed_at: Mapped[Optional[datetime]] 
    goal_id: Mapped[Optional[int]] = mapped_column(ForeignKey("goal.id"))
    goal: Mapped[Optional["Goal"]] = relationship(back_populates="tasks")

    def to_dict(self):
        task_as_dict = {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "is_complete": True if self.completed_at else False
        }

        if self.goal_id:
            task_as_dict["goal_id"] = self.goal_id
        
        return task_as_dict
    
    @classmethod
    def from_dict(cls,task_dict):
        return cls(   
            title=task_dict["title"],
            description=task_dict["description"],
            )
