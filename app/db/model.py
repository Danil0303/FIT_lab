from datetime import datetime

from sqlalchemy.dialects.mysql import FLOAT

from app.db.databases import Base
from sqlalchemy.orm import Mapped,mapped_column
from sqlalchemy import BigInteger, DateTime, BOOLEAN, String


class FitSubscribe(Base):
    __tablename__ = 'fit_subscrib'
    id_user: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    data_start: Mapped[datetime] = mapped_column(DateTime)
    data_end: Mapped[datetime] = mapped_column(DateTime)
    username: Mapped[str] = mapped_column(String)
    price: Mapped[float] = mapped_column(FLOAT)
    email_str: Mapped[str] = mapped_column(String)

