from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import modules.db.initial as models
import modules.db.theory as theory

Base = declarative_base()

engine = create_engine('mysql://root:123@127.0.0.1/sdo?charset=utf8', echo=True)

Session = sessionmaker(bind=engine)


def get_course(id_course):
    response = dict.fromkeys(['modules'])

    session = Session()

    modules_list = session.query(models.Modules) \
        .filter(models.Modules.course_id == id_course) \
        .order_by(models.Modules.order) \
        .all()
    response['modules'] = {m.id: dict.fromkeys(['name', 'course_id', 'tests', 'order', 'description', 'theory']) for m
                           in modules_list}
    print(response, 'resp')

    for module in modules_list:
        response['modules'][module.id]['name'] = module.name_module
        response['modules'][module.id]['course_id'] = module.course_id
        response['modules'][module.id]['tests'] = module.tests_id
        response['modules'][module.id]['description'] = module.description
        response['modules'][module.id]['theory'] = theory.get_list_theory(module.theory_id)

    print(response)

    # for module in modules_list:

    session.commit()
    session.close()

    return response


def get_teacher_course(id_owner):
    response = dict.fromkeys(['courses'])

    session = Session()

    course_list = session.query(models.Courses) \
        .filter(models.Courses.owner_id == id_owner) \
        .all()

    response['courses'] = {c.id: dict.fromkeys(['id', 'name_course', 'public']) for c in course_list}
    print(response, 'resp')

    for course in course_list:
        response['courses'][course.id]['id'] = course.id
        response['courses'][course.id]['name_course'] = course.name_course
        response['courses'][course.id]['public'] = course.public

    print(response)

    session.commit()
    session.close()

    return response
