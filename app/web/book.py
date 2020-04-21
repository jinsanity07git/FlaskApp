from flask import jsonify, request
from app.spider.yushun_book import YuShuBook
from app.libs.helper import is_isbn_or_key
from . import web
from app.forms.book import SearchFrom

@web.route('/book/search')
def search():
    # q = request.args['q']
    # page = request.args['page']
    form = SearchFrom(request.args)
    if form.validate():
        q = form.q.data.strip()
        page = form.page.data

        isbn_or_key = is_isbn_or_key(q)
        if isbn_or_key == 'isbn':
            result = YuShuBook.search_by_isbn(q)
        else:
            result = YuShuBook.search_by_keyword(q, page)

        return jsonify(result)
    else:
        return jsonify(form.errors)
