from typing import List

# Database URL format
# dialect+driver://username:password@host:port/database
# driver is optional. If not specified, the default driver for Postgres is psycopg2
from sqlalchemy import create_engine, String, ForeignKey, select, Engine
from sqlalchemy.orm import Session, relationship, DeclarativeBase, Mapped, mapped_column

DATABASE_URL = "postgresql://postgres:postgres@dbhost:5432/postgres"
engine = create_engine(DATABASE_URL)  # , echo=True)


class Base(DeclarativeBase):
    ...


class Author(Base):
    __tablename__ = "author"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))

    books: Mapped[List["Book"]] = relationship(back_populates="author", cascade="all, delete-orphan")

    def __repr__(self):
        return f"Author(id={self.id!r}, name={self.name!r})"


class Book(Base):
    __tablename__ = "book"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100), unique=True)
    author_id: Mapped[int] = mapped_column(ForeignKey("author.id"))

    author: Mapped["Author"] = relationship(back_populates="books")
    reviews: Mapped[List["Review"]] = relationship(back_populates="book", cascade="all, delete-orphan")

    def __repr__(self):
        return f"Book(id={self.id!r}, name={self.title!r}, author_id={self.author_id})"


class Review(Base):
    __tablename__ = "review"

    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str] = mapped_column(String(1000))
    book_id: Mapped[int] = mapped_column(ForeignKey("book.id"))

    book: Mapped["Book"] = relationship(back_populates="reviews")


class Genre(Base):
    __tablename__ = "genre"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))


class BookGenreAssociation(Base):
    __tablename__ = "book_genre"
    id: Mapped[int] = mapped_column(primary_key=True)
    genre_id: Mapped[int] = mapped_column(ForeignKey("genre.id"))
    book_id: Mapped[int] = mapped_column(ForeignKey("book.id"))
    book = relationship("Book", backref="genre")
    genre = relationship("Genre", backref="book")

    def __repr__(self):
        return f"BookGenreAssociation(book_id={self.book_id!r}, {self.genre_id!r})"


def init_db():
    Base.metadata.create_all(engine)


class BookReviewCrud:
    def __init__(self, database_engine: Engine):
        self._engine = database_engine
        self._session = Session(self._engine)

    def add_author(self, name: str):
        """

        :param name:
        :return:
        """
        self._session.add(Author(name=name))
        self._session.commit()
        # TODO total number of authors
        count = self._session.query(Author).count()
        return count

    def get_all_authors(self) -> List[str]:
        """

        :return:
        """
        return [a.name for a in self._session.scalars(select(Author))]

    def add_book_for_author(self, name: str, title: str) -> bool:
        """

        :param name:
        :param title:
        :return:
        """
        return False

    def get_all_books(self) -> List[str]:
        """

        :return:
        """
        return [b.title for b in self._session.scalars(select(Book))]

    def add_review_for_book(self, title: str, text: str):
        """

        :param title:
        :param text:
        :return:
        """
        ...

    def get_reviews_for_books(self, title: str, offset: int = 0, result_size=-1) -> List[str]:
        """

        :param title:
        :param offset:
        :param result_size:
        :return:
        """
        return []

    def get_books_for_genre(self, title: str) -> List[str]:
        """

        :param title:
        :return:
        """
        return []

    def __repr__(self):
        return f"db_url={self._engine.url}"


if __name__ == '__main__':
    init_db()
    crud = BookReviewCrud(engine)
    author_count = crud.add_author("Stephen King")
    print(f"Number of available authors {author_count}")
    count2 = crud.add_author("Charles Dickens")
    print(f"Number of available authors {count2}")
    count3 = crud.add_author("Jane Austen")
    print(f"Number of available authors {count3}")
    count4 = crud.add_author("Leo Tolstoy")
    print(f"Number of available authors {count4}")
    # clean_all()
    # populate()
    print(crud.get_all_authors())
    print(crud.get_all_books())
    crud.add_book_for_author("Charles Dickens", "David Copperfield")
    crud.add_book_for_author("Jane Austen", "Emma")
    crud.add_book_for_author("Jane Austen", "Sense and Sensibility")
