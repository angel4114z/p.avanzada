from core import note
from pydantic import BaseModel
from typing import List, Dict
from sqlalchemy import MetaData, Table, Column, Integer, String, JSON
from .db_connection import PostgresConnection
from dotenv import load_dotenv
import os
import json

class Workspace(BaseModel):
    """
    this class represents a workspace, which is a collection of notes

    parameters:
        id: int
        name: str
        creator: dict{User}
        list_users: list
        list_notes: list

    methods:
        __init__(id: int, name: str, creator: User) -> None
        add_user(user: User) -> None
        remove_user(user: User) -> None
        view_users() -> list
        add_note(note: Note) -> None
        remove_note(note: Note) -> None
        view_notes() -> list
    """
    
    id: int
    name: str
    creator: dict
    list_users: list | None = None #list[User]
    list_notes: list | None = None #list[note.Note]

    #def __init__(self, id: int, name: str, creator) -> None:
    #    self.id = id
    #    self.name = name
    #    self.creator = creator
    #    self.list_users = [creator]
    #    self.list_notes = []

    @staticmethod
    def create_workspace(name: str, creator: dict):
        load_dotenv()
        connection = PostgresConnection(os.getenv("DB_USER"), os.getenv("DB_PASSWORD"), os.getenv("DB_HOST"), os.getenv("DB_PORT"), os.getenv("DB_NAME"))
        session = connection.session()

        metadata = MetaData()
        workspaces = Table('workspaces', metadata,
            Column('id', Integer, primary_key=True),
            Column('name', String),
            Column('creator', JSON, default={}),
            Column('userslist', JSON, default={}),
            Column('noteslist', JSON, default={})
        )
        metadata.create_all(connection.engine)

        query = workspaces.insert().values(name=name, creator=creator, userslist=creator)
        session.execute(query)
        session.commit()
        session.close()

    @staticmethod
    def delete_workspace(workspace) -> None:
        load_dotenv()
        connection = PostgresConnection(os.getenv("DB_USER"), os.getenv("DB_PASSWORD"), os.getenv("DB_HOST"), os.getenv("DB_PORT"), os.getenv("DB_NAME"))
        session = connection.session()
        metadata = MetaData()
        workspaces = Table('workspaces', metadata,
            Column('id', Integer, primary_key=True),
            Column('name', String),
            Column('creator', JSON, default={}),
            Column('userslist', JSON, default={}),
            Column('noteslist', JSON, default={})
        )
        metadata.create_all(connection.engine)
        query = workspaces.delete().where(workspaces.c.id == workspace.id)
        session.execute(query)
        session.commit()
        session.close()


    def add_user(workspace, user) -> None:
        
        load_dotenv()
        connection = PostgresConnection(os.getenv("DB_USER"), os.getenv("DB_PASSWORD"), os.getenv("DB_HOST"), os.getenv("DB_PORT"), os.getenv("DB_NAME"))
        session = connection.session()
        metadata = MetaData()
        workspaces = Table('workspaces', metadata,
            Column('id', Integer, primary_key=True),
            Column('name', String),
            Column('creator', JSON, default={}),
            Column('userslist', JSON, default={}),
            Column('noteslist', JSON, default={})
        )
        metadata.create_all(connection.engine)
        query = workspaces.select().where(workspaces.c.id == workspace.id)
        result = session.execute(query).fetchone()

        userstr = str(result[3])
        user_ = {"id": user.id, "name": user.name}

        if users == "{}":
            users = json.dumps([user_])
        else:
            userlist = json.loads(userstr)
            userlist.append(user_)
            users = json.dumps(userlist)
        
        query = workspaces.update().where(workspaces.c.id == workspace.id).values(userslist=users)
        session.execute(query)
        session.commit()
        session.close()


    def remove_user(self, user) -> None:
        load_dotenv()
        connection = PostgresConnection(os.getenv("DB_USER"), os.getenv("DB_PASSWORD"), os.getenv("DB_HOST"), os.getenv("DB_PORT"), os.getenv("DB_NAME"))
        session = connection.session()
        metadata = MetaData()
        workspaces = Table('workspaces', metadata,
            Column('id', Integer, primary_key=True),
            Column('name', String),
            Column('creator', JSON, default={}),
            Column('userslist', JSON, default={}),
            Column('noteslist', JSON, default={})
        )
        metadata.create_all(connection.engine)
        query = workspaces.select().where(workspaces.c.id == self.id)
        result = session.execute(query).fetchone()

        userstr = str(result[3])
        user_ = {"id": user.id, "name": user.name}
        
        userlist = json.loads(userstr)
        userlist.remove(user_)
        users = json.dumps(userlist)
        
        query = workspaces.update().where(workspaces.c.id == self.id).values(userslist=users)
        session.execute(query)
        session.commit()
        session.close() # hacer postman

    def view_users(self) -> list:
        load_dotenv()
        connection = PostgresConnection(os.getenv("DB_USER"), os.getenv("DB_PASSWORD"), os.getenv("DB_HOST"), os.getenv("DB_PORT"), os.getenv("DB_NAME"))
        session = connection.session()
        metadata = MetaData()
        workspaces = Table('workspaces', metadata,
            Column('id', Integer, primary_key=True),
            Column('name', String),
            Column('creator', JSON, default={}),
            Column('userslist', JSON, default={}),
            Column('noteslist', JSON, default={})
        )
        metadata.create_all(connection.engine)
        query = workspaces.select().where(workspaces.c.id == self.id)
        result = session.execute(query)
        for row in result:
            userlist = row[3]
            users = json.loads(userlist)
        return users # hacer postman

    def add_note(self, note: note.Note) -> None:
        self.list_notes.append(note)

    def remove_note(self, note: note.Note) -> None:
        self.list_notes.remove(note)

    def view_notes(self) -> list:
        for note in self.list_notes:
            print(note.view_title())
        return self.list_notes
    
    class config:
        orm_mode = True