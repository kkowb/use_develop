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

from models.board import Board


main = Blueprint('board', __name__)


@main.route("/admin")
def index():
    return render_template('board/admin_index.html')
    ...


@main.route("/add", methods=["POST"])
def add():
    form = request.form
    u = current_user()
    if u.id == 1:
        m = Board.new(form)
        return redirect(url_for('topic.index'))
    else:
        return render_template('board/adminError.html')


@main.route("/delete")
def delete():
    id = int(request.args.get('board_id'))
    u = current_user()
    log('iddd', type(id), u.id == 1, u.id)
    if u.id == 1:
        Board.delete(id=id)
        return redirect(url_for('topic.index'))
    else:
        abort(403)

