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

@app.route('/new-post', methods=['POST', 'GET'])
def new_post():

    title_error = ''
    body_error = ''

    if request.method == 'POST':
        post_title = request.form['post_title']
        post_body = request.form['post_body']
        new = Blog(post_title, post_body)
        db.session.add(new)
        db.session.commit()
        if post_title == '':
            title_error = 'Please enter a Post Title.'
        elif body_error == '':
            body_error = 'Please enter some content.'
        else:
            return redirect('/blog')

    return render_template('new-post.html', title="New Post", title_error=title_error,
                body_error=body_error)

if __name__ == '__main__':
    app.run()
