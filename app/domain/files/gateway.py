from abc import ABC, abstractmethod

from app.domain.files.entities import StoredFile


class FilesGateway(ABC):
    @abstractmethod
    def get_files(self, ) -> list[StoredFile]:
        raise NotImplementedError
