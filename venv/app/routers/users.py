from fastapi import APIRouter
from fastapi.responses import JSONResponse
from database.db import SessionDep
from sqlmodel import select
from ..models.models import User, UserBase

router = APIRouter()

@router.get("/get_users", tags=["Users"])
async def get_users(session : SessionDep):
    return session.exec(select(User)).all()

@router.get("/get_user", tags=["Users"])
async def get_user(session: SessionDep, id_user : int):
    user_find = session.get(User, id_user)
    if user_find:
        return user_find.model_dump()

@router.get("/get_user_task", tags=["Users"])
async def get_user_task(session: SessionDep, id_user : int):
    user_find = session.get(User, id_user)
    list_tasks = user_find.tasks
    return list_tasks

@router.post("/add_user", tags=["Users"])
async def add_user(user : UserBase, session: SessionDep):
    new_user = user.model_dump()
    final_user = User.model_validate(new_user)
    if final_user:
        session.add(final_user)
        session.commit()
        session.refresh(final_user)
        return JSONResponse(content = {'state' : "Correcto", 
                                       'msg' : "El usuario ha sido creado de forma correcta"
                                        })
    return JSONResponse(content = {'state' : "Incorrecto", 
                                   'msg' : "No ha sido posible crear el usuario"
                                   })    

@router.delete("/delete_user", tags=["Users"])
async def delete_user(session: SessionDep, id_user : int ):
    user_find = session.get(User, id_user)
    if user_find:
        session.delete(user_find)
        session.commit()
        return JSONResponse(content = {'state' : "Correcto", 
                                       'msg' : "El usuario ha sido eliminado de forma correcta"
                                       })
    return JSONResponse(content = {'state' : "Incorrecto", 
                                   'msg' : f"El usuario de id {id_user} no ha sido encontrado"
                                   })    

@router.put("/update_user", tags=["Users"])
async def update_user(session: SessionDep, id_user :int, user : UserBase):
    user_find = session.get(User, id_user)
    if user_find:
        user_update = user.model_dump(exclude_unset=True)
        user_find.sqlmodel_update(user_update)
        session.add(user_find)
        session.commit()
        session.refresh(user_find)
        return JSONResponse(content = {'state' : "Correcto", 
                                       'msg' : "El usuario ha sido actualizado de forma correcta"
                                       })
    return JSONResponse(content = {'state' : "Incorrecto", 
                                   'msg' : f"El usuario de id {id_user} no ha sido encontrado"
                                   })