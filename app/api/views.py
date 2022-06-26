import logging

from flask import Blueprint, request, jsonify, render_template, request, abort

from app.posts.dao.posts_dao import PostsDAO
from app.posts.dao.comments_dao import CommentsDao


api_blueprint = Blueprint('api_blueprint', __name__)
posts_dao = PostsDAO("data/posts.json")
comments_dao = CommentsDao("data/comments.json")

logger = logging.getLogger("basic")


@api_blueprint.route('/api/posts/')
def posts_all():
    logger.debug("Asked all posts with API")
    posts = posts_dao.get_all()
    return jsonify(posts)


@api_blueprint.route('/api/posts/<int:post_pk>')
def posts_one(post_pk):
    logger.debug(f"Post {post_pk} asked with API")
    post = posts_dao.get_by_pk(post_pk)
    return jsonify(post)



