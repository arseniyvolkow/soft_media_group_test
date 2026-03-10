from database import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer


class Link(Base):
    __tablename__ = "links"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    original_url: Mapped[str] = mapped_column(String(2048), unique=True, index=True, nullable=False)
    visits_count: Mapped[int] = mapped_column(Integer, default=0)