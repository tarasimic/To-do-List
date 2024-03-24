from sqlalchemy.orm import sessionmaker, Session
from ..db.session import SessionLocal, get_db
from fastapi import Depends, APIRouter, HTTPException
from ..models.task import Task
from ..schemas.task_base import TaskBase, DeleteTask
from .auth import secret_key, get_current_user
from jwt.exceptions import PyJWTError


router = APIRouter(prefix='/task')

@router.post('/create')
def create_task(new_task: TaskBase, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    db_task = Task(name=new_task.name, description=new_task.description, due_date=new_task.due_date)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

@router.post('/delete/{task_id}')
def delete_task(task_id: int, current_user: int = Depends(get_current_user), db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id==task_id).first()
    if task_id:
        db.delete(task)
        db.commit()
        return {'ok': True}
    else:
        raise HTTPException(status_code=404, detail='Task not found')
    

@router.post('/edit/{task_id}')
def edit_task(to_edit: TaskBase, task_id: int, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    task_to_update = db.query(Task).filter(Task.id==task_id).first()
    
    if not task_to_update:
        raise HTTPException(status_code=404, detail='Task not found')
    task_to_update.name = to_edit.name
    task_to_update.description = to_edit.description
    task_to_update.due_date = to_edit.due_date

    db.commit()
    return {'message': 'Edited successfully'}

@router.get('/get_task/{task_id}')
def get_task(task_id: int, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    task = db.query(Task).filter(Task.id==task_id).first()
    
    if not task:
        raise HTTPException(status_code=404, detail='Task not found')
    return task
