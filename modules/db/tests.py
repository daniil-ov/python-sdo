from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()

engine = create_engine('mysql://root:123@127.0.0.1/test', echo=True)

Session = sessionmaker(bind=engine)


class Tests(Base):
    __tablename__ = 'tests'
    id = Column(Integer, primary_key=True)
    course_id = Column(
        Integer,
        ForeignKey('courses.id'),
        nullable=False,
    )
    problems = Column(String(300))
    owner = Column(Integer)
    duration = Column(Integer)
    created_date = Column(DateTime(timezone=True), server_default=func.now())

    def __init__(self, type_question, body, solution, answer, answer0, answer1, answer2, answer3):
        self.type_question = type_question
        self.body = body
        self.solution = solution
        self.answer = answer
        self.answer0 = answer0
        self.answer1 = answer1
        self.answer2 = answer2
        self.answer3 = answer3


Base.metadata.create_all(bind=engine)
