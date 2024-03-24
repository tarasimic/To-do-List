from ..schemas.user_base import UserBase, UserLogin
from ..models.user import User
from sqlalchemy.orm import sessionmaker, Session
from ..db.session import SessionLocal, get_db
from fastapi import Depends, APIRouter, HTTPException
import jwt
from passlib.context import CryptContext
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt.exceptions import PyJWTError
from datetime import datetime, timedelta

router = APIRouter(prefix='/auth')
password_context = CryptContext(schemes=["bcrypt"], deprecated='auto')
secret_key = 'secret_key'


@router.post('/register')
def register_user(new_user: UserBase, db: Session = Depends(get_db)):
    hashed_password = password_context.hash(new_user.password)
    db_user = User(name=new_user.name, last_name=new_user.last_name, email=new_user.email, password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.post('/login')
def login_user(user_login: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == user_login.email).first()
    if not user:
        raise HTTPException(status_code=401, detail='Invalid credentials')
    hashed = user.password
    
    verify = verify_password(user_login.password, hashed)
    
    if not verify:
        raise HTTPException(status_code=401, detail='Invalid credentials')
    
    token = generate_jwt(user)
    return token

def generate_jwt(user: User):
    expiration_time = datetime.utcnow() + timedelta(hours=1)

    payload = {'user_id': user.id, 'email': user.email, 'exp': expiration_time}
    secret_key = 'secret_key'
    token = jwt.encode(payload, secret_key, algorithm='HS256')
    return token

def verify_password(password: str, hashed_pass: str):
    return password_context.verify(password, hashed_pass)

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())):
    try:
        token = credentials.credentials
        payload = jwt.decode(token, secret_key, algorithms=['HS256'])
        user_id = payload.get('user_id')
        
        if user_id is None:
            raise HTTPException(status_code=401, detail='Invalid token')

        return user_id
    except PyJWTError:
        raise HTTPException(status_code=401, detail='Invalid token')