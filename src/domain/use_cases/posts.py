from src.infrastructure.sqlite.repositories.posts import PostRepository
from src.core.exceptions import AlreadyExistsException, NotFoundException
from src.schemas.posts import PostCreate, PostUpdate

class PostUseCase:
    def __init__(self):
        self.repo = PostRepository()

    def get_all(self):
        return self.repo.get_all()

    def get_by_id(self, post_id: int):
        post = self.repo.get_by_id(post_id)
        if not post:
            raise NotFoundException(f"Пост с ID {post_id} не найден")
        return post

    def create_post(self, data: PostCreate, author_id: int):
        try:
            updated_data = data.model_dump()
            updated_data["author_id"] = author_id
            secure_post_data = PostCreate(**updated_data)
            return self.repo.create(secure_post_data)

        except AlreadyExistsException as e:
            raise AlreadyExistsException(f"Не удалось создать пост '{data.title}': {e.message}")

    def update_post(self, post_id: int, data: PostUpdate, user_id: int):
        post = self.repo.get_by_id(post_id)
        if not post:
            raise NotFoundException(f"Пост с ID {post_id} не найден")

        if post.author_id != user_id:
            from fastapi import HTTPException, status
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Вы не можете редактировать чужой пост!"
            )
        return self.repo.update(post_id, data)

    def delete_post(self, post_id: int, user_id: int):
        post = self.repo.get_by_id(post_id)
        if not post:
            raise NotFoundException(f"Пост с ID {post_id} не найден")
        if post.author_id != user_id:
            from fastapi import HTTPException, status
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Вы не можете удалить чужой пост!"
            )
        self.repo.delete(post_id)
        return True