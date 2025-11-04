from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String
from typing import TYPE_CHECKING
from ..db import db

if TYPE_CHECKING:
    from .task import Task
class Goal(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(255))
    tasks: Mapped[list["Task"]] = relationship(back_populates="goal")

    def to_dict(self, include_tasks=False):
        goal_as_dict ={
            "id": self.id,
            "title": self.title,
        }

        if include_tasks:
            goal_as_dict["tasks"] = [task.to_dict() for task in self.tasks]

        return goal_as_dict

    @classmethod
    def from_dict(cls, goal_dict):
        return cls(
            title=goal_dict["title"]
        )