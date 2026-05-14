class PostAppException(Exception):
    """Базовая ошибка приложения"""
    def __init__(self, message: str):
        self.message = message

class NotFoundException(PostAppException):
    """Объект не найден"""
    pass

class AlreadyExistsException(PostAppException):
    """Объект уже существует"""
    pass

class InfrastructureException(PostAppException):
    """Ошибка на уровне базы данных"""
    pass