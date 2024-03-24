from ..schemas.user_base import UserBase, UserLogin
from ..models.user import User
from sqlalchemy.orm import sessionmaker, Session
from ..db.session import SessionLocal, get_db
from fastapi import Depends, APIRouter, HTTPException
import jwt

router = APIRouter(prefix='/auth')

@router.post('/register')
def register_user(new_user: UserBase, db: Session = Depends(get_db)):
    db_user = User(name=new_user.name, last_name=new_user.last_name, email=new_user.email, password=new_user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.post('/login')
def login_user(user_login: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == user_login.email, User.password == user_login.password).first()    
    if not user:
        raise HTTPException(status_code=401, detail='Invalid credentials')
    token = generate_jwt(user)
    return token

def generate_jwt(user: User):
    payload = {'user_id': user.id, 'email': user.email}
    secret_key = 'secret_key'
    token = jwt.encode(payload, secret_key, algorithm='HS256')
    return token