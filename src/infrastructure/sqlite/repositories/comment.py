from typing import List, Optional
from src.infrastructure.sqlite.database import get_session
from src.infrastructure.sqlite.models.comment import Comment
from src.schemas.comments import CommentCreate, CommentUpdate, CommentOut


class CommentRepository:

    def get_all(self) -> List[Comment]:
        with get_session() as session:
            return session.query(Comment).all()

    def get_by_id(self, id: int) -> Optional[Comment]:
        with get_session() as session:
            return session.query(Comment).filter(Comment.id == id).first()

    def create(self, data: CommentCreate) -> Comment:
        with get_session() as session:
            comment = Comment(**data.model_dump())
            session.add(comment)
            session.commit()
            session.refresh(comment)
            return comment

    def update(self, id: int, data: CommentUpdate) -> Optional[Comment]:
        with get_session() as session:
            comment = self.get_by_id(id)
            if not comment:
                return None
            for key, value in data.model_dump(exclude_unset=True).items():
                setattr(comment, key, value)
            session.commit()
            session.refresh(comment)
            return comment

    def delete(self, id: int) -> bool:
        with get_session() as session:
            comment = self.get_by_id(id)
            if not comment:
                return False
            session.delete(comment)
            session.commit()
            return True