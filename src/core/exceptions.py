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

class UnauthorizedException(PostAppException):
    def __init__(self, detail: str = "Не авторизован"):
        self.detail = detail
        self.status_code = 401