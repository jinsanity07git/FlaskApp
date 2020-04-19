# from flask import Flask,make_response,jsonify
from app import create_app

__author__ = "jinsanity"

app = create_app()


@app.route('/hi/')
def hello():
    headers = {
        'content-type': 'text/plain',
        'location': 'https://kepler.gl/demo'
    }
    # response = make_response('<html></html>',301)
    # response.headers =headers
    # return a simple tuple as response
    return '<html></html>', 301, headers


# # 主要用于基于类的视图，即插视图
# app.add_url_rule('/hi',view_func=hello)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=app.config['DEBUG'], port=5000)
