from typing import Optional

from sqlalchemy import select
from sqlalchemy.dialects.sqlite import insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.sqlalchemy_db import models
from app.application.models import Student, Score
from app.application.protocols import StudentGateway
from app.application.protocols.database import ScoreGateway


class StudentSqlaGateway(StudentGateway):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def upsert_student(self, tg_id: int, first_name: str, last_name: str) -> None:
        kwargs = dict(
            tg_id=tg_id,
            first_name=first_name,
            last_name=last_name,
        )

        stmt = insert(models.Student).values(**kwargs).on_conflict_do_update(
            index_elements=[models.Student.tg_id],
            set_=dict(first_name=first_name, last_name=last_name),
        )

        await self.session.execute(stmt)
        await self.session.commit()

    async def get_by_tg_id(self, tg_id: int) -> Optional[Student]:
        stmt = select(models.Student).where(models.Student.tg_id == tg_id)
        result = await self.session.execute(stmt)
        student = result.scalars().first()
        if not student:
            return None
        return student.to_dto()


class ScoreSqlaGateway(ScoreGateway):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def upsert_score(self, subject: str, score: int, tg_id: int) -> None:
        stmt = insert(models.File).values(
            subject=subject,
            score=score,
            tg_id=tg_id
        ).on_conflict_do_update(
            index_elements=['tg_id', 'subject'],
            set_={'score': score}
        )
        await self.session.execute(stmt)
        await self.session.commit()

    async def get_scores_by_tg_id(self, tg_id: int) -> list[Score]:
        stmt = select(models.File).where(models.File.tg_id == tg_id)
        result = await self.session.execute(stmt)
        scores = result.scalars().all()
        if not scores:
            return []
        return [score.to_dto() for score in scores]
