from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import modules.db.initial as models

engine = create_engine('mysql://root:123@127.0.0.1/sdo?charset=utf8', echo=True)

Session = sessionmaker(bind=engine)


def get_theory(id_theory):
    response = dict.fromkeys(['name_theory', 'course_id', 'parent_id', 'tests', 'body', 'files'])

    session = Session()
    theory_item = session.query(models.Theory) \
        .filter(models.Theory.id == id_theory) \
        .first()
    response['name_theory'] = theory_item.name_theory
    response['course_id'] = theory_item.course_id
    response['parent_id'] = theory_item.parent_id
    response['tests'] = theory_item.tests_id
    response['body'] = theory_item.body
    response['files'] = theory_item.files

    print(response)

    session.commit()
    session.close()

    return response


def get_list_theory(id_theory):
    print(id_theory, 'id_theory')
    list_theory = id_theory.split('|')

    response = {i: dict.fromkeys(['name_theory', 'course_id', 'parent_id', 'tests']) for i in list_theory}

    session = Session()

    for theory in list_theory:
        theory_item = session.query(models.Theory) \
            .filter(models.Theory.id == theory) \
            .first()

        response[theory]['name_theory'] = theory_item.name_theory
        response[theory]['course_id'] = theory_item.course_id
        response[theory]['parent_id'] = theory_item.parent_id
        response[theory]['tests'] = theory_item.tests_id

    print(response)

    session.commit()
    session.close()

    return response
