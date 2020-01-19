import tornado.ioloop
import tornado.web
import json
import validators
import modules.db.users as db
from modules.db.problems import get_problem


class Users(tornado.web.RequestHandler):
    def post(self):
        success = True
        print(json.loads(self.request.body), '-------- json получен от реакта')

        reg_user_info = json.loads(self.request.body)

        if not reg_user_info['username']:
            success = False
        if (not validators.email(reg_user_info['email'])) or (not reg_user_info['email']):
            success = False
        if not reg_user_info['password']:
            success = False
        if (not reg_user_info['passwordConfirmation']) or (
                str(reg_user_info['password']) != str(reg_user_info['passwordConfirmation'])):
            success = False

        if success:
            response = {'success': True}
            new_user = db.User(reg_user_info['username'], reg_user_info['email'], reg_user_info['password'])

            db.User.add_user(new_user)
        else:
            response = {'success': False}

        self.write(json.dumps(response))

    def get(self):
        arg = str(self.get_argument("arg"))
        print(type(arg), arg)
        new_user = db.User(arg, arg, '1')
        self.write(new_user.check_uniqueness())


class Auth(tornado.web.RequestHandler):
    def post(self):
        user_login_info = json.loads(self.request.body)
        print(user_login_info)
        user_login = db.User('some_name', user_login_info['identifier'], user_login_info['password'])

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
