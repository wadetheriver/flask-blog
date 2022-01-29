from flask import Flask, render_template, request, \
    flash, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import psycopg2
from forms import RegistrationForm, ArticleForm
from passlib.hash import sha256_crypt
# import os
from sqlalchemy import func, exc
from util import requires_login

app = Flask(__name__)
# basedir = os.path.abspath(os.path.dirname(__file__))
app.secret_key = 'replacethisinproction'

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:root@localhost/f_blog"
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'f_blog.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)
ma = Marshmallow(app)


# not certain if func()now is gonna work
class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    subtitle = db.Column(db.String(255))
    excerpt = db.Column(db.String(255))
    body = db.Column(db.String())
    created_date = db.Column(db.DateTime(timezone=True),
                             default=func.now())
    updated_date = db.Column(db.DateTime(timezone=True),
                             default=func.now())
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'), nullable=False)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    register_date = db.Column(db.DateTime(timezone=True),
                              default=func.now())
    articles = db.relationship('Article', backref='user', lazy='joined')


class ArticleSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Article
        # include_relationships = True
        # load_instance = True


article_schema = ArticleSchema()
articles_schema = ArticleSchema(many=True)


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        include_relationships = True
        load_instance = True


user_schema = UserSchema()
users_schema = UserSchema(many=True)


@app.route('/')
def index():  # put application's code here
    return render_template('home.html')


@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html')


@app.route('/articles/<article_id>', methods=['GET'])
def get_article(article_id):
    fetched_article = Article.query.get(article_id)
    lazy_user = user_schema.dump(fetched_article.user)
    lazy_user['password'] = 'Nothing to see here'
    ds_article = article_schema.dump(fetched_article)
    ds_article['author'] = lazy_user

    return ds_article


@app.route('/articles', methods=['GET'])
def get_articles():
    fetched_articles = Article.query.all()
    ds_articles = articles_schema.dump(fetched_articles)
    # print(ds_articles)
    return render_template('articles.html', articles=ds_articles)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        new_user = User(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            username=form.username.data,
            email=str(form.email.data).lower(),
            password=sha256_crypt.encrypt(str(form.password.data))
        )
        db.session.add(new_user)
        try:
            db.session.commit()
        except exc.SQLAlchemyError as e:
            print(type(e))
            flash('An error has occurred.', 'warning')
            return render_template('register.html', form=form)

        flash(f'Welcome to the community {form.first_name.data}!', 'success')
        return redirect(url_for('login'))

    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_email = str(request.form['email']).lower()
        password_candidate = request.form['password']

        # Flask sqlAchemy query
        user = User.query.filter_by(email=user_email).first()
        if user is not None:
            password = user.password
            if sha256_crypt.verify(password_candidate, password):
                session['logged_in'] = True
                session['username'] = user.username
                session['user_id'] = user.id
                flash('You are now logged in!', 'success')
                return redirect(url_for('dashboard'))
            else:
                app.logger.info('PASSWORDS DO NOT MATCH')
                error = "Invalid Password!"
                return render_template('login.html', error=error)
        else:
            error = "User Not Found!"
            return render_template('login.html', error=error)

    return render_template('login.html')


@app.route('/logout')
def logout():
    # define a db table to track logged in users...
    session.clear()
    flash('You have been logged out!', 'success')
    return redirect(url_for('login'))


@app.route('/dashboard', methods=['GET'])
@requires_login
def dashboard():
    # Unsure if i need to pass session here
    return render_template('dashboard.html', session=session)


@app.route('/add_article', methods=['GET', 'POST'])
@requires_login
def create_article():
    form = ArticleForm(request.form)
    if request.method == 'POST' and form.validate():
        new_article = Article(
            title=form.title.data,
            subtitle=form.subtitle.data,
            excerpt=form.excerpt.data,
            body=form.body.data,
            user_id=session['user_id']

        )
        db.session.add(new_article)
        try:
            db.session.commit()
        except exc.SQLAlchemyError as e:
            print(type(e))
            flash('An error has occurred.', 'warning')
            return render_template('add_article.html', form=form)

        flash(f'Your article has been created!', 'success')
        return redirect(url_for('get_articles'))

    return render_template('add_article.html', form=form)


if __name__ == '__main__':
    app.run()
