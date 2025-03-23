import io
import zipfile
from dataclasses import dataclass

from app.domain.files.gateway import FilesGateway


@dataclass
class ProcessFilesOutputDTO:
    files: io.BytesIO


class ProcessFilesUseCase:
    def __init__(
            self,
            files_gateway: FilesGateway,
    ) -> None:
        self.files_gateway = files_gateway

    async def __call__(
            self
    ) -> ProcessFilesOutputDTO:
        files = self.files_gateway.get_files()

        # process files here

        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
            for file in files:
                zip_file.writestr(file.filename, file.data)

        zip_buffer.seek(0)

        return ProcessFilesOutputDTO(files=zip_buffer)
