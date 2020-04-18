from flask import Flask,make_response
from helper import is_isbn_or_key

__author__ = "jinsanity"


app = Flask(__name__)
app.config.from_object('config')

@app.route('/book/search/<q>/<page>')
def search(q,page):
    isbn_or_key = is_isbn_or_key(q)
    pass


@app.route('/hi/')
def hello():
    headers ={
        'content-type' : 'text/plain',
        'location':'https://kepler.gl/demo'
    }
    # response = make_response('<html></html>',301)
    # response.headers =headers
    ## return a simple tuple as response
    return '<html></html>',301,headers

# # 主要用于基于类的视图，即插视图
# app.add_url_rule('/hi',view_func=hello)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=app.config['DEBUG'] ,port=5000)