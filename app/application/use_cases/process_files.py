import io
import zipfile
from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.file_info.gateway import FileInfoGateway
from app.domain.files.gateway import FilesGateway


@dataclass
class ProcessFilesOutputDTO:
    files: io.BytesIO


class ProcessFilesUseCase:
    def __init__(
            self,
            files_gateway: FilesGateway,
            files_info_gateway: FileInfoGateway,
            session: AsyncSession,
    ) -> None:
        self.files_gateway = files_gateway
        self.files_info_gateway = files_info_gateway
        self.session = session

    async def __call__(
            self
    ) -> ProcessFilesOutputDTO:
        files = self.files_gateway.get_files()

        # process files here

        for file in files:
            await self.files_info_gateway.add_file_info(file.filename)

        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
            for file in files:
                zip_file.writestr(file.filename, file.data)

        zip_buffer.seek(0)

        await self.session.commit()

        return ProcessFilesOutputDTO(files=zip_buffer)
