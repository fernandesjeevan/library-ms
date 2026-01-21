from sqlalchemy import String , Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base

class Book(Base):
    __tablename__ ="books"
    id:Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[int] = mapped_column(String(200),index=True)
    author: Mapped[str] = mapped_column(String(200),index=True)
    genre:Mapped[str] = mapped_column(String(100),nullable=True)
    no_of_pages: Mapped[int] = mapped_column(Integer, nullable=True)
    publication: Mapped[str] = mapped_column(String(100),nullable=True)

    
