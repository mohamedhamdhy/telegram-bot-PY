from sqlalchemy import Column, Integer, String, LargeBinary, Text, BigInteger
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Note(Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(BigInteger, index=True)
    file_name = Column(String, nullable=True)
    file_type = Column(String)
    content = Column(LargeBinary, nullable=True)
    text_content = Column(Text, nullable=True)
