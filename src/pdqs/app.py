import logging
import os
from datetime import datetime as dt

from flask import Flask, request, jsonify, Response, redirect, url_for
import flask_cors

import pdqs.repo
from pdqs.dto.dto import GreetingDto, AuthorResponseDto, BookResponseDto, CountDto
from pdqs.user_admin import user_admin

logging.basicConfig(filename='logfile',
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)

app = Flask(__name__)
flask_cors.CORS(app)

app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.register_blueprint(user_admin, url_prefix='/user')

from pdqs.repo import engine, BookReviewCrud
pdqs.repo.init_db()
crud = BookReviewCrud(engine)

@app.route("/alive")
def get_system_status() -> Response:
    return "I am alive", 200


@app.route('/', methods=['GET'])
def home() -> Response:
    return redirect(url_for('index'))


@app.route('/index', methods=['GET'])
def index() -> Response:
    utc_now = dt.utcnow()
    return jsonify(GreetingDto(time=utc_now, greeting="Hello World!").dict())


@app.route('/author', methods=['GET'])
def get_all_authors() -> Response:
    """ Returns a list of all authors."""
    author_results = AuthorResponseDto(name=crud.get_all_authors())
    return jsonify(author_results.dict())


@app.route('/author', methods=['POST'])
def create_author() -> Response:
    """ Add author
    Request body is JSON {"name":"<author_name>"}
    :return: Number of available authors
    """
    j = request.get_json()
    name = j['name']
    count = crud.add_author(name)
    return jsonify(CountDto(count=count).dict())


@app.route('/book', methods=['GET'])
def get_all_books() -> Response:
    """
    Returns a list of all available books.
    :return: list of books

    The response is JSON list of books
    { "title": [ "book1", "book2"] }
    """
    book_results = crud.get_all_books()
    return jsonify(BookResponseDto(title=book_results).dict())


@app.route('/book', methods=['POST'])
def create_book_for_author() -> Response:
    """
    Add given book for the author.

    The request body is a JSON {"name": "<author_name>", "title": "<book_name>"}

    The response is number of available books by the author

    Example

    Request
        {"name": "Charles Dickens", "title": "Christmas Carols"}

    Response
        { "count": "<number of books by the author" }

    """
    jobj = request.get_json()
    name = jobj['name']
    title = jobj['title']
    count: int = crud.add_book_for_author(name, title)
    dto = CountDto(count=count)
    return jsonify(dto.dict())
#
#
# @app.route('/books/author/<string:author_name>', methods=["GET"])
# def get_books_for_author(author_name: str) -> Response:
#     """ Get a list of books for a given author
#     :param author_name: name of the author
#     :return: list of books
#
#     The response body is JSON list of books
#     Example
#         request uri path /books/author/Charles%20Dickens
#         response
#             {["Christmas Carols", "David Copperfield"]}
#     """
#     book_results: BookResponseDto = review_crud.get_books_by_author(author_name)
#     return jsonify(book_results.dict())
#
#
@app.route('/review', methods=["POST"])
def create_review_for_book() -> Response:
    """ Add a new review

    The request body is JSON, and contains the following fields:

    'title' and 'text' of the review.

    Response is JSON with number of reviews for the specified book,

    Example
        Request:
            {"title": "Christmas Carols", "text": "This a good book"}

        Response:
            {"count": 2}
    """
    body = request.get_json()
    title = body['title']
    text = body['text']
    result: CountDto = review_crud.add_review_for_book(title, text)
    return jsonify(result.dict())
#
#   /review?title=
@app.route('/review', methods=["GET"])
def get_reviews_for_book(title: str) -> Response:
    """ Get a list of reviews for a given book
    :param title: Name of the book
    :return: Reviews for book

    The response body is JSON list of reviews
    Example
        request uri path /reviews/book/Christmas%20Carols
        response
            {["This is a good book", "Not worth reading"]}
    """
    title = request.args.get('title')
    logging.info(f"Book title is <{title}>")
    reviews = crud.get_reviews_for_book(title)
    return jsonify(reviews)


if __name__ == '__main__':
    app.run(debug=True)
