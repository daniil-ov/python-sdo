from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, func, update, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.types import TIMESTAMP
import modules.db.initial as models
import datetime

Base = declarative_base()

engine = create_engine('mysql://root:123@127.0.0.1/sdo?charset=utf8', echo=True)

Session = sessionmaker(bind=engine)


def count_try_tests(user_id, test_id):
    session = Session()

    try_cnt = session.query(models.Tests_stat) \
        .filter(models.Tests_stat.try_count != '-1') \
        .filter(models.Tests_stat.user_id == user_id) \
        .filter(models.Tests_stat.test_id == test_id).count()

    session.close()

    return try_cnt


def add_stat_test(data):
    print(data)
    response = dict.fromkeys(['answers', 'second_passed'])
    response['second_passed'] = 0
    response['answers'] = {}

    session = Session()

    find_stat_test = session.query(models.Tests_stat, models.Tests) \
        .filter(models.Tests_stat.try_count == '-1') \
        .filter(models.Tests_stat.user_id == data['id_user']) \
        .filter(models.Tests_stat.test_id == data['id_test']).first()
    session.close()

    if not find_stat_test:
        session = Session()
        new_stat_test = models.Tests_stat(data['id_user'], data['id_test'], data['answers'])
        session.add(new_stat_test)
        session.commit()
        session.close()

    else:
        delta_time = (datetime.datetime.now() - find_stat_test[0].start_time).seconds
        print(delta_time, 'прошло времени до')
        if delta_time > find_stat_test[1].duration:
            print(delta_time, 'прошло времени')
            session = Session()

            session.query(models.Tests_stat) \
                .filter(models.Tests_stat.id == find_stat_test[0].id) \
                .update({'try_count': count_try_tests(data['id_user'], data['id_test']) + 1})

            new_stat_test = models.Tests_stat(data['id_user'], data['id_test'], data['answers'])
            session.add(new_stat_test)

            session.commit()

            print(find_stat_test[0].start_time, 'старт теста')
            print(find_stat_test[1].duration, 'продолжительность теста')

        else:
            print(find_stat_test[0].start_time, 'старт теста')
            print(find_stat_test[1].duration, 'продолжительность теста')

            if data['answers'] != {}:
                session = Session()

                session.query(models.Tests_stat) \
                    .filter(models.Tests_stat.id == find_stat_test[0].id) \
                    .update({'answers': data['answers']})

                session.commit()

            response['second_passed'] = delta_time
            response['answers'] = find_stat_test[0].answers

    return response


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
