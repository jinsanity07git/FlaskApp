

# flaskApp

flask learning


* kill whatever process is using port 8080 so that I can vagrant up?
```
lsof -n -i4TCP:5000
kill -9 PID
```



[2-6 flask最小原型与唯一URL原则.avi]()

URL兼容/原理： 重定向 2-6

![image-20200418145104427](README_img/image-20200418145104427.png)





2-7 路由的另一种注册方法

```
## 调试状态 无需反复启动服务器
app.run(debug=True)

# 主要用于基于类的视图，即插视图
app.add_url_rule('/hi',view_func=hello)
```



2-8 app.run相关参数与flask配置文件

```
#接受外网访问，端口设置
app.run(host="0.0.0.0", debug=True,port=5000)

## subclass of the dict:  app.config['DEBUG']
## all variable in config should be in capital 
app.config.from_object('config')
app.run(host="0.0.0.0", debug=app.config['DEBUG'] ,port=5000)
```



2-9 你并没有真正理解 if __name__的作用 .

```
Nginx + uwsgi 
```



2-10 响应对象：Response

```
view function return

status code 200, 404, 301
content-type httpheaders
content-type= text/html
Response object


def hello():
    headers ={
        'content-type' : 'text/plain'
    }
    response = make_response('<html></html>',404)
    response.headers =headers
    return response
    
## 301 location url redirection     
def hello():
    headers ={
        'content-type' : 'text/plain',
        'location':'https://kepler.gl/demo'
    }
    response = make_response('<html></html>',301)
    response.headers =headers
    return response
    
def hello():
    headers ={
        'content-type' : 'text/plain',
        'location':'https://kepler.gl/demo'
    }
    # response = make_response('<html></html>',301)
    # response.headers =headers
    ## return a simple tuple as response
    return '<html></html>',301,headers

```





3-1 搜索而不是拍照上传

3-2 数据API

```
关键字搜索
http://t.yushu.im/v2/book/search?q={}&start={}&count={}

isbn搜索
http://t.yushu.im/v2/book/isbn/{isbn}
```

3-3 搜索关键字

```
# get agrv from url
@app.route('/book/search/<q>/<page>')
def search(q,page):
```

3-4 简单的重构

```

```

3-5 requests发送http请求及代码的简化手段

```
class HTTP:

    @staticmethod
    def get(url, return_json=True):
        r = requests.get(url)
        # restful
        # json
        if r.status_code != 200:
            return {} if return_json else ''
        return r.json() if return_json else r.text

```



3-6 requests vs urllib

```
staticmethod vs classmethod
staticmethod: no self
classmethod : no self but cls

经典类 VS 新式类
```

3-7 从API获取数据



```
self : 链式查找


from http import HTTP

class YuShuBook:
    isbn_url ='http://t.yushu.im/v2/book/isbn/{}'
    keyword_url = 'http://t.yushu.im/v2/book/search?q={}&start={}&count={}'

    @classmethod
    def search_by_isbn(cls, isbn):
        url = cls.isbn_url.format(isbn)
        result=HTTP.get(url)
        return result
    @classmethod
    def search_by_keyword(cls, keyword, count=15, start=0):
        url = cls.keyword_url.format(keyword, count, start)
        results = HTTP.get(url)
        return results
```

3-8 使用jsonify

http.py 会与 自带的http.client 冲突



3-9 将视图函数拆分到单独的文件中 

如何导入 app 到分文件中？

3-10 深入了解flask路由

![image-20200418190521528](README_img/image-20200418190521528.png)

3-11 循环引入流程分析.a

![image-20200418191349505](README_img/image-20200418191349505.png)

3-12 找不到视图函数的最终解释与证明

```
print ("id:" + str(id(app) + entity)
```



4-1 应用、蓝图与视图函数

![image-20200418192822874](README_img/image-20200418192822874.png)



4-2 用蓝图注册视图函数

App/init

```
from flask import Flask


def create_app():
    app = Flask(__name__)
    app.config.from_object('config')
    register_blueprint(app)
    return app

def register_blueprint(app):
    from app.web.book import web
    app.register_blueprint(web)
```

app/Web/book

```
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
 
```



4-3 单蓝图多模块拆分视图函数



