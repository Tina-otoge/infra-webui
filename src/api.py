import flask

from . import items, password

bp = flask.Blueprint("api", __name__, url_prefix="/api")


@bp.before_request
def check_token():
    token = flask.request.cookies.get("token")
    if not password.check_token(token):
        return flask.abort(401)


@bp.get("/status")
def status_all():
    inventory = items.get_inventory()
    return {name: inventory[name].get_status() for name in inventory}


@bp.get("/items/<name>/start")
def start_item(name):
    inventory = items.get_inventory()
    inventory[name].start()
    return flask.Response(status=200)


@bp.get("/items/<name>/stop")
def stop_item(name):
    inventory = items.get_inventory()
    inventory[name].stop()
    return flask.Response(status=200)
