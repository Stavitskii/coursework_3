import logging
from json import JSONDecodeError

from flask import Blueprint, render_template, request, abort
from app.posts.dao.posts_dao import PostsDAO
from app.posts.dao.comments_dao import CommentsDao

posts_blueprint = Blueprint('posts_blueprint', __name__, template_folder='templates')
posts_dao = PostsDAO("data/posts.json")
comments_dao = CommentsDao("data/comments.json")

logger = logging.getLogger("basic")


@posts_blueprint.route('/')
def posts_all():
    logger.debug("All posts asked")
    try:
        posts = posts_dao.get_all()
        return render_template("index.html", posts=posts)
    except:
        return "Something is wrong"


@posts_blueprint.route('/posts/<int:post_pk>')
def posts_one(post_pk):
    logger.debug(f"Post {post_pk} asked")
    try:
        post = posts_dao.get_by_pk(post_pk)
        comments = comments_dao.get_by_post_pk(post_pk)
        number_of_comments = len(comments)
    except (JSONDecodeError, FileNotFoundError) as error:
        return render_template("error.html", error=error)
    except BaseException as e:
        return render_template("error.html", error="Undefined error")
    else:
        if post is None:
            abort(404)
        return render_template("post.html", post=post, comments=comments, number_of_comments=number_of_comments)


@posts_blueprint.errorhandler(404)
def post_error(e):
    return "No post is found", 404


@posts_blueprint.route('/search/')
def posts_search():
    query = request.args.get("s", None)
    #    if query is not None:
    #        posts = posts_dao.search(query)
    #        number_of_posts = len(posts)
    #    else:
    #        posts = []
    #        number_of_posts = 0

    if query is None or len(query) < 1:
        posts = []
        number_of_posts = 0
    else:
        posts = posts_dao.search(query)
        number_of_posts = len(posts)

    return render_template("search.html", query=query, posts=posts, number_of_posts=number_of_posts)


@posts_blueprint.route('/users/<username>/')
def posts_by_user(username):
    posts = posts_dao.get_by_user(username)
    number_of_posts = len(posts)
    return render_template("user-feed.html", posts=posts, number_of_posts=number_of_posts)
