from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import bcrypt
import jwt
from sqlalchemy.types import TIMESTAMP
from sqlalchemy.dialects import mysql

Base = declarative_base()

engine = create_engine('mysql://root:123@127.0.0.1/sdo?charset=utf8', echo=True)

Session = sessionmaker(bind=engine)


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(40))
    second_name = Column(String(40))
    third_name = Column(String(40))
    email = Column(String(40), unique=True)
    user_status = Column(Integer)
    password_digest = Column(String(100))
    created_date = Column(DateTime(timezone=True), server_default=func.now())

    def __init__(self, name, second_name, third_name, email, user_status, password_digest):
        self.name = name
        self.second_name = second_name
        self.third_name = third_name
        self.email = email
        self.user_status = user_status
        self.password_digest = password_digest

    def add_user(self):
        session_for_new_user = Session()
        new_user = User(self.username, self.email,
                        bcrypt.hashpw(self.password_digest.encode('utf-8'), bcrypt.gensalt()))
        session_for_new_user.add(new_user)
        session_for_new_user.commit()
        session_for_new_user.close()

    def find_user_from_id(self):
        find_user = dict.fromkeys(['username', 'email'])

        session = Session()
        for user in session.query(User).filter(User.id == self.id):
            find_user['username'] = user.username
            find_user['email'] = user.email

        if find_user:
            success = True

        else:
            success = False
        session.commit()
        session.close()

        if success:
            print(find_user['username'], 'nameuser-------------')
            return find_user
        else:
            return False

    def check_uniqueness(self):
        user = dict.fromkeys(['user'])
        errors = {}
        session = Session()

        find_user = session.query(User).filter(User.username == self.username).one_or_none()
        if find_user is None:
            pass
        else:
            errors['username'] = find_user.username
            errors['email'] = find_user.email
            user['user'] = errors

        find_user = session.query(User).filter(User.email == self.email).one_or_none()
        if find_user is None:
            pass
        else:
            errors['username'] = find_user.username
            errors['email'] = find_user.email
            user['user'] = errors

        session.commit()
        session.close()

        return user

    def auth(self):
        session = Session()
        response = {'isValid': False, 'errors': None, 'jwt': None}
        errors = dict.fromkeys(['errors'])
        form = dict.fromkeys(['form'])

        find_user_for_auth = session.query(User).filter(User.email == self.email).one_or_none()
        if find_user_for_auth is None:
            form['form'] = 'Пользователь с такой почтой не найден'
            response['errors'] = form
            session.commit()
            session.close()
            return response
        else:
            if bcrypt.checkpw(self.password_digest.encode('utf-8'), find_user_for_auth.password_digest.encode('utf-8')):
                encoded_jwt = jwt.encode({'id': find_user_for_auth.id, 'email': find_user_for_auth.email}, '!secret!',
                                         algorithm='HS256').decode('utf-8')
                print("нашел такого пользователя")
                response['isValid'] = True
                response['jwt'] = encoded_jwt
                session.commit()
                session.close()
                return response
            else:
                form['form'] = 'Пароль неверный'
                response['errors'] = form
                session.commit()
                session.close()
                return response


class Tests_stat(Base):
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


class Courses(Base):
    __tablename__ = 'courses'
    id = Column(Integer, primary_key=True)
    name_course = Column(String(100), unique=True)
    description_course = Column(mysql.TEXT(collation=u'utf8_general_ci'), nullable=False)
    owner_id = Column(
        Integer,
        ForeignKey('users.id'),
        nullable=False)
    public = Column(Integer)
    created_date = Column(DateTime(timezone=True), server_default=func.now())

    def __init__(self, name_course, description_course, owner_id, public):
        self.name_course = name_course
        self.description_course = description_course
        self.owner_id = owner_id
        self.public = public


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


class Theory(Base):
    __tablename__ = 'theory'
    id = Column(Integer, primary_key=True)
    name_theory = Column(String(200))
    course_id = Column(Integer)
    parent_id = Column(Integer)
    tests_id = Column(String(300))
    body = Column(String(3000))
    files = Column(String(100))
    created_date = Column(DateTime(timezone=True), server_default=func.now())

    def __init__(self, name_theory, body, files):
        self.name_theory = name_theory
        self.body = body
        self.files = files


class Modules(Base):
    __tablename__ = 'modules'
    id = Column(Integer, primary_key=True)
    name_module = Column(String(100), unique=True)
    course_id = Column(
        Integer,
        ForeignKey('courses.id'),
        nullable=False,
    )
    tests_id = Column(
        String(100))
    order = Column(Integer)
    theory_id = Column(
        String(50))
    description = Column(String(1000))
    created_date = Column(DateTime(timezone=True), server_default=func.now())

    def __init__(self, name_module, course_id, test_id, order, theory_id, description):
        self.name_module = name_module
        self.course_id = course_id
        self.test_id = test_id
        self.order = order
        self.theory_id = theory_id
        self.description = description




Base.metadata.create_all(bind=engine)