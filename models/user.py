from pydantic import BaseModel, Field

class UserAuth(BaseModel):
    """This is for user authentication."""
    username: str = Field(
        ...,
        min_length=1,
        max_length=255,
        title="Username",
        description="It's the person's username"
    )
    password: str = Field(..., title="Password", description="It's the accoun's password")

class UserRegister(UserAuth):

    """Personal User's info"""
    ci: str = Field(
        ...,
        min_length=1,
        max_length=255,
        title="CI",
        description="It's the person's CI"
    )
    email: str = Field(
        ...,
        min_length=1,
        max_length=255,
        title="E-mail",
        description="It's the person's email"
    )
    phone_number: str = Field(
        ...,
        min_length=1,
        max_length=255,
        title="Phone number",
        description="It's the person's phone number"
    )

