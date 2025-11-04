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

    # Consider moving these methods into Base class after wave 3
    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "is_complete": True if self.completed_at else False
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