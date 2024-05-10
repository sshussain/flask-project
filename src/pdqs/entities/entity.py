from datetime import datetime
from typing import List

from sqlalchemy import create_engine, Column, String, Integer, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base, mapped_column, Mapped, relationship, scoped_session

# TODO Get Database configuration from Config class
db_url = 'localhost:5432'
db_name = 'online-exam'
db_user = 'postgres'
db_password = '0NLIN3-ex4m'
engine = create_engine(f'postgresql://{db_user}:{db_password}@{db_url}/{db_name}')
session = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine))

# TODO Use this for scoped session
#
#  db_session = scoped_session(sessionmaker(autocommit=False,
#                                          autoflush=False,
#                                          bind=engine))
# Base = declarative_base()
# Base.query = db_session.query_property()
#
# def init_db():
#     # import all modules here that might define models so that
#     # they will be registered properly on the metadata.  Otherwise
#     # you will have to import them first before calling init_db()
#     import yourapplication.models
#     Base.metadata.create_all(bind=engine)

Base = declarative_base()
Base.query = session.query_property()


class Author(Base):
    __tablename__ = 'author'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)

    # Relationship: one-to-many books for author
    books: Mapped[List["Book"]] = relationship(back_populates="author")

    def __repr__(self):
        return f"Author(id={self.id!r}, name={self.name!r})"


class Book(Base):
    __tablename__ = "book"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)

    # Relation many-to-one author for books
    author: Mapped[Author] = relationship(back_populates="books")

    # Relation one-to-many all reviews for this book
    reviews: Mapped[List["Review"]] = relationship(back_populates="reviewed_book")

    def __repr__(self):
        return f"Book(id={self.id!r}, title={self.title!r})"


class Review(Base):
    __tablename__ = "reviewß"
    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str] = mapped_column(String(1000), nullable=False)

    # Relation book for this review
    reviewed_book: Mapped[Book] = relationship(back_populates="reviews")

    def __repr__(self):
        return f"Review(id={self.id!r})"
