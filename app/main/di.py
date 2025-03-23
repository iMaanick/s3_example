from typing import AsyncIterable

from dishka import Provider, provide, Scope
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine, async_sessionmaker, AsyncSession

from app.application.models.config import MinioSettings, DatabaseSettings
from app.application.use_cases.process_files import ProcessFilesUseCase
from app.domain.file_info.gateway import FileInfoGateway
from app.domain.files.gateway import FilesGateway
from app.infrastructure.minio.gateway import MinioGateway
from app.infrastructure.sqlalchemy_db.database.file_info import FileInfoSqlGateway


class InfraProvider(Provider):
    @provide(scope=Scope.APP)
    def get_minio_config(self) -> MinioSettings:
        return MinioSettings()

    @provide(scope=Scope.APP)
    async def sqlite_engine(self) -> AsyncIterable[AsyncEngine]:
        db_uri = DatabaseSettings().database_uri
        engine = create_async_engine(db_uri, echo=True)
        try:
            yield engine
        finally:
            await engine.dispose()

    @provide(scope=Scope.APP)
    async def sessionmaker(self, engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
        return async_sessionmaker(
            bind=engine,
            class_=AsyncSession,
            expire_on_commit=False,
            autoflush=False,
            autocommit=False
        )

    @provide(scope=Scope.REQUEST)
    async def session(self, sessionmaker: async_sessionmaker[AsyncSession]) -> AsyncIterable[AsyncSession]:
        async with sessionmaker() as session:
            yield session

    minio = provide(MinioGateway, provides=FilesGateway, scope=Scope.APP)
    files_info = provide(FileInfoSqlGateway, provides=FileInfoGateway, scope=Scope.REQUEST)


class UseCaseProvider(Provider):
    process_files = provide(ProcessFilesUseCase, scope=Scope.REQUEST)
