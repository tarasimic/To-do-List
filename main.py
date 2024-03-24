from fastapi import FastAPI
from app.routes.auth import router as rout
from app.db.session import engine
from app.models import user

user.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(rout)

