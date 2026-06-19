import uuid
from locust import HttpUser, task, between

class BlogicumLoadTest(HttpUser):
    # Симулируем паузу реального пользователя (от 1 до 2 секунд между кликами)
    wait_time = between(1, 2)

    # 1. ЧТЕНИЕ: Получение ленты всех постов (самый частый запрос на сайте)
    @task(5)
    def get_all_posts(self):
        self.client.get("/api/v1/posts/")

    # 2. ЧТЕНИЕ: Получение одного конкретного поста
    # (Перед тестом создай хотя бы один пост в Swagger, чтобы ID 1 существовал!)
    @task(4)
    def get_one_post(self):
        self.client.get("/api/v1/posts/1")

    # 3. ЧТЕНИЕ: Получение списка категорий
    @task(3)
    def get_categories(self):
        self.client.get("/api/v1/categories/")

    # 4. ЗАПИСЬ: Создание нового поста (упрощенный вариант без файлов)
    @task(2)
    def create_post(self):
        form_data = {
            "title": "Тестовый пост locust",
            "text": "Проверяем скорость асинхронного fastAPI под нагрузкой",
            "category_id": 1,
            "is_published": True
        }
        # Убрали files=files, шлем чистую форму
        self.client.post("/api/v1/posts/", data=form_data)

    # 5. ЗАПИСЬ: Добавление комментария (тоже без файлов)
    @task(2)
    def create_comment(self):
        form_data = {
            "text": "Асинхронный комментарий под locust",
            "post_id": 1
        }
        # Шлем чистую форму
        self.client.post("/api/v1/comments/", data=form_data)

