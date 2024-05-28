import uvicorn
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


engine = create_engine('postgresql+psycopg2://postgres:postgres@localhost:5432/public')
Session = sessionmaker(bind=engine)
session = Session()

metadata = MetaData()
products = Table('products', metadata,
                 Column('id', Integer, primary_key=True),
                 Column('name', String),
                 Column('description', String))


app = FastAPI()

#added orgins due a cors error
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/hello_ud")
def hello_ud():
    return "Welcome to UD!"

@app.get("/data")
def get_products():
    query = products.select()
    result = session.execute(query)
    products = result.fetchall()
    return products

@app.post("/create_product")
def create_product(name: str, description: str):
    query = products.insert().values(name=name, description=description)
    session.execute(query)
    session.commit()
    return {"message": "Product created successfully"}



# app = FastAPI() deleated this line
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)