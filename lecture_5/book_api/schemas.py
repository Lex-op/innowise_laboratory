from pydantic import BaseModel, Field, field_validator, ConfigDict
from typing import Optional, Annotated


class BookBase(BaseModel):
    """
    Base Pydantic model for book data with common validation.

    Attributes:
        title: Book title (required, minimum length 1).
        author: Book author (required, minimum length 1).
        year: Year of publication (optional).
    """

    title: Annotated[
        str,
        Field(..., min_length=1, examples=["War and peace"], description="Book title"),
    ]
    author: Annotated[
        str,
        Field(..., min_length=1, examples=["Lev Tolstoy"], description="Book author"),
    ]
    year: Annotated[
        Optional[int], Field(None, examples=[1869], description="Year of publication")
    ] = None

    @field_validator("title", "author")
    @classmethod
    def validate_not_empty(cls, v: str) -> str:
        """
        Validate that string fields are not empty or whitespace-only.

        Args:
            v: String value to validate.

        Returns:
            str: Stripped value if validation passes.

        Raises:
            ValueError: If value is empty or contains only whitespace.
        """
        v_stripped = v.strip()
        if not v_stripped:
            raise ValueError("Field cannot be empty or contain only whitespace")
        return v_stripped


class BookCreate(BookBase):
    """Pydantic model for creating a new book."""


class BookUpdate(BaseModel):
    """
    Pydantic model for updating an existing book.

    Attributes:
        title: Book title (optional, minimum length 1 if provided).
        author: Book author (optional, minimum length 1 if provided).
        year: Year of publication (optional).
    """

    title: Annotated[
        Optional[str], Field(None, min_length=1, description="Book title")
    ] = None
    author: Annotated[
        Optional[str], Field(None, min_length=1, description="Book author")
    ] = None
    year: Annotated[Optional[int], Field(None, description="Year of publication")] = (
        None
    )


class BookResponse(BookBase):
    """
    Pydantic model for book API responses.

    Attributes:
        id: Unique identifier of the book.
    """

    id: Annotated[
        int, Field(..., description="The unique identifier of the book", examples=[1])
    ]

    model_config = ConfigDict(from_attributes=True)
