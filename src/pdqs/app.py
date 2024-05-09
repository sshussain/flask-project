import logging
import os
from logging.config import dictConfig
# from typing import Any

from flask import Flask, request, jsonify, Response, redirect, url_for
# from flask.logging import default_handler
from flask_sqlalchemy import SQLAlchemy

from pdqs.models import GreetingModel, AuthorResponseModel, BookResponseModel, ReviewResponseModel, CountModel

app = Flask(__name__)

# Example of loading from a yaml file
# data = yaml_loader.yaml("/Users/pjose/Project/dev_maintenance/backend/config.yaml")
# app.config.from_object(data)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

logging.config.dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})
gunicorn_logger = logging.getLogger('gunicorn.debug')
app.logger.handlers = gunicorn_logger.handlers
app.logger.setLevel(gunicorn_logger.level)

db = SQLAlchemy(app)

""" NOTE
The import should be here to prevent cyclic dependencies. A better solution is to write a CRUD interface that
manages database.
"""
from pdqs import database
from pdqs.crud import CRUD, RawCrud

review_crud: CRUD = RawCrud(db)


@app.route('/', methods=['GET'])
def home() -> Response:
    return jsonify(GreetingModel(greeting="Hello World!").dict())
    # return redirect(url_for('index'))


# @app.route('/index', methods=['GET'])
# def index() -> Response:
#     return jsonify(GreetingModel(greeting="Hello World!").dict())


@app.route('/authors', methods=['GET'])
def get_all_authors() -> Response:
    """ Returns a list of all authors."""
    author_results: AuthorResponseModel = review_crud.get_all_authors()
    return jsonify(author_results.dict())


@app.route('/authors', methods=['POST'])
def create_author() -> Response:
    """ Add authors in the request.
         The request body is JSON list
         Return list of all available authors
    Example:
        Request: {"names": ["<NAME1>", "<NAME2>"]}
        Response: {"names": [<all authors>]
    """
    j = request.get_json()
    names = j['names']
    author_results: AuthorResponseModel = review_crud.add_authors(names)
    return jsonify(author_results.dict())


@app.route('/books', methods=['GET'])
def get_all_books() -> Response:
    """
    Returns a list of all available books.
    :return: list of books

    The response is JSON list of books
    """
    book_results: BookResponseModel = review_crud.get_all_books()
    return jsonify(book_results.dict())


@app.route('/books', methods=['POST'])
def create_book_for_author() -> Response:
    """
    Add list of books specified in request.
    The request body is JSON list
    The response is JSON list of all created books
    Example
    Request
    {[
        {"author_name": "Charles Dickens", "title": "Christmas Carols"},
        {"author_name": "Jane Austen", "title": "Emma"}
    ]}

    Response
    { "titles": ["Christmas Carols", "Emma"] }
    """
    j = request.get_json()['books']
    book_results: BookResponseModel = review_crud.add_books(j)
    return jsonify(book_results.dict())


@app.route('/books/author/<string:author_name>', methods=["GET"])
def get_books_for_author(author_name: str) -> Response:
    """ Get a list of books for a given author
    :param author_name: name of the author
    :return: list of books

    The response body is JSON list of books
    Example
        request uri path /books/author/Charles%20Dickens
        response
            {["Christmas Carols", "David Copperfield"]}
    """
    book_results: BookResponseModel = review_crud.get_books_by_author(author_name)
    return jsonify(book_results.dict())


@app.route('/reviews/book', methods=["POST"])
def create_review_for_book() -> Response:
    """ Add a new review

    The request body is JSON, and contains the following fields:

    'book_name' and 'text' of the review.

    Response is JSON with number of reviews for the specified book,

    Example
        Request:
            {"book_name": "Christmas Carols", "text": "This a good book"}

        Response:
            {"count": 2}
    """
    body = request.get_json()
    book_name = body['book_name']
    text = body['text']
    result: CountModel = review_crud.add_review_for_book(book_name, text)
    return jsonify(result.dict())


@app.route('/reviews/book/<string:book_name>', methods=["GET"])
def get_reviews_for_book(book_name: str) -> Response:
    """ Get a list of reviews for a given book
    :param book_name: Name of the book
    :return: Reviews for book

    The response body is JSON list of reviews
    Example
        request uri path /reviews/book/Christmas%20Carols
        response
            {["This is a good book", "Not worth reading"]}
    """
    reviews = review_crud.get_reviews_for_book(book_name)
    return jsonify(reviews)


if __name__ == '__main__':
    app.run(debug=True)
