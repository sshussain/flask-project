import csv
from datetime import datetime
from typing import List, Dict

# Database URL format
# dialect+driver://username:password@host:port/database
# driver is optional. If not specified, the default driver for Postgres is psycopg2
from sqlalchemy import create_engine, String, ForeignKey, select, Engine, DateTime
from sqlalchemy.orm import Session, relationship, DeclarativeBase, Mapped, mapped_column

DATABASE_URL = "postgresql://postgres:postgres@dbhost:5432/postgres"
# DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/postgres"
engine = create_engine(DATABASE_URL)  # , echo=True)


class Base(DeclarativeBase):
    ...


# TODO Use this as a common entity to auto inject create and update dates
class Entity:
    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime)
    updated_at: Mapped[DateTime] = mapped_column(DateTime)
    last_updated_by: Mapped[DateTime] = mapped_column(DateTime)

    def __init__(self, created_by):
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.last_updated_by = created_by


class Author(Base):
    __tablename__ = "author"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True)

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


class UserCreds(Base):
    __tablename__ = "user_creds"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    password: Mapped[str] = mapped_column(String(32))

    def __repr__(self):
        return f"UserCreds(id={self.id!r}, name={self.name!r}, password={self.password!r})"


def init_db():
    Base.metadata.create_all(engine)


class BookReviewCrud:
    def __init__(self, database_engine: Engine):
        self._engine = database_engine
        self._session = Session(self._engine)

    def load(self, csvfile):
        with open(csvfile, newline='') as csvfile:
            cr = csv.reader(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL, skipinitialspace=True)
            # Skip header line
            next(cr, None)
            for row in cr:
                name = row[0].strip()
                title = row[1].strip()
                # Add author if not available
                existing_name = self._session.query(Author).filter(Author.name == name).first()
                if not existing_name:
                    self.add_author(name)
                # Add book for author
                count = self._session.query(Book).filter(Book.title == title).count()
                if not count:
                    self.add_book_for_author(name, title)

    def add_author(self, name: str) -> int:
        """

        :param name: author name
        :return: number of authors
        """
        self._session.add(Author(name=name))
        self._session.commit()
        count = self._session.query(Author).count()
        return count

    def get_all_authors(self) -> List[str]:
        """

        :return:
        """
        return [a.name for a in self._session.scalars(select(Author))]

    def add_book_for_author(self, name: str, title: str) -> int:
        """

        :param name: Author name
        :param title: Title of the book
        :return: number of books by this author
        """
        author = self._session.query(Author).filter(Author.name == name).first()
        print(f"Book to be added for author {author}")
        self._session.add(Book(title=title, author=author))
        self._session.commit()
        return 0

    def get_all_books(self) -> List[Dict[str, str]]:
        """

        :return:
        """
        return [{"name": b.author.name, "title": b.title} for b in self._session.scalars(select(Book))]

    def add_review_for_book(self, title: str, text: str) -> int:
        """

        :param title: Title (name) of the book
        :param text:
        :return: number of reviews for the given book
        """
        book = self._session.query(Book).filter(Book.title == title).first()
        self._session.add(Review(text=text, book=book))
        self._session.commit()
        count = self._session.query(Review).filter(Review.book == book).count()
        return count

    def get_reviews_for_book(self, title: str, offset: int = 0, result_size=-1) -> List[str]:
        """

        :param title:
        :param offset:
        :param result_size:
        :return:
        """
        stmt = select(Review).join(Book, Review.book_id == Book.id).where(Book.title == title)
        result = self._session.scalars(stmt).all()
        return [r.text for r in result]

    def __repr__(self):
        return f"db_url={self._engine.url}"


if __name__ == '__main__':

    init_db()
    crud = BookReviewCrud(engine)
    crud.load("/Users/sshussai/PycharmProjects/flask-project/data/author-book.csv")
    l = crud.get_all_authors()
    print(f"All authors {l}")
    l = crud.get_all_books()
    print(f"All books: {l}")
    # btitle = "Emma"
    # crud.add_review_for_book("Emma", "This is a boring book -- too long and meandering.")
    print(f"Get reviews")
    rb = crud.get_reviews_for_book("Emma")
    print(f"Reviews: {rb}")
    # crud.add_book_for_author("Jane Austen", "Emma")
    # crud.add_book_for_author("Jane Austen", "Sense and Sensibility")

    # crud.add_review_for_book("Emma", "This is a boring book -- too long and meandering.")
    # crud.add_review_for_book("David Copperfield", "A good read for long nights.")
    # number_of_reviews = crud.add_review_for_book("David Copperfield", "The book is set in Victorian era")

