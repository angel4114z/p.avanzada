
class User:
    """
    this class is teh behavior of the user

    parameters:
        id: int
        name: str
        email: str
        password: str
        list_workspaces: list

    methods:
        __init__(id: int, name: str, email: str, password: str) -> None
        add_workspace(workspace: Workspace) -> None
        remove_workspace(workspace: Workspace) -> None
    """

    def __init__(self, id: int, name: str, email: str, password: str) -> None:
        self.id = id
        self.name = name
        self.email = email
        self.password = password
        self.list_workspaces = []

    def add_workspace(self, workspace) -> None:
        self.list_workspaces.append(workspace)

    def remove_workspace(self, workspace) -> None:
        self.list_workspaces.remove(workspace)

    def view_workspaces(self) -> list:
        return self.list_workspaces