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
        for problem in session.query(models.Problems).filter(models.Problems.id == answer):
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

    for problem in session.query(models.Problems).filter(models.Problems.id == id):
        find_problem['body'] = problem.body
        find_problem['type_question'] = problem.type_question
        find_problem['answer_1'] = problem.answer_1
        find_problem['answer_2'] = problem.answer_2
        find_problem['answer_3'] = problem.answer_3
        find_problem['answer_4'] = problem.answer_4

    session.commit()
    session.close()

    # print(str(find_problem['body']), 'body--------------1')
    return find_problem


def get_theory_problems(id_theory):
    theory_problems = {}

    session = Session()

    for problem in session.query(models.Problems).filter(models.Problems.theory_id == id_theory):
        theory_problems[problem.id] = {}

        theory_problems[problem.id]['id'] = problem.id
        theory_problems[problem.id]['course_id'] = problem.course_id
        theory_problems[problem.id]['type_question'] = problem.type_question
        theory_problems[problem.id]['status_id'] = problem.status_id
        theory_problems[problem.id]['theory_id'] = problem.theory_id
        theory_problems[problem.id]['body'] = problem.body
        theory_problems[problem.id]['solution'] = problem.solution
        theory_problems[problem.id]['answer'] = problem.answer
        theory_problems[problem.id]['answer_1'] = problem.answer_1
        theory_problems[problem.id]['answer_2'] = problem.answer_2
        theory_problems[problem.id]['answer_3'] = problem.answer_3
        theory_problems[problem.id]['answer_4'] = problem.answer_4
        theory_problems[problem.id]['mark'] = problem.mark

    session.commit()
    session.close()

    return theory_problems


def update_problem(id_problem, data_problem):
    if id_problem == 'new':
        print(data_problem, 'data_problem')

        session = Session()

        if data_problem['type_question'] == 1:
            new_problem = models.Problems(data_problem['course_id'], data_problem['type_question'],
                                          data_problem['status_id'], data_problem['theory_id'], data_problem['body'],
                                          data_problem['solution'],
                                          data_problem['answer'], data_problem['answer_1'], data_problem['answer_2'],
                                          data_problem['answer_3'], data_problem['answer_4'], data_problem['mark'])
        elif data_problem['type_question'] == 2:
            new_problem = models.Problems(data_problem['course_id'], data_problem['type_question'],
                                          data_problem['status_id'], data_problem['theory_id'], data_problem['body'],
                                          data_problem['solution'],
                                          data_problem['answer'], None, None,
                                          None, None, data_problem['mark'])

        session.add(new_problem)
        session.commit()
        session.close()

        return 'ok'

    elif id_problem != 'new':
        print(data_problem, 'data_problem')
        session = Session()

        find_problem = session.query(models.Problems) \
            .filter(models.Problems.id == id_problem).first()

        find_problem.id = data_problem['id']
        find_problem.course_id = data_problem['course_id']
        find_problem.type_question = data_problem['type_question']
        find_problem.status_id = data_problem['status_id']
        find_problem.theory_id = data_problem['theory_id']
        find_problem.body = data_problem['body']
        find_problem.solution = data_problem['solution']
        find_problem.answer = data_problem['answer']
        find_problem.answer_1 = data_problem['answer_1']
        find_problem.answer_2 = data_problem['answer_2']
        find_problem.answer_3 = data_problem['answer_3']
        find_problem.answer_4 = data_problem['answer_4']
        find_problem.mark = data_problem['mark']

        session.commit()
        session.close()

        return 'ok'
    else:
        return 'error'


def count_problems_theory(id_theory):
    session = Session()
    cnt = session.query(models.Problems) \
        .filter(models.Problems.theory_id == id_theory) \
        .count()

    session.commit()
    session.close()

    return cnt
