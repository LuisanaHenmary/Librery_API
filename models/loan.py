from pydantic import BaseModel, Field
from typing import Optional

class Loan(BaseModel):
    """Loan's Info"""

    initial_date: str = Field(
        ...,
        min_length=1,
        max_length=50,
        title="Initial date",
        description="It's the Loan's initial date",
        example='April 01, 2025'
    )

    delivere_date: str = Field(
        ...,
        min_length=1,
        max_length=50,
        title="Final date",
        description="It's the Loan's initial date",
        example='April 01, 2025'
    )

    id_user: int = Field(
        ...,
        title="User's ID",
        description="It's the normal user's ID",
        example=2
    )

    id_book: int = Field(
        ...,
        title="Book's ID",
        description="It's the loaned book's ID",
        example=1
    )

class LoanResponce(Loan):
    """Endpoint's responce"""
    id: int = Field(
        ...,
        example=1
    )

    was_delivered_on_time: Optional[bool] = Field() 