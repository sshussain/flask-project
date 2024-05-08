import abc
from typing import List, Dict

from pdqs.database import Author, Book, Review
from pdqs.models import AuthorResponseModel, BookResponseModel, ReviewResponseModel, CountModel


class CRUD(abc.ABC):
    @abc.abstractmethod
    def get_all_authors(self):
        ...

    @abc.abstractmethod
    def add_authors(self, author_names: List[str]):
        ...

    @abc.abstractmethod
    def get_all_books(self):
        ...

    @abc.abstractmethod
    def add_books(self, books: List[Dict]):
        ...

    @abc.abstractmethod
    def get_books_by_author(self, author_name):
        ...

    @abc.abstractmethod
    def get_reviews_for_book(self, book_title):
        ...

    @abc.abstractmethod
    def add_review_for_book(self, book_name, text):
        ...


class RawCrud(CRUD):
    def __init__(self, db):
        self.repo = db

    def get_all_authors(self) -> AuthorResponseModel:
        query_result: List[Author] = Author.query.order_by(Author.name).all()
        return AuthorResponseModel(names=[a.name for a in query_result])

    def add_authors(self, author_names: List[str]) -> AuthorResponseModel:
        for an in author_names:
            try:
                self.repo.session.add(Author(name=an))
            except Exception as e:
                pass
        self.repo.session.commit()
        return self.get_all_authors()

    def get_all_books(self) -> BookResponseModel:
        query_result: List[Book] = Book.query.order_by(Book.title).all()
        return BookResponseModel(titles=[b.title for b in query_result])

    def add_books(self, books: List[Dict]) -> BookResponseModel:
        for b in books:
            author = b['author_name']
            title = b['title']

            a = Author.query.filter(Author.name == author).first()
            author_id = a.id
            if author_id:
                self.repo.session.add(Book(title=title, author_id=author_id))
                self.repo.session.commit()
        return self.get_all_books()

    def get_books_by_author(self, author_name) -> BookResponseModel:
        a = Author.query.filter(Author.name == author_name).first()
        author_id = a.id
        query_result: List[Book] = Book.query.filter(Book.author_id == author_id).all()
        return BookResponseModel(titles=[b.title for b in query_result])

    def get_reviews_for_book(self, book_name) -> ReviewResponseModel:
        book: Book = Book.query.filter_by(name=book_name).first()
        if book is None:
            return ReviewResponseModel(text=[])
        query_result: List[Review] = Review.query.filter_by(book_id=book.id).all()
        return ReviewResponseModel(texts=[r.review_text for r in query_result])

    def add_review_for_book(self, book_name, text) -> CountModel:
        book: Book = Book.query.filter_by(name=book_name).first()
        if book is None:
            return f'Book {book_name} does not exist'
        review = Review(book_id=book.id, review_text=text)
        self.repo.session.add(review)
        self.repo.session.commit()
        count = Review.query.filter_by(book_id=book.id).count()
        return CountModel(count=count)
