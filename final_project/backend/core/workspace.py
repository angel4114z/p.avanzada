from .note import Note
from pydantic import BaseModel
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
        creator: dict (id and name)
        list_users: list of dict (id and name)
        list_notes: list of dict (id and title)

    methods:
        create_workspace(name: str, creator: dict) -> None
        delete_workspace(workspace) -> None
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
    list_users: list | None = None
    list_notes: list | None = None

    @staticmethod
    def create_workspace(name: str, creator: dict) -> int:
        """
        this method is used to create a workspace
        parameters:
            name: str
            creator: dict
        """
        # connection to the database
        load_dotenv()
        connection = PostgresConnection(
            os.getenv("DB_USER"),
            os.getenv("DB_PASSWORD"),
            os.getenv("DB_HOST"),
            os.getenv("DB_PORT"),
            os.getenv("DB_NAME"),
        )
        session = connection.session()

        metadata = MetaData()
        workspaces = Table(
            "workspaces",
            metadata,
            Column("id", Integer, primary_key=True),
            Column("name", String),
            Column("creator", JSON, default={}),
            Column("userslist", JSON, default={}),
            Column("noteslist", JSON, default={}),
        )
        metadata.create_all(connection.engine)
        # insert the workspace into the database
        creator = json.dumps([creator])
        query = workspaces.insert().values(
            name=name, creator=creator, userslist=creator
        )
        session.execute(query)
        result = session.execute(workspaces.select().where(workspaces.c.name == name))
        workspace = result.fetchone()
        id_ = workspace[0]
        session.commit()
        session.close()
        return id_

    @staticmethod
    def delete_workspace(workspace) -> None:
        """
        this method is used to delete a workspace
        parameters:
            workspace: Workspace, needed to get the workspace id
        """
        # connection to the database
        load_dotenv()
        connection = PostgresConnection(
            os.getenv("DB_USER"),
            os.getenv("DB_PASSWORD"),
            os.getenv("DB_HOST"),
            os.getenv("DB_PORT"),
            os.getenv("DB_NAME"),
        )
        session = connection.session()
        metadata = MetaData()
        workspaces = Table(
            "workspaces",
            metadata,
            Column("id", Integer, primary_key=True),
            Column("name", String),
            Column("creator", JSON, default={}),
            Column("userslist", JSON, default={}),
            Column("noteslist", JSON, default={}),
        )
        metadata.create_all(connection.engine)
        # delete the workspace from the database
        query = workspaces.delete().where(workspaces.c.id == workspace.id)
        session.execute(query)
        session.commit()
        session.close()

    def add_user(workspace, user) -> None:
        """
        this method is used to add a user to the workspace
        parameters:
            workspace: Workspace, needed to get the workspace id
            user: User, needed to get the user id and name
        """
        # connection to the database
        load_dotenv()
        connection = PostgresConnection(
            os.getenv("DB_USER"),
            os.getenv("DB_PASSWORD"),
            os.getenv("DB_HOST"),
            os.getenv("DB_PORT"),
            os.getenv("DB_NAME"),
        )
        session = connection.session()
        metadata = MetaData()
        workspaces = Table(
            "workspaces",
            metadata,
            Column("id", Integer, primary_key=True),
            Column("name", String),
            Column("creator", JSON, default={}),
            Column("userslist", JSON, default={}),
            Column("noteslist", JSON, default={}),
        )
        metadata.create_all(connection.engine)
        # get the workspace from the database
        query = workspaces.select().where(workspaces.c.id == workspace.id)
        result = session.execute(query).fetchone()
        # add the user to the workspace
        userstr = str(result[3])
        user_ = {"id": user.id, "name": user.name}
        if userstr == "{}":
            users = json.dumps([user_])
        else:
            userlist = json.loads(userstr)
            userlist.append(user_)
            users = json.dumps(userlist)
        query = (
            workspaces.update()
            .where(workspaces.c.id == workspace.id)
            .values(userslist=users)
        )
        session.execute(query)
        session.commit()
        session.close()

    def remove_user(self, user) -> None:
        """
        this method is used to remove a user from the workspace
        parameters:
            user: User, needed to get the user id and name
            workspace as self, needed to get the workspace id
        """
        # connection to the database
        load_dotenv()
        connection = PostgresConnection(
            os.getenv("DB_USER"),
            os.getenv("DB_PASSWORD"),
            os.getenv("DB_HOST"),
            os.getenv("DB_PORT"),
            os.getenv("DB_NAME"),
        )
        session = connection.session()
        metadata = MetaData()
        workspaces = Table(
            "workspaces",
            metadata,
            Column("id", Integer, primary_key=True),
            Column("name", String),
            Column("creator", JSON, default={}),
            Column("userslist", JSON, default={}),
            Column("noteslist", JSON, default={}),
        )
        metadata.create_all(connection.engine)
        # get the workspace from the database
        query = workspaces.select().where(workspaces.c.id == self.id)
        result = session.execute(query).fetchone()
        # remove the user from the workspace
        userstr = str(result[3])
        user_ = {"id": user.id, "name": user.name}
        userlist = json.loads(userstr)
        userlist.remove(user_)
        users = json.dumps(userlist)
        # update the workspace in the database
        query = (
            workspaces.update()
            .where(workspaces.c.id == self.id)
            .values(userslist=users)
        )
        session.execute(query)
        session.commit()
        session.close()

    def view_users(self) -> list:
        """
        this method is used to view the users in the workspace
        return:
            list of dict (id and name)
        """
        # connection to the database
        load_dotenv()
        connection = PostgresConnection(
            os.getenv("DB_USER"),
            os.getenv("DB_PASSWORD"),
            os.getenv("DB_HOST"),
            os.getenv("DB_PORT"),
            os.getenv("DB_NAME"),
        )
        session = connection.session()
        metadata = MetaData()
        workspaces = Table(
            "workspaces",
            metadata,
            Column("id", Integer, primary_key=True),
            Column("name", String),
            Column("creator", JSON, default={}),
            Column("userslist", JSON, default={}),
            Column("noteslist", JSON, default={}),
        )
        metadata.create_all(connection.engine)
        # get the workspace from the database
        query = workspaces.select().where(workspaces.c.id == self.id)
        result = session.execute(query).fetchone()
        # get the users from the workspace
        userstr = str(result[3])
        users = json.loads(userstr)
        return users

    def create_note(self, note: Note) -> None:
        """
        this method is used to create a note in the workspace
        parameters:
            note: Note
        """
        # create the note
        note.id = Note.create_note(note.title, note.content)
        # connection to the database
        load_dotenv()
        connection = PostgresConnection(
            os.getenv("DB_USER"),
            os.getenv("DB_PASSWORD"),
            os.getenv("DB_HOST"),
            os.getenv("DB_PORT"),
            os.getenv("DB_NAME"),
        )
        session = connection.session()
        metadata = MetaData()
        workspaces = Table(
            "workspaces",
            metadata,
            Column("id", Integer, primary_key=True),
            Column("name", String),
            Column("creator", JSON, default={}),
            Column("userslist", JSON, default={}),
            Column("noteslist", JSON, default={}),
        )
        # get the workspace from the database
        metadata.create_all(connection.engine)
        query = workspaces.select().where(workspaces.c.id == self.id)
        result = session.execute(query).fetchone()
        # add the note to the workspace
        note_ = {"id": note.id, "title": note.title}
        notesstr = str(result[4])
        if notesstr == "{}":
            notes = json.dumps([note_])
        else:
            noteslist = json.loads(notesstr)
            noteslist.append(note_)
            notes = json.dumps(noteslist)
        # update the workspace in the database
        query = (
            workspaces.update()
            .where(workspaces.c.id == self.id)
            .values(noteslist=notes)
        )
        session.execute(query)
        session.commit()
        session.close()

    def delete_note(self, note: Note) -> None:
        """
        this method is used to delete a note from the workspace
        parameters:
            note: Note, needed to get the note id and title
        """
        # delete the note
        Note.delete_note({"id": note.id, "title": note.title})
        # connection to the database
        load_dotenv()
        connection = PostgresConnection(
            os.getenv("DB_USER"),
            os.getenv("DB_PASSWORD"),
            os.getenv("DB_HOST"),
            os.getenv("DB_PORT"),
            os.getenv("DB_NAME"),
        )
        session = connection.session()
        metadata = MetaData()
        workspaces = Table(
            "workspaces",
            metadata,
            Column("id", Integer, primary_key=True),
            Column("name", String),
            Column("creator", JSON, default={}),
            Column("userslist", JSON, default={}),
            Column("noteslist", JSON, default={}),
        )
        metadata.create_all(connection.engine)
        # get the workspace from the database
        query = workspaces.select().where(workspaces.c.id == self.id)
        result = session.execute(query).fetchone()
        # remove the note from the workspace
        notesstr = str(result[4])
        note_ = {"id": note.id, "title": note.title}
        noteslist = json.loads(notesstr)
        noteslist.remove(note_)
        notes = json.dumps(noteslist)
        # update the workspace in the database
        query = (
            workspaces.update()
            .where(workspaces.c.id == self.id)
            .values(noteslist=notes)
        )
        session.execute(query)
        session.commit()
        session.close()

    def view_notes(self) -> list:
        """
        this method is used to view the notes in the workspace
        return:
            list of dict (id and title)
        """
        # connection to the database
        load_dotenv()
        connection = PostgresConnection(
            os.getenv("DB_USER"),
            os.getenv("DB_PASSWORD"),
            os.getenv("DB_HOST"),
            os.getenv("DB_PORT"),
            os.getenv("DB_NAME"),
        )
        session = connection.session()
        metadata = MetaData()
        workspaces = Table(
            "workspaces",
            metadata,
            Column("id", Integer, primary_key=True),
            Column("name", String),
            Column("creator", JSON, default={}),
            Column("userslist", JSON, default={}),
            Column("noteslist", JSON, default={}),
        )
        metadata.create_all(connection.engine)
        # get the workspace from the database
        query = workspaces.select().where(workspaces.c.id == self.id)
        result = session.execute(query).fetchone()
        # get the notes from the workspace
        notesstr = str(result[4])
        notes = json.loads(notesstr)
        return notes

    def edit_note(self, note: Note, new_content: Note) -> None:
        """
        this method is used to edit a note in the workspace
        parameters:
            note: Note, needed to get the note id and title
            new_content: Note, needed to get the new title and content
        """
        # edit the note content
        note.edit_content(new_content.content)
        # comprove if the title has changed
        if note.title != new_content.title:
            # edit the note title
            oldnote = {"id": note.id, "title": note.title}
            note.edit_title(new_content.title)
            # connection to the database
            load_dotenv()
            connection = PostgresConnection(
                os.getenv("DB_USER"),
                os.getenv("DB_PASSWORD"),
                os.getenv("DB_HOST"),
                os.getenv("DB_PORT"),
                os.getenv("DB_NAME"),
            )
            session = connection.session()
            metadata = MetaData()
            workspaces = Table(
                "workspaces",
                metadata,
                Column("id", Integer, primary_key=True),
                Column("name", String),
                Column("creator", JSON, default={}),
                Column("userslist", JSON, default={}),
                Column("noteslist", JSON, default={}),
            )
            metadata.create_all(connection.engine)
            # get the workspace from the database
            query = workspaces.select().where(workspaces.c.id == self.id)
            result = session.execute(query).fetchone()
            # edit the note in the workspace
            notesstr = str(result[4])
            note_ = {"id": note.id, "title": new_content.title}
            noteslist = json.loads(notesstr)
            noteslist.remove(oldnote)
            noteslist.append(note_)
            notes = json.dumps(noteslist)
            # update the workspace in the database
            query = (
                workspaces.update()
                .where(workspaces.c.id == self.id)
                .values(noteslist=notes)
            )
            session.execute(query)
            session.commit()
            session.close()

    class config:
        orm_mode = True