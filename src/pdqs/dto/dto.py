from datetime import datetime
from typing import List, Dict

import pydantic


class GreetingDto(pydantic.BaseModel):
    time: datetime
    greeting: str


class AuthorResponseDto(pydantic.BaseModel):
    name: List[str]


class AuthorCreateDto(pydantic.BaseModel):
    name: List[str]


class BookResponseDto(pydantic.BaseModel):
    # title: List[str]
    book: List[Dict[str, str]]


class ReviewResponseDto(pydantic.BaseModel):
    text: List[str]


class CountDto(pydantic.BaseModel):
    count: int
