from flask import Flask, render_template, request, flash, redirect, url_for, session, logging
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import psycopg2
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt

# import os
from sqlalchemy import func

app = Flask(__name__)
# basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:root@localhost/f_blog"
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'f_blog.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)
ma = Marshmallow(app)


# not certain if func()now is gonna work
class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    body = db.Column(db.String())
    author = db.Column(db.String(100))
    create_date = db.Column(db.DateTime(timezone=True),
                            default=func.now())


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    user_name = db.Column(db.String(100))
    password = db.Column(db.String(100))
    register_date = db.Column(db.DateTime(timezone=True),
                              default=func.now())


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


@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html')


@app.route('/articles/<article_id>', methods=['GET'])
def get_article(article_id):
    fetched_article = Article.query.get(article_id)
    ds_article = article_schema.dump(fetched_article)
    return render_template('article.html', article=ds_article)
    # return ds_articles


@app.route('/articles', methods=['GET'])
def get_articles():
    fetched_articles = Article.query.all()
    ds_articles = articles_schema.dump(fetched_articles)
    print(ds_articles)
    return render_template('articles.html', articles=ds_articles)


if __name__ == '__main__':
    app.run()
