
# model backrefs set to lazy, separate query is made for users
# @app.route('/articles/<article_id>', methods=['GET'])
# def get_article(article_id):
#     fetched_article = Article.query.get(article_id)
#     lazy_user = user_schema.dump(fetched_article.user)
#     ds_article = article_schema.dump(fetched_article)
#     ds_article['author'] = lazy_user
#     return ds_article