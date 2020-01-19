import tornado.ioloop
import tornado.web
from modules.authorizationHeader import authorization_header
import db


class Events(tornado.web.RequestHandler):
    def post(self):
        error, decode_token = authorization_header(self)

        if not error:
            user = db.User(None, None, None)
            user.id = decode_token['id']

            find_user = db.User.find_user_from_id(user)
            if not find_user:
                success = False
                print('нет такого')
                self.write({'error': 'нет такого пользователя'})
            else:
                print('есть такой')
                success = True
                self.write(find_user)
        else:
            self.write('access denied!')
