from pydantic import BaseModel, Field

class Category(BaseModel):
    """Category's Info"""
    name: str = Field(
        ...,
        min_length=1,
        max_length=255,
        title="Category's name",
        description="It's the category's name",
        example='Novel'
    )

class CategoryResponce(Category):
    """Endpoint's responce"""
    id: int = Field(
        ...,
        example=1
    )