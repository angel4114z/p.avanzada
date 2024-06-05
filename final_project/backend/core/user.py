from pydantic import BaseModel
from typing import List, Dict
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from .db_connection import PostgresConnection


class User(BaseModel):
    """
    this class is teh behavior of the user
    parameters:
        id: int
        name: str
        email: str
        password: str
        list_workspaces: list of dictionaries

    methods:
        __init__(id: int, name: str, email: str, password: str) -> None
        add_workspace(workspace: Workspace) -> None
        remove_workspace(workspace: Workspace) -> None
    """
    id: int
    name: str
    email: str
    password: str
    list_workspaces: List[Dict[str, int]]

    #def __init__(self, id: int, name: str, email: str, password: str) -> None:
    #    self.id = id
    #    self.name = name
    #    self.email = email
    #    self.password = password
    #    self.list_workspaces = []

    @staticmethod
    def login(self, email: str, password: str) -> bool:
        if email == self.email and password == self.password:
            return True
        return False

    @staticmethod
    def register(name: str, email: str, password: str) -> None:
        
        

        connection = PostgresConnection("postgres", "admin12345", "localhost", 5432, "db_test")
        session = connection.session()
        user_db = Userdb(
                id=1,
                name=name,
                email=email,
                password=password
                )
        session.add(user_db)
        session.commit()
        session.close()


    def add_workspace(self, workspace) -> None:
        workspace_ = {"name": workspace.name, "id": workspace.id}
        self.list_workspaces.append(workspace_)

    def remove_workspace(self, workspace) -> None:
        self.list_workspaces.remove(workspace)

    def view_workspaces(self) -> list:
        return self.list_workspaces
    
    class config:
        orm_mode = True
    

Base = declarative_base()

class Userdb(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    password = Column(String)
    list_workspaces = Column(String)
