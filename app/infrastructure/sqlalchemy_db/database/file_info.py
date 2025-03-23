from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.file_info.gateway import FileInfoGateway
from app.infrastructure.sqlalchemy_db.models import FileInfoORM


class FileInfoSqlGateway(FileInfoGateway):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def add_file_info(self, file_name: str) -> None:
        stmt = insert(FileInfoORM).values(file_name=file_name)

        await self.session.execute(stmt)
