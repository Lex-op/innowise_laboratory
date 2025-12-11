from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import validates
from typing import Dict, Any
from database import Base


class Book(Base):
    """
    SQLAlchemy ORM model representing a book in the collection.

    Attributes:
        id: Primary key identifier.
        title: Book title (required, indexed).
        author: Book author (required, indexed).
        year: Year of publication (optional).
    """

    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False, index=True)
    author = Column(String, nullable=False, index=True)
    year = Column(Integer, nullable=True)

    def __repr__(self) -> str:
        """
        Return a string representation of the Book instance.

        Returns:
            str: String representation showing id, truncated title, and author.
        """
        return f"<Book(id={self.id}, title='{self.title[:30]}...', author='{self.author}')>"

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the Book instance to a dictionary.

        Returns:
            Dict[str, Any]: Dictionary representation of the book.
        """
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "year": self.year,
        }

    @validates("title", "author")
    def validate_not_empty(self, key: str, value: str) -> str:
        """
        Validate that title and author fields are not empty.

        Args:
            key: Field name being validated ('title' or 'author').
            value: Field value to validate.

        Returns:
            str: Stripped value if validation passes.

        Raises:
            ValueError: If value is empty after stripping whitespace.
        """
        value = value.strip()
        if not value:
            raise ValueError(f"{key} cannot be empty")
        return value
