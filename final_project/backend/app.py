from core.user import User
from core.note import Note
from core.workspace import Workspace

user1 = User(1, "angel", "angel@email.com", "password")
note1 = Note(1, "note1", "this is the first note", "angel")
note2 = Note(2, "note2", "this is the second note", "angel")
workspace1 = Workspace(1, "workspace1", "angel")
workspace2 = Workspace(1, "workspace2", "angel")
workspace1.add_note(note1)
workspace1.add_note(note2)
workspace2.add_note(note1)
user1.add_workspace(workspace1)
user1.add_workspace(workspace2)


print(user1.view_workspaces())
print(user1.list_workspaces[0].view_notes())
print(user1.list_workspaces[0].list_notes[0].view_note())   