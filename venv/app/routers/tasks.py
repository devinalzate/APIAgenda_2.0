from fastapi import APIRouter
from fastapi.responses import JSONResponse
from ..models.models import Task, TaskBase, User 
from database.db import SessionDep
from sqlmodel import select

router = APIRouter()

@router.get("/get_tasks", tags=["Tasks"])
async def get_tasks(session : SessionDep):
    return session.exec(select(Task)).all()

@router.get("/get_task", tags=["Tasks"])
async def get_task(session: SessionDep, id_task : int):
    taks_find = session.get(Task, id_task)
    if taks_find:
        return taks_find
    return JSONResponse(content={'state': "Incorrecto", 
                                    'msg': f"No se ha encontrado ninguna tarea con id {id_task}"
                                })
    
@router.post("/add_task", tags=["Tasks"])        
async def add_task(session : SessionDep, task: TaskBase):
    new_task = task.model_dump()
    validate = Task.model_validate(new_task)
    id = new_task['user_id']
    if validate:
        user = session.get(User, id)
        if not user:
            return JSONResponse(content={'state': "Incorrecto", 
                                     'msg': f"No existe usuario de id {id}"
                                    })
        session.add(validate)
        session.commit()
        session.refresh(validate)
        return JSONResponse(content={'state': "Correcto", 
                                     'msg': "La tarea ha sido creada correctamente"
                                    })
    return JSONResponse(content={'state': "Incorrecto", 
                                     'msg': "La tarea no ha sido ingresada correctamente"
                                    })
    
@router.delete("/delete_task", tags=["Tasks"])
async def delete_task(session: SessionDep, id_task : int):
    task_found = session.get(Task, id_task)
    if task_found:
        session.delete(task_found)
        return JSONResponse(content={'state': "Correcto", 
                                     'msg': "La tarea ha sido eliminada correctamente"
                                    })
    return JSONResponse(content={'state': "Incorrecto", 
                                     'msg': f"No se ha encontrado ninguna tarea con id {id_task}"
                                    })

@router.put("/update_task", tags=["Tasks"])
async def update_task(session: SessionDep, task : TaskBase, id_task : int):
    task_find = session.get(Task, id_task)
    if task_find:
        task_update = task.model_dump(exclude_unset=True)
        task_find.sqlmodel_update(task_update)
        session.add(task_find)
        session.commit()
        session.refresh(task_find)
        return JSONResponse(content={'state': "Correcto", 
                                     'msg': "La tarea ha sido actualizada correctamente"
                                    })
    return JSONResponse(content={'state': "Incorrecto", 
                                     'msg': "La tarea no ha sido encontrada"
                                    })