from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, func, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.types import TIMESTAMP
import modules.db.initial as models
import datetime

Base = declarative_base()

engine = create_engine('mysql://root:123@127.0.0.1/sdo?charset=utf8', echo=True)

Session = sessionmaker(bind=engine)


def add_stat_test(data):
    print(data)
    session = Session()
    # find_stat_test = session.query(models.Tests_stat, models.Tests).join(models.Tests,
    #                                                        models.Tests.id == models.Tests_stat.test_id).filter(
    #     models.Tests_stat.user_id == data['id_user']).filter(models.Tests_stat.test_id == data[
    #         'id_test']).filter(models.Tests_stat.try_count == '-1').first()

    find_stat_test = session.query(models.Tests_stat, models.Tests).filter(
        models.Tests_stat.user_id == data['id_user'] and models.Tests_stat.test_id == data[
            'id_test'] and models.Tests_stat.try_count == '-1').first()
    session.close()

    if find_stat_test:
        response = dict.fromkeys(['answers', 'second_passed'])
        print(find_stat_test[0].start_time, 'старт теста')
        print(find_stat_test[1].duration, 'продолжительность теста')

        response['second_passed'] = (datetime.datetime.now() - find_stat_test[0].start_time).seconds
        response['answers'] = find_stat_test[0].answers

        return response
    else:
        new_stat_test = models.Tests_stat(data['id_user'], data['id_test'], data['answers'])
        session.add(new_stat_test)
        session.commit()
        session.close()
        return "success"


class Stat_tests(Base):
    __tablename__ = 'tests_stat'
    id = Column(Integer, primary_key=True)
    user_id = Column(
        Integer,
        ForeignKey('users.id'),
        nullable=False,
    )
    test_id = Column(
        Integer,
        ForeignKey('tests.id'),
        nullable=False
    )
    answers = Column(String(500))
    try_count = Column(Integer, default=-1)
    start_time = Column(TIMESTAMP(timezone=True), server_default=func.now())

    def __init__(self, user_id, test_id, answers):
        self.user_id = user_id
        self.test_id = test_id
        self.answers = answers


Base.metadata.create_all(bind=engine)
