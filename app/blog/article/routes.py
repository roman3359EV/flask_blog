from flask import render_template, Response, request
from flask_login import current_user
from . import article_routes
from ..models import User, Category, Article, Access, Tag, cache


@article_routes.route('/articles', methods=['GET'])
def articles() -> str | Response:
    dict_user = {
        'name': current_user.name if current_user.is_authenticated else '',
        'login': current_user.login if current_user.is_authenticated else '',
        'balance': User.get_balance(current_user),
    }

    if cache.has('categories_all'):
        categories_all = cache.get('categories_all')
    else:
        categories_all = Category.query.all()
        cache.set('categories_all', categories_all)

    return render_template('articles.html', user=dict_user, categories=categories_all)


@article_routes.route('/category/<category_id>', methods=['GET'])
def category(category_id: int) -> str:
    dict_user = {
        'name': current_user.name if current_user.is_authenticated else '',
        'login': current_user.login if current_user.is_authenticated else '',
        'balance': User.get_balance(current_user),
    }

    page = int(request.args.get('page')) if request.args.get('page') else 1
    category_current = Category.query.filter_by(id=category_id).first()

    articles_all = Article \
        .query \
        .filter_by(category_id=category_id) \
        .order_by(Article.id.asc()) \
        .paginate(page=page, per_page=Article.PER_PAGE)

    return render_template('category.html', user=dict_user, category=category_current, articles=articles_all)


@article_routes.route('/tags', methods=['GET'])
def tags() -> str:
    dict_user = {
        'name': current_user.name if current_user.is_authenticated else '',
        'login': current_user.login if current_user.is_authenticated else '',
        'balance': User.get_balance(current_user),
    }

    if cache.has('tags_all'):
        tags_all = cache.get('tags_all')
    else:
        tags_all = Tag.query.all()
        cache.set('tags_all', tags_all)

    return render_template('tags.html', user=dict_user, tags=tags_all)


@article_routes.route('/tag/<alias>', methods=['GET'])
def tag(alias: str) -> str:
    dict_user = {
        'name': current_user.name if current_user.is_authenticated else '',
        'login': current_user.login if current_user.is_authenticated else '',
        'balance': User.get_balance(current_user),
    }

    tag_current = Tag.query.filter_by(alias=alias).first()

    return render_template('tag.html', user=dict_user, tag=tag_current)


@article_routes.route('/article/<article_id>', methods=['GET'])
def article(article_id: int) -> str:
    current_article = Article.query \
        .filter_by(id=article_id) \
        .first()

    dict_user = {
        'name': current_user.name if current_user.is_authenticated else '',
        'login': current_user.login if current_user.is_authenticated else '',
        'balance': User.get_balance(current_user),
        'access': Access.is_access(current_article, current_user)
    }

    return render_template('article.html', user=dict_user, article=current_article)
