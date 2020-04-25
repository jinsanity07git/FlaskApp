import json

from flask import jsonify, request, render_template, flash
from sqlalchemy.sql.functions import current_user

from app.spider.yushun_book import YuShuBook
from app.libs.helper import is_isbn_or_key
from app.view_models.book import BookCollection, BookViewModel
from . import web
from app.forms.book import SearchFrom


@web.route('/book/search')
def search():
    # q = request.args['q']
    # page = request.args['page']
    form = SearchFrom(request.args)
    books = BookCollection()
    if form.validate():
        q = form.q.data.strip()
        page = form.page.data

        isbn_or_key = is_isbn_or_key(q)
        yushu_book = YuShuBook()
        if isbn_or_key == 'isbn':
            yushu_book.search_by_isbn(q)
        else:
            yushu_book.search_by_keyword(q, page)

        books.fill(yushu_book, q)

    else:
        # return jsonify(form.errors)
        flash('搜索的关键字不符合要求，请重新输入关键字')

    return render_template('search_result.html', books=books)


# @web.route('/book/search', methods=['Get', 'POST'])

@web.route('/book/<isbn>/detail')
# @cache.cached(timeout=1800)
def book_detail(isbn):
    pass
