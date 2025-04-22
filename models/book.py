from pydantic import BaseModel, Field
from typing import Optional

class Book(BaseModel):
    title: str = Field(...)
    code: str = Field(...)
    publish_date: str = Field(...)
    edition: Optional[int] = Field(default="1")
    author_id: int = Field(...)
    
    

    