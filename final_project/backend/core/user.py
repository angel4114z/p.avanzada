from pydantic import BaseModel
from typing import List
from sqlalchemy import MetaData, Table, Column, Integer, String, JSON
from .db_connection import PostgresConnection
from dotenv import load_dotenv
import os
import json


class User(BaseModel):
    """
    this class is the behavior of the user
    parameters:
        id: int
        name: str
        email: str
        password: str
        list_workspaces: list of dict, dict contains id and name of the workspace

    methods:
        login(email_: str, password_: str) -> bool:
        register(name_: str, email_: str, password_: str) -> None:
        get_users() -> List[User]:
        add_workspace(workspace) -> None:
        remove_workspace(workspace) -> None:
        view_workspaces() -> list:


    """

    id: int | None = None
    name: str
    email: str
    password: str
    list_workspaces: list | None = None

    @staticmethod
    def login(email_: str, password_: str) -> bool:
        """
        this method is used to login the user
        parameters:
            email_: str
            password_: str
        return:
            bool

        """
        for user in User.get_users():
            if user.email == email_ and user.password == password_:
                return True
        return False

    @staticmethod
    def get_users() -> List["User"]:
        """
        this method is used to get all the users
        return:
            List["User"]

        """
        # connect to the database
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
        users = Table(
            "users",
            metadata,
            Column("id", Integer, primary_key=True),
            Column("name", String),
            Column("email", String),
            Column("password", String),
            Column("workspaceslist", JSON, default={}),
        )
        metadata.create_all(connection.engine)

        # get the users from the database
        query = users.select()
        result = session.execute(query)
        users_list = []
        # create a list of users
        for row in result:
            user = User(
                id=row[0],
                name=row[1],
                email=row[2],
                password=row[3],
                list_workspaces=[],
            )
            users_list.append(user)
        session.close()
        return users_list

    @staticmethod
    def register(name_: str, email_: str, password_: str) -> None:
        """
        this method is used to register the user
        parameters:
            name_: str
            email_: str
            password_: str
        """

        # connect to the database
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
        users = Table(
            "users",
            metadata,
            Column("id", Integer, primary_key=True, autoincrement=True),
            Column("name", String),
            Column("email", String),
            Column("password", String),
            Column("workspaceslist", JSON, default={}),
        )
        metadata.create_all(connection.engine)

        # insert the user to the database
        query = users.insert().values(name=name_, email=email_, password=password_)
        session.execute(query)
        session.commit()
        session.close()

    @staticmethod
    def add_workspace(self, workspace) -> None:
        """
        this method is used to add a workspace to the user
        parameters:
            user: User as self, needed to get the user id and name
            workspace: Workspace, needed to get the workspace id and name


        """

        workspace_ = {"id": workspace.id, "name": workspace.name}

        # connect to the database
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
        users = Table(
            "users",
            metadata,
            Column("id", Integer, primary_key=True),
            Column("name", String),
            Column("email", String),
            Column("password", String),
            Column("workspaceslist", JSON, default={}),
        )
        metadata.create_all(connection.engine)
        # get the user from the database
        query = users.select().where(users.c.id == self.id)
        result = session.execute(query).fetchone()

        # add the workspace to the user
        workspacesstr = str(result[4])
        if workspacesstr == "{}":
            workspaces = json.dumps([workspace_])
        else:
            workspaceslist = json.loads(workspacesstr)  # convert to list
            workspaceslist.append(workspace_)
            workspaces = json.dumps(workspaceslist)  # convert to json string

        # update the user in the database
        query = (
            users.update()
            .where(users.c.id == self.id)
            .values(workspaceslist=workspaces)
        )
        session.execute(query)
        session.commit()
        session.close()

    def remove_workspace(self, workspace) -> None:
        """
        this method is used to remove a workspace from the user
        parameters:
            user: User as self, needed to get the user id and name
            workspace: Workspace, needed to get the workspace id and name
        """

        # connect to the database
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
        users = Table(
            "users",
            metadata,
            Column("id", Integer, primary_key=True),
            Column("name", String),
            Column("email", String),
            Column("password", String),
            Column("workspaceslist", JSON, default={}),
        )
        metadata.create_all(connection.engine)
        # get the user from the database
        query = users.select().where(users.c.id == self.id)
        result = session.execute(query).fetchone()
        # remove the workspace from the user
        workspacestr = str(result[4])
        workspace_ = {"id": workspace.id, "name": workspace.name}
        workspaceslist = json.loads(workspacestr)
        workspaceslist.remove(workspace_)
        workspaces = json.dumps(workspaceslist)
        # update the user in the database
        query = (
            users.update()
            .where(users.c.id == self.id)
            .values(workspaceslist=workspaces)
        )
        session.execute(query)
        session.commit()
        session.close()

    def view_workspaces(self) -> list:
        """
        this method is used to view the workspaces of the user
        parameters:
            user: User as self, needed to get the user id and name
        return:
            list of dict, dict contains id and name of the workspace
        """
        # connect to the database
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
        users = Table(
            "users",
            metadata,
            Column("id", Integer, primary_key=True),
            Column("name", String),
            Column("email", String),
            Column("password", String),
            Column("workspaceslist", JSON, default={}),
        )
        metadata.create_all(connection.engine)
        # get the user from the database
        query = users.select().where(users.c.id == self.id)
        result = session.execute(query).fetchone()
        # get the workspaces list of the user
        workspacestr = str(result[4])
        workspaceslist = json.loads(workspacestr)
        return workspaceslist

    class config:
        orm_mode = True