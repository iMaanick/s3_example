from abc import ABC, abstractmethod

from app.domain.files_gateway.entities import StoredFile


class FilesGateway(ABC):
    @abstractmethod
    async def get_files(self, ) -> list[StoredFile]:
        raise NotImplementedError
