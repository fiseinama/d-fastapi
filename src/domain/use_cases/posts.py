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

    def create_post(self, data: PostCreate):
        try:
            return self.repo.create(data)
        except AlreadyExistsException as e:
            raise AlreadyExistsException(f"Не удалось создать пост '{data.title}': {e.message}")

    def update_post(self, post_id: int, data: PostUpdate):
        post = self.repo.update(post_id, data)
        if not post:
            raise NotFoundException(f"Пост с ID {post_id} не найден для обновления")
        return post

    def delete_post(self, post_id: int):
        if not self.repo.delete(post_id):
            raise NotFoundException(f"Пост с ID {post_id} не найден для удаления")
        return True