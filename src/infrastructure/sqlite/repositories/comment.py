from typing import List, Optional
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from src.infrastructure.sqlite.database import get_session
from src.infrastructure.sqlite.models.comment import Comment
from src.schemas.comments import CommentCreate, CommentUpdate
from src.core.exceptions import AlreadyExistsException, InfrastructureException

class CommentRepository:

    def get_all(self) -> List[Comment]:
        try:
            with get_session() as session:
                return session.query(Comment).all()
        except SQLAlchemyError as e:
            raise InfrastructureException(f"Ошибка при получении комментариев: {str(e)}")

    def get_by_id(self, id: int) -> Optional[Comment]:
        try:
            with get_session() as session:
                return session.query(Comment).filter(Comment.id == id).first()
        except SQLAlchemyError as e:
            raise InfrastructureException(f"Ошибка при получении комментария: {str(e)}")

    def create(self, data: CommentCreate) -> Comment:
        try:
            with get_session() as session:
                comment = Comment(**data.model_dump())
                session.add(comment)
                session.commit()
                session.refresh(comment)
                session.expunge(comment)
                return comment
        except IntegrityError as e:
            raise AlreadyExistsException(f"Комментарий уже существует или нарушены связи: {str(e.orig)}")
        except SQLAlchemyError as e:
            raise InfrastructureException(f"Ошибка при создании комментария: {str(e)}")

    def update(self, id: int, data: CommentUpdate) -> Optional[Comment]:
        try:
            with get_session() as session:
                comment = session.query(Comment).filter(Comment.id == id).first()
                if not comment:
                    return None
                for key, value in data.model_dump(exclude_unset=True).items():
                    setattr(comment, key, value)
                session.commit()
                session.refresh(comment)
                session.expunge(comment)
                return comment
        except IntegrityError as e:
            raise AlreadyExistsException(f"Ошибка обновления: данные конфликтуют: {str(e.orig)}")
        except SQLAlchemyError as e:
            raise InfrastructureException(f"Ошибка комментария: {str(e)}")

    def delete(self, id: int) -> bool:
        try:
            with get_session() as session:
                comment = session.query(Comment).filter(Comment.id == id).first()
                if not comment:
                    return False
                session.delete(comment)
                session.commit()
                return True
        except SQLAlchemyError as e:
            raise InfrastructureException(f"Ошибка при удалении комментария: {str(e)}")