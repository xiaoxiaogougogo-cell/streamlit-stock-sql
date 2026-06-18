from jose import jwt

SECRET_KEY = "CHANGE_ME"

def create_token(data):
    return jwt.encode(data, SECRET_KEY, algorithm="HS256")
