from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'f_blog.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)
ma = Marshmallow(app)


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    body = db.Column(db.String(100))
    author = db.Column(db.String(100))
    create_date = db.Column(db.String(100))


# class Author(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     first_name = db.Column(db.String(100))
#     last_name = db.Column(db.String(100))
#     email = db.Column(db.String(100))
#     password = db.Column(db.String(100))


class ArticleSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Article
        # include_relationships = True
        # load_instance = True


article_schema = ArticleSchema()
articles_schema = ArticleSchema(many=True)


@app.route('/')
def hello_world():  # put application's code here
    return render_template('home.html')


@app.route('/about', methods = ['GET'])
def about():
    return render_template('about.html')


@app.route('/articles/<article_id>', methods=['GET'])
def get_article(article_id):
    fetched_article = Article.query.get(article_id)
    ds_article = article_schema.dump(fetched_article)
    return ds_article

@app.route('/articles', methods=['GET'])
def get_articles():
    fetched_articles = Article.query.all()
    ds_articles = articles_schema.dump(fetched_articles)
    print(ds_articles)
    return render_template('articles.html', articles=ds_articles)


if __name__ == '__main__':
    app.run()
