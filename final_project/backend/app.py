from core.user import User, Userdb
from core.note import Note
from core.workspace import Workspace
from fastapi import FastAPI
import uvicorn
from core.db_connection import PostgresConnection


app = FastAPI()

#---------------- USER ----------------

@app.get("/login")
def login(email: str, password: str):
    return User.login(email, password)

@app.post("/register")
def register(name: str, email: str, password: str):
    User.register(name, email, password)
    return "User registered successfully"
    

#---------------- WORKSPACE ----------------

@app.get("/viewWorkspaces")
def view_workspaces():
    pass

@app.post("/createWorkspace")
def create_workspace():
    pass

@app.post("/deleteWorkspace")
def delete_workspace():
    pass

#---------------- edit workspace ----------------

#--------- User ---------

@app.post("/addUser")
def add_user():
    pass

@app.post("/removeUser")
def remove_user():
    pass

#----------- Note -----------

@app.post("/createNote")
def create_note():
    pass

@app.post("/deleteNote")
def delete_note():
    pass

@app.get("/viewNotes")
def view_notes():
    pass

@app.get("/viewNote")
def view_note():
    pass

@app.post("/editNote")
def edit_note():
    pass


#----------------- RUN -----------------

if __name__ == "__main__":


    Userdb.metadata.create_all(bind= PostgresConnection("postgres", "admin12345", "localhost", 5432, "db_test")) #esta mrd no sirve :D
    uvicorn.run(app, host="0.0.0.0", port=8000)