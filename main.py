#Python
from typing import Optional

#Pydantic
from pydantic import BaseModel

#FastAPI
from fastapi import FastAPI, Body, Query, Path

app = FastAPI()

# Models
class Location(BaseModel):
    city: str
    state: str
    country: str

class Person(BaseModel):
    first_name: str
    last_name: str
    age: int
    hair_color: Optional[str] = None
    is_married: Optional[bool] = None

@app.get('/')
def home():
    return {
        'message': 'Hello world'
    }

# Request and Response Body

@app.post('/person/new')
def create_person(person: Person = Body(...)):
    return person

@app.get('/person/detail')
def show_person(
    name: Optional[str] = Query(
        None
        , min_length = 1
        , max_length = 50
        , title = 'Person Name'
        , description = "This is the person name. It's between 1 and 50 characters"
    )
    , age: str = Query(
        ...
        , title = 'Person Age'
        , description = "This is the person age. It's required"
    )
):
    return {
        'name': name
        , 'age': age
    }

# validaciones: path parameters
@app.get('/person/detail/{person_id}')
def show_detail_person(
    person_id: int = Path(
        ...
        ,  gt = 0
        , title = 'Person Id'
        , description = "This is the person id. It's required and must be more than zero"
    )
):
    return {
        person_id: 'It exists!'
    }

# validaciones: request body
@app.put('/person/{person_id}')
def update_person(
    person_id: int = Path(
        ...
        ,  gt = 0
        , title = 'Person Id'
        , description = "This is the person id. It's required and must be more than zero"
    )
    , person: Person = Body(...)
    , location: Location = Body(...)
):
    results = person.dict()
    results.update(location.dict())

    return results
