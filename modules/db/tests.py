from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()

engine = create_engine('mysql://root:123@127.0.0.1/sdo?charset=utf8', echo=True)

Session = sessionmaker(bind=engine)


def get_test(id):
    find_test = dict.fromkeys(['course_id', 'problems', 'owner', 'duration'])

    session = Session()

    for test in session.query(Tests).filter(Tests.id == id):
        find_test['course_id'] = test.course_id
        find_test['problems'] = test.problems
        find_test['owner'] = test.owner
        find_test['duration'] = test.duration

    session.commit()
    session.close()

    return find_test


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

    def __init__(self, course_id, problems, owner, duration):
        self.course_id = course_id
        self.problems = problems
        self.owner = owner
        self.duration = duration


Base.metadata.create_all(bind=engine)
