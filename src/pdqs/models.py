from datetime import datetime
from typing import List, Dict

import pydantic


class GreetingModel(pydantic.BaseModel):
    time: datetime
    greeting: str


class AuthorResponseModel(pydantic.BaseModel):
    names: List[str]


class AuthorCreateModel(pydantic.BaseModel):
    names: List[str]


class BookResponseModel(pydantic.BaseModel):
    titles: List[str]
    # books: List[Dict[str, str]]


class ReviewResponseModel(pydantic.BaseModel):
    text: List[str]


class CountModel(pydantic.BaseModel):
    count: int
