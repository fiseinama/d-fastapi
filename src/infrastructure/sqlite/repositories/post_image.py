from typing import List

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.exceptions import InfrastructureException
from src.infrastructure.sqlite.models.post_image import PostImage


class PostImageRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_post_id(self, post_id: int) -> List[PostImage]:
        try:
            result = await self.session.execute(
                select(PostImage).where(PostImage.post_id == post_id)
            )
            return list(result.scalars().all())
        except SQLAlchemyError as e:
            raise InfrastructureException(f"Ошибка при получении изображений поста: {str(e)}")

    async def create_many(self, post_id: int, image_paths: List[str]) -> List[PostImage]:
        try:
            images = [
                PostImage(post_id=post_id, image_path=path)
                for path in image_paths
            ]
            self.session.add_all(images)
            await self.session.flush()
            for image in images:
                await self.session.refresh(image)
            return images
        except SQLAlchemyError as e:
            raise InfrastructureException(f"Ошибка при сохранении изображений: {str(e)}")
