from pydantic import BaseModel
from typing import List, Dict
from sqlalchemy import MetaData, Table, Column, Integer, String
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
    id: int | None = None
    name: str
    email: str
    password: str
    list_workspaces: List[Dict[str, int]]  | None = None


    @staticmethod
    def login(self, email: str, password: str) -> bool:
        if email == self.email and password == self.password:
            return True
        return False

    @staticmethod
    def register(name_: str, email_: str, password_: str) -> None:
        
        connection = PostgresConnection("postgres", "admin12345", "localhost", 5432, "db_test")
        session = connection.session()

        metadata = MetaData()
        users = Table('users', metadata,
            Column('id', Integer, primary_key=True),
            Column('name', String),
            Column('email', String),
            Column('password', String),
            Column('workspaceslist', String, default="")
        )
        metadata.create_all(connection.engine)


        query = users.insert().values(name=name_, email=email_, password=password_)
        session.execute(query)
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
    