```
__init__.py
from flask import Blueprint

web = Blueprint('web', __name__)

from app.web import book
from app.web import user
```



4-4 request 对象

```
http://localhost:5000/book/search?q=9787111562108&page=123

pyCharm debugger
check the type of request: LocalProxy or response

```

4-5 WTForms参数验证

```
pipenv install wtforms

```

```
from wtforms import Form, StringField, IntegerField
from wtforms.validators import Length, NumberRange


class SearchFrom(Form):
    q = StringField(validators=[Length(min=1, max=30)])
    page = IntegerField(validators=[NumberRange(min=1, max=99)], default=1)

```



4-6 拆分配置文件

```
http://localhost:5000/book/search?q=9787111562108

http://localhost:5000/book/search?q= &page=1

localhost:5000/book/search?q=郭敬明&page=1
```

```
setting.py
secure.py 

from flask import current_app
```



4-7 Model First、Database First与Code First

```
libs
```

4-8 定义第一个模型类

```
pipenv install flask_sqlalchemy
```

```
(flaskApp) jinsanity@jinsanity-pro flaskApp % pipenv graph
Flask-SQLAlchemy==2.4.1
  - Flask [required: >=0.10, installed: 1.1.2]
    - click [required: >=5.1, installed: 7.1.1]
    - itsdangerous [required: >=0.24, installed: 1.1.0]
    - Jinja2 [required: >=2.10.1, installed: 2.11.2]
      - MarkupSafe [required: >=0.23, installed: 1.1.1]
    - Werkzeug [required: >=0.15, installed: 1.0.1]
  - SQLAlchemy [required: >=0.8.0, installed: 1.3.16]
http-client==0.1.22
  - pycurl [required: Any, installed: 7.43.0.5]
  - six [required: Any, installed: 1.14.0]
requests==2.23.0
  - certifi [required: >=2017.4.17, installed: 2020.4.5.1]
  - chardet [required: >=3.0.2,<4, installed: 3.0.4]
  - idna [required: >=2.5,<3, installed: 2.9]
  - urllib3 [required: >=1.21.1,<1.26,!=1.25.1,!=1.25.0, installed: 1.25.9]
WTForms==2.2.1

```

4-9 将模型映射到数据库中

```
from app.models.book import db
    
    db.init(app)
```

```
pipenv install cymysql
```

```
SQLALCHEMY_DATABASE_URI =
```

```
def create_app():
    app = Flask(__name__)
    app.config.from_object('app.secure')
    app.config.from_object('app.setting')
    register_blueprint(app)

    db.init_app(app)
    db.create_all()
    return app
```

```
RuntimeError: No application found. Either work inside a view function or push an application context.
```



4-10 ORM与CodeFirst区别

```
db.create_all(app=app）

## MVC model 业务逻辑放M层
```



5-1 flask中经典错误 working outside application context

```
current_app
--LocalProxy()

```

```
request
--LocalProxy()
```



5-2 AppContext、RequestContext、Flask与Request之间的关系

```
应用上下文对象
	AppContext 
请求上下文对象 
	RequestContext 
	
	localProxy provide a indriect method to manipulate a Context object
	
	
```

5-3 详解flask上下文与出入栈

![image-20200422140551654](README_img/image-20200422140551654.png)

```
stack LIFO
queue FIFO

# get AppContext Object 
ctx= app.app_context()
# push object to stack
ctx.push()

## offline application & unit test 
```



5-4 flask上下文与with语句

```
#实现了上下文协议的对象使用with
#上下文管理器
# __enter__  __exit__
#上下文表达式必须要返回一个上下文管理器

```

```
class A:
	def __enter__(self):
			a = 1
			return a
			
	def __exit__(self):
			b = 2
			
with A() as obj_A:
	pass
	  
```

5-5 详解上下文管理器的__exit__方法

```
exc_type,exc_value,tb
```

5-6 阅读源码解决db.create_all的问题

```

```

6-1 什么是进程

```
进程调度
挂起算法

操作系统原理

```

6-2 线程的概念

```
更小单元
灵活 小巧 轻便
进程：分配资源
线程：属于进程，利用CPU执行代码，访问进程资源
```

6-3,6-4 多线程的优势与好处

