from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__, static_url_path='/static')
# app.config["DEBUG"] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
db = SQLAlchemy(app)


class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    content = db.Column(db.Text(120), nullable=False)
    author = db.Column(db.String(60),  nullable=False, default="N/A")
    post_time = db.Column(db.DateTime(), nullable=False,
                          default=datetime.utcnow())

    def __repr__(self):
        return '<Blog %r>' % self.id


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(60), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username


posts = [
    {
        'title': 'post1',
        'detail': 'post 1 details ose here',
        'author': 'imran'
    },
    {
        'title': 'post2',
        'detail': 'post 2 details ose here'
    }
]


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/users/<string:user>/')
def users(user):
    return "<h2> hello " + user + " how are you </h2>"


@app.route('/post/', methods=['GET', 'POST'])
def post():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        author = request.form['author']
        new_post = Blog(title=title, content=content, author=author)
        db.session.add(new_post)
        db.session.commit()
        return redirect('/post/')
    else:
        blogs = Blog.query.all()
        return render_template('blog.html', posts=blogs)


if __name__ == '__main__':
    app.run(debug=True)
