import json

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import modules.db.initial as models
import modules.db.tests_stat as tests_stat

Base = declarative_base()

engine = create_engine('mysql://root:123@127.0.0.1/sdo?charset=utf8', echo=True)

Session = sessionmaker(bind=engine)


def check_test(answers_json):
    answers = json.loads(answers_json)
    for answer in answers['answers']:
        answers['answers'][answer.lstrip('answers_')] = answers['answers'].pop(answer)

    print(answers['answers'], 'answers')
    result_test = dict.fromkeys(answers['answers'])
    print(result_test, 'result_test')

    session = Session()

    # Подсчет количества баллов
    student_points = 0
    max_points = 0

    for answer in answers['answers'].keys():
        for problem in session.query(Problems).filter(Problems.id == answer):
            max_points = max_points + problem.mark

            if problem.answer == answers['answers'][answer]:
                result_test[answer] = True
                student_points = student_points + problem.mark
            else:
                result_test[answer] = False

    # выставление оценки
    mark_student = 2
    try:
        if student_points / max_points >= 0.85:
            mark_student = 5
        elif student_points / max_points >= 0.65:
            mark_student = 4
        elif student_points / max_points >= 0.5:
            mark_student = 3
    except ZeroDivisionError:
        pass

    result = {'result': result_test}
    result.update({'mark': mark_student})

    session.query(models.Tests_stat) \
        .filter(models.Tests_stat.test_id == answers['id_test']) \
        .filter(models.Tests_stat.try_count == '-1') \
        .filter(models.Tests_stat.user_id == answers['id_user']) \
        .update({'try_count': tests_stat.count_try_tests(answers['id_user'], answers['id_test']) + 1})

    session.commit()
    session.close()

    print(result_test, 'result')
    return result


def get_problem(id):
    find_problem = dict.fromkeys(['body', 'answer_1', 'answer_2', 'answer_3', 'answer_4'])

    session = Session()

    for problem in session.query(Problems).filter(Problems.id == id):
        find_problem['body'] = problem.body
        find_problem['type_question'] = problem.type_question
        find_problem['answer_1'] = problem.answer_1
        find_problem['answer_2'] = problem.answer_2
        find_problem['answer_3'] = problem.answer_3
        find_problem['answer_4'] = problem.answer_4

    session.commit()
    session.close()

    print(str(find_problem['body']), 'body--------------1')
    return find_problem


class Problem_status(Base):
    __tablename__ = 'problem_status'
    STATUS_INITIAL = 0

    id = Column(Integer, primary_key=True)
    name = Column(String(20), unique=True)


class Problems(Base):
    __tablename__ = 'problems'
    id = Column(Integer, primary_key=True)
    course_id = Column(
        Integer,
        ForeignKey('courses.id'),
        nullable=False
    )
    type_question = Column(Integer)
    status_id = Column(
        Integer,
        ForeignKey('problem_status.id'),
        nullable=False,
        default=Problem_status.STATUS_INITIAL)
    module_id = Column(
        Integer,
        ForeignKey('modules.id')
    )
    body = Column(String(3000))
    solution = Column(String(3000))
    answer = Column(String(100))
    answer_1 = Column(String(100))
    answer_2 = Column(String(100))
    answer_3 = Column(String(100))
    answer_4 = Column(String(100))
    mark = Column(Integer)
    created_date = Column(DateTime(timezone=True), server_default=func.now())

    def __init__(self, type_question, body, solution, answer, answer_1, answer_2, answer_3, answer_4, mark):
        self.type_question = type_question
        self.body = body
        self.solution = solution
        self.answer = answer
        self.answer_1 = answer_1
        self.answer_2 = answer_2
        self.answer_3 = answer_3
        self.answer_4 = answer_4
        self.mark = mark

    def get_problem(self, id):
        find_problem = dict.fromkeys(['body'])

        session = Session()
        for body in session.query(Problems.id).filter(Problems.id == id):
            print(body)

        for problem in session.query(Problems).filter(Problems.id == id):
            find_problem['body'] = problem.body

        if find_problem:
            success = True
        else:
            success = False

        session.commit()
        session.close()

        if success:
            print(str(find_problem['body'].encode('utf-8')), 'body-------------1')
            return find_problem
        else:
            return False


Base.metadata.create_all(bind=engine)
