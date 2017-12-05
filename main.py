from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:buildablog2017@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    post_title = db.Column(db.String(120))
    post_body = db.Column(db.String(25000))

    def __init__(self, title, body):
        self.post_title = title
        self.post_body = body


@app.route('/blog', methods = ['POST','GET'])
def index():

    posts = Blog.query.all()
    return render_template('blog.html', title="Build a Blog", posts=posts)

@app.route('/new-post', methods=['POST'])
def new_post():
    
    if request.method == 'POST':
        post_title = request.form['post_title']
        post_body = request.form['post_body']
        new_post = Blog(post_title, post_body)
        db.session.add(new_post)
        db.session.commit()

    return render_template('new-post.html', title="New Post")

if __name__ == '__main__':
    app.run()
