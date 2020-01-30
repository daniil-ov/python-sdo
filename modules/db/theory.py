from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()

engine = create_engine('mysql://root:123@127.0.0.1/sdo?charset=utf8', echo=True)

Session = sessionmaker(bind=engine)


class Theory(Base):
    __tablename__ = 'theory'
    id = Column(Integer, primary_key=True)
    body = Column(String(3000))
    files = Column(String(100))
    created_date = Column(DateTime(timezone=True), server_default=func.now())

    def __init__(self, body, files):
        self.body = body
        self.files = files


Base.metadata.create_all(bind=engine)
