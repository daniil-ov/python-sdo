from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import modules.db.initial as models
from modules.db.problems import count_problems_theory

engine = create_engine('mysql://root:123@127.0.0.1/sdo?charset=utf8', echo=True)

Session = sessionmaker(bind=engine)


def get_gen_test(id_course):
    response = {}

    session = Session()

    modules_list = session.query(models.Modules) \
        .filter(models.Modules.course_id == id_course) \
        .order_by(models.Modules.order) \
        .all()
    for module in modules_list:
        cnt_prob_in_module = 0
        if module.theory_id:
            for t in module.theory_id.split('|'):
                cnt_prob_in_module += count_problems_theory(t)
                theory_f = session.query(models.Theory) \
                    .filter(models.Theory.id == t) \
                    .one_or_none()
                if theory_f:
                    gen_test_f = session.query(models.Gen_test) \
                        .filter(models.Gen_test.theory_id == t) \
                        .all()
                    if gen_test_f:
                        for gen_t in gen_test_f:
                            response[gen_t.id] = {}
                            response[gen_t.id]['active'] = gen_t.active
                            response[gen_t.id]['theory_id'] = gen_t.theory_id
                            response[gen_t.id]['module_id'] = gen_t.module_id
                            response[gen_t.id]['name'] = theory_f.name_theory
                            response[gen_t.id]['cnt_bank'] = count_problems_theory(t)
                            response[gen_t.id]['cnt_in_test'] = gen_t.count_prob
                            response[gen_t.id]['random_switch'] = gen_t.random_switch

        gen_t_module = session.query(models.Gen_test) \
            .filter(models.Gen_test.module_id == module.id) \
            .all()
        if gen_t_module:
            for gen_t in gen_t_module:
                response[gen_t.id] = {}
                response[gen_t.id]['active'] = gen_t.active
                response[gen_t.id]['theory_id'] = gen_t.theory_id
                response[gen_t.id]['module_id'] = gen_t.module_id
                response[gen_t.id]['name'] = module.name_module
                response[gen_t.id]['cnt_bank'] = cnt_prob_in_module
                response[gen_t.id]['cnt_in_test'] = gen_t.count_prob
                response[gen_t.id]['random_switch'] = gen_t.random_switch

    session.commit()
    session.close()

    return response



