#Python
from typing import Optional
from enum import Enum

#Pydantic
from pydantic import BaseModel, Field

#FastAPI
from fastapi import FastAPI, Body, Query, Path

app = FastAPI()

# Models
class HairColor(Enum):
    white =  'white'
    brown =  'brown'
    black =  'black'
    blonde = 'blonde'
    red =    'red'

class Location(BaseModel):
    city: str
    state: str
    country: str

class Person(BaseModel):
    first_name: str = Field(
        ...
        , min_length = 1
        , max_length = 50
        , example = 'Tony'
    )

    last_name: str = Field(
        ...
        , min_length = 1
        , max_length = 50
        , example = 'Stark'
    )

    age: int = Field(
        ...
        , gt = 0
        , le = 115
        , example = 27
    )

    hair_color: Optional[HairColor] = Field(
        default = None
        , example = 'black'
    )

    is_married: Optional[bool] = Field(
        default = None
        , example = True
    )

    # class Config:
    #     schema_extra = {
    #         'example': {
    #             'first_name': 'Bruce'
    #             , 'last_name': 'Wayne'
    #             , 'age': 21
    #             , 'hair_color': 'blonde'
    #             , 'is_married': False
    #         }
    #     }

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
