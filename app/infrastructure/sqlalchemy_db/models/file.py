from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.sqlalchemy_db.models import Base


class File(Base):
    __tablename__ = 'files'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, nullable=False)
