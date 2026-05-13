from typing import List, Optional
from src.infrastructure.sqlite.database import get_session
from src.infrastructure.sqlite.models.posts import Post
from src.schemas.posts import PostCreate, PostUpdate

class PostRepository:
    def get_all(self) -> List[Post]:
        with get_session() as session:
            return session.query(Post).all()

    def get_by_id(self, post_id: int) -> Optional[Post]:
        with get_session() as session:
            return session.query(Post).filter(Post.id == post_id).first()

    def create(self, data: PostCreate) -> Post:
        with get_session() as session:
            post = Post(**data.model_dump())
            session.add(post)
            return post

    def update(self, post_id: int, data: PostUpdate) -> Optional[Post]:
        with get_session() as session:
            post = session.query(Post).filter(Post.id == post_id).first()
            if not post: return None
            for key, value in data.model_dump(exclude_unset=True).items():
                setattr(post, key, value)
            return post

    def delete(self, post_id: int) -> bool:
        with get_session() as session:
            post = session.query(Post).filter(Post.id == post_id).first()
            if not post:
                return False
            session.delete(post)
            session.commit()
            return True