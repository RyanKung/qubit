import flask
from qubit.config import STATIC_PATH, STATIC_URL
__all__ = ['app']

app = flask.Flask(
    'qubit',
    static_url_path=STATIC_URL,
    static_folder=STATIC_PATH)
