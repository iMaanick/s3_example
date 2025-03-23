from abc import ABC, abstractmethod


class FileInfoGateway(ABC):
    @abstractmethod
    async def add_file_info(self, file_name: str) -> None:
        raise NotImplementedError
