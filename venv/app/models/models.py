from sqlmodel import SQLModel, Field, Relationship

class UserBase(SQLModel):
    nombre : str
    edad : int
    rol : str

class User(UserBase, table = True):
    id : int | None = Field(None, primary_key=True)
    tasks : list['Task'] = Relationship(back_populates="user")

class TaskBase(SQLModel):
    title : str
    duration: int
    overview: str
    user_id : int = Field(foreign_key="user.id")
    
class Task(TaskBase, table=True):
    id : int|None = Field(None, primary_key=True)
    user : User = Relationship(back_populates="tasks")
    