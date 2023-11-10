import flask

from .config import secret_key

app = flask.Flask(__name__)
app.config.update(
    SECRET_KEY=secret_key,
)

for module in ("front", "api"):
    module = __import__(f"src.{module}", fromlist=["bp"])
    app.register_blueprint(module.bp)
