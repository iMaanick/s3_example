from dishka import Provider, provide, Scope

from app.application.models.config import MinioSettings
from app.application.use_cases.process_files import ProcessFilesUseCase
from app.domain.files.gateway import FilesGateway
from app.infrastructure.minio.gateway import MinioGateway


class InfraProvider(Provider):
    @provide(scope=Scope.APP)
    def get_minio_config(self) -> MinioSettings:
        return MinioSettings()
    minio = provide(MinioGateway, provides=FilesGateway, scope=Scope.APP)

class UseCaseProvider(Provider):
    process_files = provide(ProcessFilesUseCase, scope=Scope.REQUEST)
