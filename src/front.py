import flask

from . import items

bp = flask.Blueprint("front", __name__)


@bp.route("/")
def index():
    inventory = items.get_inventory()
    return flask.render_template("index.html", inventory=inventory)


@bp.post("/token")
def save_token():
    token = flask.request.form.get("token")
    if not token:
        return flask.abort(400)
    # Save the token in a cookie
    resp = flask.make_response(flask.redirect("/"))
    resp.set_cookie("token", token)
    flask.flash("Token saved!")
    return resp
