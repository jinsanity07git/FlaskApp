from flask import jsonify, request
from yushun_book import YuShuBook
from helper import is_isbn_or_key
from . import web


@web.route('/book/search')
def search():
    q = request.args['q']
    page = request.args['page']
    isbn_or_key = is_isbn_or_key(q)
    if isbn_or_key == 'isbn':
        result = YuShuBook.search_by_isbn(q)
    else:
        result = YuShuBook.search_by_keyword(q)

    return jsonify(result)
