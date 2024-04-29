from core import note

class Workspace:
    """
    this class represents a workspace, which is a collection of notes

    parameters:
        id: int
        name: str
        creator: User
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
    
    def __init__(self, id: int, name: str, creator) -> None:
        self.id = id
        self.name = name
        self.creator = creator
        self.list_users = [creator]
        self.list_notes = []

    def add_user(self, user) -> None:
        self.list_users.append(user)
        user.add_workspace(self)

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