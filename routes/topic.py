from flask import (
    render_template,
    request,
    redirect,
    url_for,
    Blueprint,
    abort,
)
from utils import log
from routes import *
from models.topic import Topic
from models.board import Board


main = Blueprint('topic', __name__)


import uuid
csrf_tokens = dict()
@main.route("/")
def index():
    # board_id = 2
    board_id = int(request.args.get('board_id', -1))
    if board_id == -1:
        #ms = Topic.cache_all()
        ms = Topic.all_delay()
    else:
        #ms = Topic.cache_find(board_id)
        ms = Topic.find_all(board_id=board_id)
    token = str(uuid.uuid4())
    u = current_user()
    csrf_tokens[token] = u.id
    bs = Board.all()
    bs = [result for result in bs if result.deleted is False]
    image = u.user_image
    zero_replies = [result for result in ms if len(result.replies()) == 0]
    return render_template("topic/index.html",
                           image=image,
                           ms=ms,
                           token=token,
                           bs=bs,
                           zero_replies=zero_replies)


@main.route('/<int:id>')
def detail(id):
    m = Topic.get(id)
    user = m.user()
    # 传递 topic 的所有 reply 到 页面中
    # t = int(time.time())
    # m.passed_time = t - m.created_time
    m.username = m.user().username
    return render_template("topic/detail.html", topic=m, user=user)


@main.route("/add", methods=["POST"])
def add():
    form = request.form
    u = current_user()
    m = Topic.new(form, user_id=u.id)
    # for i in range(1000):
    #     m = Topic.new(form, user_id=u.id)
    return redirect(url_for('.detail', id=m.id))


@main.route("/delete")
def delete():
    id = int(request.args.get('id'))
    uid = int(request.args.get('uid'))
    # log('id', type(id))
    token = request.args.get('token')
    # log("token", token)
    u = current_user()
    # 判断 token 是否是我们给的
    if token in csrf_tokens and csrf_tokens[token] == u.id and uid == u.id:
        log(1)
        csrf_tokens.pop(token)
        if u is not None:
            # log('删除 topic 的用户是', u, id)
            Topic.delete(id)
            return redirect(url_for('.index'))
        else:
            abort(404)
    else:
        abort(403)


@main.route("/new")
def new():
    bs = Board.all()
    bs = [result for result in bs if result.deleted is False]

    return render_template("topic/new.html", bs=bs)


@main.route("/profile/<int:id>")
def profile(id):
    # id = int(request.args.get('id'))"
    t = Topic.get(id)
    # log('uuu', type(id), id, t)
    user = t.user()
    return render_template("topic/profile.html", user=user)

