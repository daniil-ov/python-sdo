from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import bcrypt
import jwt

Base = declarative_base()

engine = create_engine('mysql://root:123@127.0.0.1/test', echo=True)

Session = sessionmaker(bind=engine)


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(40), unique=True)
    email = Column(String(40), unique=True)
    password_digest = Column(String(100))
    created_date = Column(DateTime(timezone=True), server_default=func.now())
    updated_date = Column(DateTime(timezone=True), onupdate=func.now())

    def __init__(self, username, email, password_digest):
        self.username = username
        self.email = email
        self.password_digest = password_digest

    def __repr__(self):
        return "<User('%s', '%s', '%s')>" % (self.username, self.email, self.password_digest)

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


Base.metadata.create_all(bind=engine)
