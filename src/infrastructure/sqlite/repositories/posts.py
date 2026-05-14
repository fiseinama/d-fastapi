from typing import List, Optional
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from src.infrastructure.sqlite.database import get_session
from src.infrastructure.sqlite.models.posts import Post
from src.schemas.posts import PostCreate, PostUpdate
from src.core.exceptions import AlreadyExistsException, InfrastructureException

class PostRepository:
    def get_all(self) -> List[Post]:
        try:
            with get_session() as session:
                return session.query(Post).all()
        except SQLAlchemyError as e:
            raise InfrastructureException(f"Ошибка при получении постов: {str(e)}")

    def get_by_id(self, post_id: int) -> Optional[Post]:
        try:
            with get_session() as session:
                return session.query(Post).filter(Post.id == post_id).first()
        except SQLAlchemyError as e:
            raise InfrastructureException(f"Ошибка при получении поста: {str(e)}")

    def create(self, data: PostCreate) -> Post:
        try:
            with get_session() as session:
                post = Post(**data.model_dump())
                session.add(post)
                session.commit()
                session.refresh(post)
                return post
        except IntegrityError as e:
            raise AlreadyExistsException(f"Пост с таким slug или данными уже существует: {str(e.orig)}")
        except SQLAlchemyError as e:
            raise InfrastructureException(f"Ошибка при создании поста: {str(e)}")

    def update(self, post_id: int, data: PostUpdate) -> Optional[Post]:
        try:
            with get_session() as session:
                post = session.query(Post).filter(Post.id == post_id).first()
                if not post:
                    return None
                for key, value in data.model_dump(exclude_unset=True).items():
                    setattr(post, key, value)
                session.commit()
                session.refresh(post)
                return post
        except IntegrityError as e:
            raise AlreadyExistsException(f"Конфликт данных при обновлении поста: {str(e.orig)}")
        except SQLAlchemyError as e:
            raise InfrastructureException(f"Ошибка при обновлении поста: {str(e)}")

    def delete(self, post_id: int) -> bool:
        try:
            with get_session() as session:
                post = session.query(Post).filter(Post.id == post_id).first()
                if not post:
                    return False
                session.delete(post)
                session.commit()
                return True
        except SQLAlchemyError as e:
            raise InfrastructureException(f"Ошибка при удалении поста: {str(e)}")