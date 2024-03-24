from fastapi import FastAPI
from app.routes.auth import router as auth_router
from app.db.session import engine
from app.models import user, task
from app.routes.task import router as task_router
from app.db.session import Base


user.Base.metadata.create_all(bind=engine)
task.Base.metadata.create_all(bind=engine)


app = FastAPI()

app.include_router(auth_router)
app.include_router(task_router)

