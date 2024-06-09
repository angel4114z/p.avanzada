from core.user import User
from core.note import Note
from core.workspace import Workspace
from fastapi import FastAPI
import uvicorn
from core.db_connection import PostgresConnection


app = FastAPI()

#---------------- USER ----------------

@app.get("/login")
def login(user: User):
    return User.login(user.email, user.password)

@app.post("/register")
def register(user: User):
    User.register(user.name, user.email, user.password)
    return "User registered successfully"

@app.delete("/user/deleteWorkspace")
def remove_workspace(user: User, workspace: Workspace):
    user.remove_workspace(workspace)
    
@app.get("/user/viewWorkspaces")
def view_workspaces(user : User):
    return user.view_workspaces()

#---------------- WORKSPACE ----------------#


@app.post("/createWorkspace")
def create_workspace(workspace: Workspace):
    Workspace.create_workspace(workspace.name, workspace.creator)
    user = User(id=workspace.creator["id"], name=workspace.creator["name"], email="", password="", list_workspaces=[])
    user.add_workspace(user, workspace)
    return "Workspace created successfully"

@app.delete("/deleteWorkspace")
def remove_workspace(workspace: Workspace):
    Workspace.delete_workspace(workspace)
    

#---------------- edit workspace ----------------#

#--------- User ---------#

@app.put("/workspace/addUser")
def add_user(workspace: Workspace, user: User):
    Workspace.add_user(workspace, user)
    user.add_workspace(user, workspace)

@app.put("/workspace/removeUser")
def remove_user(workspace: Workspace, user: User):
    workspace.remove_user(user)
    user.remove_workspace(workspace)

@app.get("/workspace/viewUsers")
def view_users(workspace: Workspace):
    return workspace.view_users()

#----------- Note -----------

@app.post("/workspace/createNote")
def create_note(note: Note, workspace: Workspace):
    Workspace.create_note(workspace, note)

@app.delete("/workspace/deleteNote")
def delete_note(note: Note, workspace: Workspace):
    Workspace.delete_note(workspace, note) #hay que pasar bien el id de la nota, el error ya esta en workspace.py, pero si quita la nota de la lista

@app.get("/workspace/viewNotes")
def view_notes(workspace: Workspace):
    return workspace.view_notes()

@app.get("/workspace/viewNote")
def view_note(workspace: Workspace, note: Note):
    workspace.view_note(note) # TypeError: Note.view_note() takes 2 positional arguments but 3 were given #esta ese error

@app.put("/workspace/editNote")
def edit_note(workspace: Workspace, note: Note, new_note: Note):
    workspace.edit_note(note, new_note) #TypeError: Note.edit_title() takes 2 positional arguments but 3 were given, otra vez xd
    


#----------------- RUN -----------------

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)