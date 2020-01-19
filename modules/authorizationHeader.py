import jwt


def authorization_header(data):
    token = None
    decode_token = None
    error = None

    if data.request.headers.get('Authorization'):
        token = data.request.headers.get('Authorization').split(' ')[1]
    if not token:
        error = 'Нет токена'
        return error, decode_token
    else:
        try:
            decode_token = jwt.decode(token, '!secret!', algorithms=['HS256'])
        except (jwt.DecodeError, jwt.ExpiredSignatureError):
            error = 'Неверный токен'
            return error, decode_token
        if decode_token:
            return error, decode_token
