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


def update_theory(id_course, id_module, id_theory, data_theory):
    if id_theory == 'new' and data_theory['name_theory'] != '':

        session = Session()

        new_theory = models.Theory(data_theory['name_theory'], id_course, None, None, None, None)
        session.add(new_theory)
        session.commit()

        session.refresh(new_theory)
        id_new_theory = new_theory.id

        find_module = session.query(models.Modules) \
            .filter(models.Modules.id == id_module).first()

        if find_module.theory_id is None or find_module.theory_id == '':
            find_module.theory_id = str(id_new_theory)
        else:
            find_module.theory_id = str(find_module.theory_id) + '|' + str(id_new_theory)

        session.commit()
        session.close()

        return 'ok'

    elif id_theory != 'new':
        session = Session()

        find_theory = session.query(models.Theory) \
            .filter(models.Theory.id == id_theory).first()

        find_theory.name_theory = data_theory['name_theory']
        find_theory.body = data_theory['body']

        session.commit()
        session.close()

        return 'ok'
    else:
        return 'error'
