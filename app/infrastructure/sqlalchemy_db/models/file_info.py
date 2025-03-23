from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.sqlalchemy_db.models import Base


class FileInfo(Base):
    __tablename__ = 'file_info'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, nullable=False)
