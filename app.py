import tornado.ioloop
import tornado.web
import json
import validators
import modules.db.users as db
from modules.db.gen_test import get_gen_test
from modules.db.modules import create_module, update_module
from modules.db.problems import get_problem, check_test, get_theory_problems, update_problem
from modules.db.tests import get_test
from modules.db.theory import get_theory, update_theory
from modules.db.users import get_user_with_email
from modules.db.tests_stat import add_stat_test
from modules.db.courses import get_course, get_teacher_course, create_course


class Users(tornado.web.RequestHandler):
    def post(self):
        success = True
        # print(json.loads(self.request.body), '-------- json получен от реакта')

        reg_user_info = json.loads(self.request.body)

        if not reg_user_info['name']:
            success = False
        if not reg_user_info['second_name']:
            success = False
        if not reg_user_info['third_name']:
            success = False
        if (not validators.email(reg_user_info['email'])) or (not reg_user_info['email']):
            success = False
        if not reg_user_info['password']:
            success = False
        if (not reg_user_info['passwordConfirmation']) or (
                str(reg_user_info['password']) != str(reg_user_info['passwordConfirmation'])):
            success = False
        if reg_user_info['status'] == 'student':
            reg_user_info['status'] = 0
        elif reg_user_info['status'] == 'teacher':
            reg_user_info['status'] = 1

        if success:
            response = {'success': True}
            new_user = db.User(reg_user_info['name'], reg_user_info['second_name'], reg_user_info['third_name'],
                               reg_user_info['email'], reg_user_info['status'], reg_user_info['password'])

            db.User.add_user(new_user)
        else:
            response = {'success': False}

        self.write(json.dumps(response))

    def get(self):
        email = str(self.get_argument("email"))
        print(email)

        self.write(get_user_with_email(email))


class Auth(tornado.web.RequestHandler):
    def post(self):
        user_login_info = json.loads(self.request.body)
        print(user_login_info)
        user_login = db.User('name', 'second_name', 'third_name', user_login_info['mail'], '0',
                             user_login_info['password'])

        self.write(db.User.auth(user_login))


class Problem(tornado.web.RequestHandler):
    def get(self):
        id = str(self.get_argument("id"))

        self.write(get_problem(int(id)))

    def post(self):
        id = str(self.get_argument("id"))

        self.write(update_problem(id, json.loads(self.request.body)))


class Test(tornado.web.RequestHandler):
    def get(self):
        id = str(self.get_argument("id"))

        self.write(get_test(int(id)))


class CheckTest(tornado.web.RequestHandler):
    def post(self):
        self.write(check_test(self.request.body))


class StatTest(tornado.web.RequestHandler):
    def post(self):
        self.write(add_stat_test(json.loads(self.request.body)))


class Course(tornado.web.RequestHandler):
    def post(self):
        new_course = json.loads(self.request.body)
        self.write(create_course(new_course))

    def get(self):
        id = str(self.get_argument("id"))

        self.write(get_course(int(id)))


class Module(tornado.web.RequestHandler):
    def post(self):
        data_module = json.loads(self.request.body)
        id_course = str(self.get_argument("id_course"))
        id_module = str(self.get_argument("id_module"))
        if id_module == 'new':
            self.write(create_module(id_course, data_module))
        else:
            self.write(update_module(id_module, data_module))


class CourseOwner(tornado.web.RequestHandler):
    def get(self):
        id = str(self.get_argument("id"))

        self.write(get_teacher_course(int(id)))


class Theory(tornado.web.RequestHandler):
    def get(self):
        id = str(self.get_argument("id"))

        self.write(get_theory(int(id)))

    def post(self):
        id_module = str(self.get_argument("id_module"))
        id_theory = str(self.get_argument("id_theory"))
        id_course = str(self.get_argument("id_course"))
        data_theory = json.loads(self.request.body)
        self.write(update_theory(int(id_course), id_module, id_theory, data_theory))


class TheoryProblems(tornado.web.RequestHandler):
    def get(self):
        id_theory = str(self.get_argument("id_theory"))

        self.write(get_theory_problems(int(id_theory)))


class GenTest(tornado.web.RequestHandler):
    def get(self):
        id_course = str(self.get_argument("id_course"))

        self.write(get_gen_test(int(id_course)))


# r"/" == root website address
application = tornado.web.Application([
    (r"/api/users", Users),
    (r"/api/auth", Auth),
    (r"/api/problem", Problem),
    (r"/api/test", Test),
    (r"/api/check_test", CheckTest),
    (r"/api/add_stat", StatTest),
    (r"/api/course", Course),
    (r"/api/course_owner", CourseOwner),
    (r"/api/theory", Theory),
    (r"/api/module", Module),
    (r"/api/theory_problems", TheoryProblems),
    (r"/api/gen_test", GenTest)
], debug=True)

# Start the server at port 7777
if __name__ == "__main__":
    PortNumber = str(7777)
    print(r'Server Running at http://localhost:' + PortNumber + r'/')
    print(r'To close press ctrl + c')
    application.listen(PortNumber)
    tornado.ioloop.IOLoop.instance().start()
