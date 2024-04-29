class Note:
    """
    this class represents a note

    parameters:
        id: int
        title: str
        content: str
        creator: User

    methods:
        __init__(id: int, title: str, content: str, creator: User) -> None
        edit_title(new_title: str) -> None
        edit_content(new_content: str) -> None
        view_note() -> str
        #view_title() -> str
        #view_content() -> str
    """
    def __init__(self, id: int, title: str, content: str, creator: str) -> None:
        self.id = id
        self.title = title
        self.content = content
        self.creator = creator

    def edit_title(self, new_title: str) -> None:
        self.title = new_title

    def edit_content(self, new_content: str) -> None:
        self.content = new_content

    def view_note(self) -> str:
        return self.title + "\n" + self.content

    def view_title(self) -> str:
        return self.title

    def view_content(self) -> str:
        return self.content