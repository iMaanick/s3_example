from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter
from starlette.responses import StreamingResponse

from app.application.use_cases.process_files import ProcessFilesUseCase

index_router = APIRouter()


@index_router.get("/processed_files", )
@inject
async def get_processed_files(
        use_case: FromDishka[ProcessFilesUseCase]
) -> StreamingResponse:
    data = await use_case()
    return StreamingResponse(
        data.files,
        media_type="application/zip",
        headers={"Content-Disposition": "attachment; filename=files.zip"}
    )
