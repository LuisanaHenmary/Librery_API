from pydantic import BaseModel, Field
from typing import Optional

class Book(BaseModel):
    """Book's Info"""
    title: str = Field(
        ...,
        min_length=1,
        max_length=150,
        title="Book's title",
        description="It's the book's title",
        example='The metamorphosis'
    )
    code: str = Field(
        ...,
        min_length=1,
        max_length=150,
        title="Book's code",
        description="It's the book's serial code",
        example='A-1'
    )
    publish_date: str = Field(
        ...,
        min_length=1,
        max_length=150,
        title="Book's publish date",
        description="It's the book's publish date",
        example='May, 1915'
    )
    edition: Optional[int] = Field(default="1")
    author_id: int = Field(
        ...,
        title="Book's author ID",
        description="It's the book's author ID",
        example=1
    )
    id_category: int = Field(
        ...,
        title="Book's category ID",
        description="It's the book's category ID",
        example=1
    )
    
    
class BookResponce(Book):
    """Endpoint's responce"""
    id: int = Field(
        ...,
        example=1
    )

    is_available: Optional[bool] = Field()

    