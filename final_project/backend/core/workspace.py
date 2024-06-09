from .note import Note
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

        creator = json.dumps([creator])

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
        print(userstr)

        user_ = {"id": user.id, "name": user.name}

        if userstr == "{}":
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
        session.close()

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
        result = session.execute(query).fetchone()
        userstr = str(result[3])
        users = json.loads(userstr)
        return users

    def create_note(self, note: Note) -> None:

        Note.create_note(note.title, note.content) 

        #en algun lado de aqui el id de la nota se pierde y no se guarda en la lista, pero en la base de datos si se guarda

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
        note_ = {"id": note.id, "title": note.title}
        notesstr = str(result[4])
        if notesstr == "{}":
            notes = json.dumps([note_])
        else:
            noteslist = json.loads(notesstr)
            noteslist.append(note_)
            notes = json.dumps(noteslist)
        query = workspaces.update().where(workspaces.c.id == self.id).values(noteslist=notes)
        session.execute(query)
        session.commit()
        session.close()

    def delete_note(self, note: Note) -> None:

        Note.delete_note({"id": note.id, "title": note.title})

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
        notesstr = str(result[4])
        note_ = {"id": note.id, "title": note.title}
        noteslist = json.loads(notesstr)
        noteslist.remove(note_)
        notes = json.dumps(noteslist)
        query = workspaces.update().where(workspaces.c.id == self.id).values(noteslist=notes)
        session.execute(query)
        session.commit()
        session.close()

    def view_notes(self) -> list:
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
        notesstr = str(result[4])
        notes = json.loads(notesstr)
        return notes

    def edit_note(self, note: Note, new_content: Note) -> None:

        note.edit_content(note, new_content)

        if note.title != new_content.title:
            oldnote = {"id": note.id, "title": note.title}
            note.edit_title(note, new_content.title)

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
            notesstr = str(result[4])
            note_ = {"id": note.id, "title": note.title}
            noteslist = json.loads(notesstr)
            noteslist.remove(oldnote)
            noteslist.append(note_)
            notes = json.dumps(noteslist)
            query = workspaces.update().where(workspaces.c.id == self.id).values(noteslist=notes)
            session.execute(query)
            session.commit()
            session.close()

    def view_note(self, note: Note) -> dict:
        return note.view_note(note.id, note.title)
    
    class config:
        orm_mode = True