from pydantic import BaseModel
from typing import List, Dict
from sqlalchemy import MetaData, Table, Column, Integer, String, JSON
from .db_connection import PostgresConnection
from dotenv import load_dotenv
import os
import json

class Note(BaseModel):
    """
    this class represents a note

    parameters:
        id: int
        title: str
        content: str

    methods:
        __init__(id: int, title: str, content: str) -> None
        edit_title(new_title: str) -> None
        edit_content(new_content: str) -> None
        view_note() -> str
        #view_title() -> str
        #view_content() -> str
    """

    id: int
    title: str
    content: str

    #def __init__(self, id: int, title: str, content: str, creator: str) -> None:
    #    self.id = id
    #    self.title = title
    #    self.content = content

    @staticmethod
    def create_note(title_: str, content_: str) -> int:

        load_dotenv()
        connection = PostgresConnection(os.getenv("DB_USER"), os.getenv("DB_PASSWORD"), os.getenv("DB_HOST"), os.getenv("DB_PORT"), os.getenv("DB_NAME"))
        session = connection.session()

        metadata = MetaData()
        notes = Table('notes', metadata,
            Column('id', Integer, primary_key=True, autoincrement=True),
            Column('title', String),
            Column('content', String)
        )
        metadata.create_all(connection.engine)

        query = notes.insert().values(title=title_, content=content_)
        session.execute(query)
        query = notes.select().where(notes.c.title == title_)
        result = session.execute(query).fetchone()
        id_ = result[0]
        session.commit()
        session.close()
        return id_

    @staticmethod
    def delete_note(note_) -> None:
        load_dotenv()
        connection = PostgresConnection(os.getenv("DB_USER"), os.getenv("DB_PASSWORD"), os.getenv("DB_HOST"), os.getenv("DB_PORT"), os.getenv("DB_NAME"))
        session = connection.session()

        metadata = MetaData()
        notes = Table('notes', metadata,
            Column('id', Integer, primary_key=True),
            Column('title', String),
            Column('content', String)
        )
        metadata.create_all(connection.engine)

        query = notes.delete().where(notes.c.id == note_["id"]).where(notes.c.title == note_["title"])
        session.execute(query)
        session.commit()
        session.close()
    

    def edit_title(self, new_title: str) -> None:

            load_dotenv()
            connection = PostgresConnection(os.getenv("DB_USER"), os.getenv("DB_PASSWORD"), os.getenv("DB_HOST"), os.getenv("DB_PORT"), os.getenv("DB_NAME"))
            session = connection.session()

            metadata = MetaData()
            notes = Table('notes', metadata,
                Column('id', Integer, primary_key=True),
                Column('title', String),
                Column('content', String)
            )
            metadata.create_all(connection.engine)

            query = notes.update().where(notes.c.id == self.id).values(title=new_title)
            session.execute(query)
            session.commit()
            session.close()

    def edit_content(self, new_content: str) -> None:
        load_dotenv()
        connection = PostgresConnection(os.getenv("DB_USER"), os.getenv("DB_PASSWORD"), os.getenv("DB_HOST"), os.getenv("DB_PORT"), os.getenv("DB_NAME"))
        session = connection.session()

        metadata = MetaData()
        notes = Table('notes', metadata,
            Column('id', Integer, primary_key=True),
            Column('title', String),
            Column('content', String)
        )
        metadata.create_all(connection.engine)

        query = notes.update().where(notes.c.id == self.id).values(content=new_content)
        session.execute(query)
        session.commit()
        session.close()

    def view_note(self) -> dict:
        load_dotenv()
        connection = PostgresConnection(os.getenv("DB_USER"), os.getenv("DB_PASSWORD"), os.getenv("DB_HOST"), os.getenv("DB_PORT"), os.getenv("DB_NAME"))
        session = connection.session()

        metadata = MetaData()
        notes = Table('notes', metadata,
            Column('id', Integer, primary_key=True),
            Column('title', String),
            Column('content', String)
        )
        metadata.create_all(connection.engine)

        query = notes.select().where(notes.c.id == self.id).where(notes.c.title == self.title)
        result = session.execute(query).fetchone()
        session.close()
        note_ = {"id": result[0], "title": result[1], "content": result[2]}
        return note_
        