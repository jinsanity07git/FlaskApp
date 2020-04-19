from flask import jsonify
from yushun_book import YuShuBook 
from helper import is_isbn_or_key
from flask import Blueprint

web = Blueprint('web',__name__)

@web.route('/book/search/<q>/<page>')
def search(q,page):
    isbn_or_key = is_isbn_or_key(q)
    if isbn_or_key =='isbn':
        result = YuShuBook.search_by_isbn(q)
    else:
        result = YuShuBook.search_by_keyword(q)

    return jsonify(result)
 
