from pydantic import BaseModel
from typing import List, Dict
from sqlalchemy import MetaData, Table, Column, Integer, String, JSON
from .db_connection import PostgresConnection
from dotenv import load_dotenv
import os
import json


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
    list_workspaces: list | None = None


    @staticmethod
    def login(email_: str, password_: str) -> bool:
        for user in User.get_users():
            if user.email == email_ and user.password == password_:
                return True
        return False
    
    @staticmethod
    def get_users() -> List["User"]:
        load_dotenv()
        connection = PostgresConnection(os.getenv("DB_USER"), os.getenv("DB_PASSWORD"), os.getenv("DB_HOST"), os.getenv("DB_PORT"), os.getenv("DB_NAME"))
        session = connection.session()

        metadata = MetaData()
        users = Table('users', metadata,
            Column('id', Integer, primary_key=True),
            Column('name', String),
            Column('email', String),
            Column('password', String),
            Column('workspaceslist', JSON, default={})
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
        
        load_dotenv()
        connection = PostgresConnection(os.getenv("DB_USER"), os.getenv("DB_PASSWORD"), os.getenv("DB_HOST"), os.getenv("DB_PORT"), os.getenv("DB_NAME"))
        session = connection.session()

        metadata = MetaData()
        users = Table('users', metadata,
            Column('id', Integer, primary_key=True),
            Column('name', String),
            Column('email', String),
            Column('password', String),
            Column('workspaceslist', JSON, default={})
        )
        metadata.create_all(connection.engine)


        query = users.insert().values(name=name_, email=email_, password=password_)
        session.execute(query)
        session.commit()
        session.close()

    @staticmethod
    def add_workspace(self, workspace) -> None:
        workspace_ = {"id": workspace.id, "name": workspace.name}
        
        load_dotenv()
        connection = PostgresConnection(os.getenv("DB_USER"), os.getenv("DB_PASSWORD"), os.getenv("DB_HOST"), os.getenv("DB_PORT"), os.getenv("DB_NAME"))
        session = connection.session()
        metadata = MetaData()
        users = Table('users', metadata,
            Column('id', Integer, primary_key=True),
            Column('name', String),
            Column('email', String),
            Column('password', String),
            Column('workspaceslist', JSON, default={})
        )
        metadata.create_all(connection.engine)
        query = users.select().where(users.c.id == self.id)
        result = session.execute(query).fetchone()


        workspacesstr = str(result[4])
        if workspacesstr == "{}":
            workspaces = json.dumps([workspace_])
        else:
            workspaceslist = json.loads(workspacesstr) #convert to list
            workspaceslist.append(workspace_)
            workspaces = json.dumps(workspaceslist) #convert to json string

        query = users.update().where(users.c.id == self.id).values(workspaceslist=workspaces)
        session.execute(query)
        session.commit()
        session.close()

    def remove_workspace(self, workspace) -> None:
        load_dotenv()
        connection = PostgresConnection(os.getenv("DB_USER"), os.getenv("DB_PASSWORD"), os.getenv("DB_HOST"), os.getenv("DB_PORT"), os.getenv("DB_NAME"))  
        session = connection.session()
        metadata = MetaData()
        users = Table('users', metadata,
            Column('id', Integer, primary_key=True),
            Column('name', String),
            Column('email', String),
            Column('password', String),
            Column('workspaceslist', JSON, default={})
        )
        metadata.create_all(connection.engine)
        query = users.select().where(users.c.id == self.id)
        result = session.execute(query).fetchone()
        
        workspacestr = str(result[4])

        workspace_ = {"id": workspace.id, "name": workspace.name}
        workspaceslist = json.loads(workspacestr)
        workspaceslist.remove(workspace_)
        workspaces = json.dumps(workspaceslist)
            
        query = users.update().where(users.c.id == self.id).values(workspaceslist=workspaces)
        session.execute(query)
        session.commit()
        session.close()

    def view_workspaces(self) -> list:
        
        load_dotenv()
        connection = PostgresConnection(os.getenv("DB_USER"), os.getenv("DB_PASSWORD"), os.getenv("DB_HOST"), os.getenv("DB_PORT"), os.getenv("DB_NAME"))
        session = connection.session()
        metadata = MetaData()
        users = Table('users', metadata,
            Column('id', Integer, primary_key=True),
            Column('name', String),
            Column('email', String),
            Column('password', String),
            Column('workspaceslist', JSON, default={})
        )
        metadata.create_all(connection.engine)
        query = users.select().where(users.c.id == self.id)
        result = session.execute(query).fetchone()
        
        workspacestr = str(result[4])
        workspaceslist = json.loads(workspacestr)
        return workspaceslist
    
    class config:
        orm_mode = True