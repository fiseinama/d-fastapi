from src.infrastructure.sqlite.repositories.comment import CommentRepository
from src.core.exceptions import AlreadyExistsException, NotFoundException
from src.schemas.comments import CommentCreate, CommentUpdate

class CommentUseCase:
    def __init__(self):
        self.repo = CommentRepository()

    def get_all(self):
        return self.repo.get_all()

    def create_comment(self, data: CommentCreate):
        try:
            return self.repo.create(data)
        except AlreadyExistsException as e:
            raise AlreadyExistsException(f"Не удалось опубликовать комментарий: {e.message}")

    def update_comment(self, comment_id: int, data: CommentUpdate):
        comment = self.repo.update(comment_id, data)
        if not comment:
            raise NotFoundException(f"Комментарий с ID {comment_id} не найден для обновления")
        return comment

    def delete_comment(self, comment_id: int):
        if not self.repo.delete(comment_id):
            raise NotFoundException(f"Комментарий с ID {comment_id} не найден")
        return True