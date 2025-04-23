from pydantic import BaseModel, Field

class Author(BaseModel):
    """Author's Info"""
    name: str = Field(
        ...,
        min_length=1,
        max_length=255,
        title="Author's name",
        description="It's the author's name",
        example='Franks Kafka'
    )

class AuthorResponce(Author):
    """Endpoint's responce"""
    id: int = Field(
        ...,
        example=1
    )