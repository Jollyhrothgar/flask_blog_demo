from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for

from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('blog', __name__)

@bp.route('/')
def index():
    """
    Selects all posts, ordered by creation date, and then returns them rendered
    in the blog template.
    """
    db = get_db()
    posts = db.execute(
        """
        SELECT
            p.id,
            title,
            body,
            created,
            author_id,
            username
        FROM
            post AS p
        JOIN
            user AS u
            ON p.author_id = u.id
        ORDER BY
            created
        DESC
        """
    ).fetchall()

    return render_template('blog/index.html', posts=posts)

@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    """
    Grabs the input from the form for creating a post and extracts these
    attributes from the post-request.

    This is a one-and-done method - no auto-save or nothin' if the post request
    fails, you lose the content.
    """
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                """
                INSERT INTO post
                    (title, body, author_id)'
                VALUES
                    (?, ?, ?)
                """,
                (title, body, g.user['id'])
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/create.html')

def get_post(id, check_author=True):
    """
    This is a helper function which simply grabs a post by ID given an
    author_id. It is re-used any time we need to get a post for some reason.

    The post is grabbed before we check to see if the author is logged in for
    situations where one might want to write a view where you show an
    individual post on a page in the case where logged in user doesn't matter.
    """
    post = get_db().execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if post is None:
        abort(404, "Post id {0} doesn't exist.".format(id))

    if check_author and post['author_id'] != g.user['id']:
        abort(403)

    return post

@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    """
    Given a post id, extract the post contents from the form and update the
    database with the post contents.
    """

    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                """
                UPDATE post SET title = ?, body = ?
                WHERE id = ?
                """,
                (title, body, id)
            )

            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/update.html', post=post)

@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    """
    Given a post id, we re-use the post function to return an error in the case
    where we try delete a post that doesn't exist. No need to capture the
    return value, because if it exists, we're going to delete it, and existance
    is the only condition where an HTTP response is NOT returned.
    """
    get_post(id)

    db = get_db()
    db.execute('DELETE FROM post WHERE id = ?', (id,))
    db.commit()

    return redirect(url_for('blog.index'))