```

```

7-1 ViewModel的基本概念

![image-20200422153459531](README_img/image-20200422153459531.png)

裁剪；修饰；合并

7-2 使用ViewModel处理书籍数据 上

7-3 使用ViewModel处理书籍数据 下

7-4 伪面向对象：披着面向对象外衣的面向过程

```
# 描述特征 （类变量、实例变量）
# 行为	（方法）

```

7-5 重构鱼书核心对象：YuShuBook 上

7-5 重构鱼书核心对象：YuShuBook 下

```

```

7-7 从json序列化看代码解释权反转

```
python 不能直接序列化一个对象

```

![image-20200422161557388](README_img/image-20200422161557388.png)

```
json.dumps(books, default=lambda obj: obj.__dict__)
```

7-8 详解单页面与网站的区别

 ![image-20200422162420053](README_img/image-20200422162420053.png)



多页面

![image-20200422162516347](README_img/image-20200422162516347.png)



单页面：数据填充,模板渲染 在客户端进行; AJAX

![image-20200422162718871](README_img/image-20200422162718871.png)



8-1 静态文件访问原理

```
static
```

8-2 模板文件的位置与修改方案

```
render_template()

项目层级
蓝图层级
```

8-3 Jinja2的概念

```
template language
```

8-4 在Jinja2中读取字典和对象

```
{{ data.age}}
```

8-5 流程控制语句 if

```
{% if ... == 18: %}

{% elif %}
{% else %}

{% endif%}
```

8-6 流程控制语句 for in 循环

```
{% for ... iin %}
{% endfor %}
```

8-7 使用模板继承

```
{%extends ' .html'%}
{{super()}}

{%block head %}
{%endcontent %}


```



8-8 过滤器与管道命令

```
{{data,name | default('未名')}}

|  : linux tunnel command
```

8-9 反向构建URL

```
herf = {{url_for(‘  ’  )， filename = 'text.css'}} 

```

8-10 消息闪现、SecretyKey与变量作用域

```
flash messages

{% set msg = get_flashed_message() %}

secret_key

变量作用域: with endwith
```

8-11 显示搜索结果页面

```
http://localhost:5000/book/search

flash('搜索的关键字不符合要求，请重新输入关键字')
```

8-12 页面结构解析

```
 <form class="form-inline" action="{{ url_for('web.search') }}" method="get">
                <div class="flex-vertical-center-height">
                    <div class="col-md-2">
                        <img src="{{url_for('static', filename='images/logo-yushu.png')}}"/>
                    </div>
                    <div style="margin-left:30px;" class="col-md-8 input-group">
                        <input name="q" type="text" placeholder="ISBN、图书名称"
                               class="form-control input-sm">
                        <span class="input-group-btn">
                            <input class="btn btn-search" type="submit" value="搜索"/>
                        </span>
                    </div>
                </div>
            </form>
```

9-1 viewmodel意义的体现与filter函数的巧妙应用

```
    @property
    def intro(self):
        intros = filter(lambda x: True if x else False,
                        [self.author, self.publisher, self.price])
        return ' / '.join(intros)

```

9-2 书籍详情页面业务逻辑分析

![image-20200424154959413](README_img/image-20200424154959413.png)

9-3 实现书籍详情页面

```
   yushu_book.py
   
   @property
    def first(self):
        return self.books[0] if self.total >= 1 else None
```

9-4 模型与模型关系

```
   from sqlalchemy import Column, String, Integer, ForeignKey, Boolean
   uid = Column(Integer, ForeignKey('user.id'), nullable=False)
```

9-5 自定义基类模型

```
# status used for soft remove
class Base(db.Model):
    __abstract__ = True
    create_time = Column('create_time', Integer)
    status = Column(SmallInteger, default=1)
    
 class Gift(Base):
    __tablename__ = 'gift'

    id = Column(Integer, primary_key=True)
    uid = Column(Integer, ForeignKey('user.id'), nullable=False)
    user = relationship('User')
    isbn = Column(String(13))
    launched = Column(Boolean, default=False)
```



9-6 用户注册

```
 __abstract__ = True #避免默认注册表
 
 http://0.0.0.0:5000/register
 
get 访问
post 提交表单
```

