from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import modules.db.initial as models

Base = declarative_base()

engine = create_engine('mysql://root:123@127.0.0.1/sdo?charset=utf8', echo=True)

Session = sessionmaker(bind=engine)


def create_module(id_course, data_module):
    if data_module['name_module'] != '' and data_module['description_module'] != '':
        session = Session()

        new_module = models.Modules(data_module['name_module'], id_course, None, count_modules(id_course) + 1, None,
                                    data_module['description_module'])
        session.add(new_module)
        session.commit()
        session.close()

        return 'ok'
    else:
        return 'error'


def update_module(id_module, data_module):
    if data_module['name_module'] != '' and data_module['description_module'] != '':
        session = Session()

        find_module = session.query(models.Modules) \
            .filter(models.Modules.id == id_module).first()

        find_module.name_module = data_module['name_module']
        find_module.description = data_module['description_module']
        find_module.order = data_module['order']

        session.commit()
        session.close()

        return 'ok'
    else:
        return 'error'


def count_modules(id_course):
    session = Session()

    mod_cnt = session.query(models.Modules) \
        .filter(models.Modules.course_id == id_course).count()

    session.close()

    return mod_cnt
