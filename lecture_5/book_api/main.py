from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
import models
import schemas
from database import get_db, create_tables
from typing import Annotated


create_tables()

app = FastAPI(
    title="Book Collection API",
    description="A simple API for managing book collection",
    version="1.0.0",
)


@app.post("/books/", response_model=schemas.BookResponse, status_code=201)
def create_book(
    book: schemas.BookCreate, 
    db: Annotated[Session, Depends(get_db)]
) -> schemas.BookResponse:
    """
    Create a new book in the collection.

    Args:
        book: BookCreate schema containing book details.
        db: Database session dependency.

    Returns:
        schemas.BookResponse: The created book with its assigned ID.

    Raises:
        HTTPException: If database operation fails.
    """
    db_book = models.Book(title=book.title, author=book.author, year=book.year)
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


@app.get("/books/", response_model=List[schemas.BookResponse])
def get_all_books(
    skip: int = Query(0, ge=0, description="Number of items to skip"),
    limit: int = Query(
        100, ge=1, le=1000, description="Maximum number of items to return"
    ),
    db: Session = Depends(get_db),
) -> List[schemas.BookResponse]:
    """
    Retrieve all books with pagination.

    Args:
        skip: Number of records to skip for pagination.
        limit: Maximum number of records to return.
        db: Database session dependency.

    Returns:
        List[schemas.BookResponse]: Paginated list of books.
    """
    books = db.query(models.Book).offset(skip).limit(limit).all()
    return books # type: ignore


@app.delete("/books/{book_id}", status_code=204)
def delete_book(
    book_id: int, 
    db: Session = Depends(get_db)
) -> None:
    """
    Delete a book by its ID.

    Args:
        book_id: ID of the book to delete.
        db: Database session dependency.

    Raises:
        HTTPException: If book with given ID is not found.
    """
    book = db.query(models.Book).filter(models.Book.id == book_id).first()

    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    db.delete(book)
    db.commit()


@app.put("/books/{book_id}", response_model=schemas.BookResponse)
def update_book(
    book_id: int, 
    book_update: schemas.BookUpdate, 
    db: Session = Depends(get_db)
) -> schemas.BookResponse:
    """
    Update an existing book's details.

    Args:
        book_id: ID of the book to update.
        book_update: BookUpdate schema with fields to update.
        db: Database session dependency.

    Returns:
        schemas.BookResponse: The updated book.

    Raises:
        HTTPException: If book with given ID is not found.
    """
    db_book = db.query(models.Book).filter(models.Book.id == book_id).first()

    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")

    update_data = book_update.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(db_book, field, value)

    db.commit()
    db.refresh(db_book)
    return db_book


@app.get("/books/search/", response_model=List[schemas.BookResponse])
def search_books(
    title: Optional[str] = Query(None, description="Search by title"),
    author: Optional[str] = Query(None, description="Search by author"),
    year: Optional[int] = Query(None, description="Search by exact year"),
    db: Session = Depends(get_db),
) -> List[schemas.BookResponse]:
    """
    Search books by various criteria.

    Args:
        title: Substring to search in book titles (case-insensitive).
        author: Substring to search in author names (case-insensitive).
        year: Exact year of publication to match.
        db: Database session dependency.

    Returns:
        List[schemas.BookResponse]: List of books matching search criteria.
    """
    query = db.query(models.Book)

    if title:
        query = query.filter(models.Book.title.ilike(f"%{title}%"))
    if author:
        query = query.filter(models.Book.author.ilike(f"%{author}%"))
    if year:
        query = query.filter(models.Book.year == year)

    return query.all()


@app.get("/")
def read_root() -> Dict[str, Any]:
    """
    Root endpoint providing API information.

    Returns:
        Dict[str, Any]: Welcome message and available endpoints.
    """
    return {
        "message": "Welcome to Book Collection API",
        "docs": "Visit /docs for interactive API documentation",
        "endpoints": {
            "POST /books/": "Add a new book",
            "GET /books/": "Get all books",
            "PUT /books/{id}": "Update book details",
            "DELETE /books/{id}": "Delete a book by ID",
            "GET /books/search/": "Search books",
        },
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
