from core import note
from pydantic import BaseModel
from typing import List, Dict
from sqlalchemy import MetaData, Table, Column, Integer, String
from .db_connection import PostgresConnection
from dotenv import load_dotenv
import os

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
    creator: str #dict
    list_users: str #list
    list_notes: str #list[note.Note]

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
            Column('creator', String),
            Column('userslist', String, default=""),
            Column('noteslist', String, default="")
        )
        metadata.create_all(connection.engine)

        query = workspaces.insert().values(name=name, creator=creator, userslist=creator)
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
            Column('creator', String),
            Column('userslist', String, default=""),
            Column('noteslist', String, default="")
        )
        metadata.create_all(connection.engine)
        query = workspaces.select().where(workspaces.c.id == workspace.id)
        result = session.execute(query)

        for row in result:
            
            users = row[3]
            users = users + ", { 'id': " + f"{user.id}" + ", 'name': '" + user.name + "'}"

            query = workspaces.update().where(workspaces.c.id == workspace.id).values(userslist=users)
            session.execute(query)
            session.commit()
            session.close()


    def remove_user(self, user) -> None:
        self.list_users.remove(user)
        user.remove_workspace(self)

    def view_users(self) -> list:
        return self.list_users

    def add_note(self, note: note.Note) -> None:
        self.list_notes.append(note)

    def remove_note(self, note: note.Note) -> None:
        self.list_notes.remove(note)

    def view_notes(self) -> list:
        for note in self.list_notes:
            print(note.view_title())
        return self.list_notes