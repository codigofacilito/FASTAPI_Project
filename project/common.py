import jwt

from fastapi import Depends

from .database import User

from datetime import datetime
from datetime import timedelta

from fastapi.security import OAuth2PasswordBearer

oauth2_schema = OAuth2PasswordBearer(tokenUrl='/auth')

SECRET_KEY = 'CodigoFacilitoSECRET'

def create_access_token(user_id, username, days=7):
    data = {
        'user_id': user_id,
        'username': username,
        'exp': datetime.utcnow() + timedelta(days=days)
    }

    return jwt.encode(data, SECRET_KEY, algorithm='HS256')


def decode_access_token(token):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
    except Exception:
        return None


def token_is_valid(exp):
    return True


def get_current_user(token: str = Depends(oauth2_schema)) -> User:
    access_token = decode_access_token(token)

    if  access_token and access_token.get('user_id') and token_is_valid(access_token.get('exp')):
        return  User.select().where(User.id == access_token['user_id']).first()
    
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

