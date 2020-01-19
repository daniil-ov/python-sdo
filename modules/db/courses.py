from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()

engine = create_engine('mysql://root:123@127.0.0.1/test', echo=True)

Session = sessionmaker(bind=engine)


class Courses(Base):
    __tablename__ = 'courses'
    id = Column(Integer, primary_key=True)
    name_course = Column(String(100), unique=True)
    owner_id = Column(
        Integer,
        ForeignKey('users.id'),
        nullable=False)
    public = Column(Integer)
    created_date = Column(DateTime(timezone=True), server_default=func.now())

    def __init__(self, name_course, owner, public):
        self.name_course = name_course
        self.owner = owner
        self.public = public


Base.metadata.create_all(bind=engine)
