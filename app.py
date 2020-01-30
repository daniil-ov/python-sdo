import tornado.ioloop
import tornado.web
import json
import validators
import modules.db.users as db
from modules.db.problems import get_problem
from modules.db.users import get_user_with_email


class Users(tornado.web.RequestHandler):
    def post(self):
        success = True
        print(json.loads(self.request.body), '-------- json получен от реакта')

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

        # self.set_status(401)

        self.write(db.User.auth(user_login))


class Problem(tornado.web.RequestHandler):
    def get(self):
        id = str(self.get_argument("id"))
        print(id)

        self.write(get_problem(int(id)))


# r"/" == root website address
application = tornado.web.Application([
    (r"/api/users", Users),
    (r"/api/auth", Auth),
    (r"/api/problem", Problem)
], debug=True)

# Start the server at port 7777
if __name__ == "__main__":
    PortNumber = str(7777)
    print(r'Server Running at http://localhost:' + PortNumber + r'/')
    print(r'To close press ctrl + c')
    application.listen(PortNumber)
    tornado.ioloop.IOLoop.instance().start()
