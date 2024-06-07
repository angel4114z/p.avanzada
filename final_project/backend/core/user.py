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
    def login(email_: str, password_: str) -> bool:
        for user in User.get_users():
            if user.email == email_ and user.password == password_:
                return True
        return False
    
    @staticmethod
    def get_users() -> List["User"]:
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

        query = users.select()
        result = session.execute(query)
        users_list = []
        for row in result:
            user = User(id=row[0], name=row[1], email=row[2], password=row[3], list_workspaces=[])
            users_list.append(user)
        session.close()
        return users_list

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
    

