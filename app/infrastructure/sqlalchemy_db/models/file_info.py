from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.sqlalchemy_db.models import Base


class FileInfoORM(Base):
    __tablename__ = 'file_info'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, nullable=False)
    file_name: Mapped[str] = mapped_column(nullable=False, unique=True)
