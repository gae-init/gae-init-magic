# coding: utf-8

from datetime import datetime
import flask
import requests
import requests_toolbelt.adapters.appengine

import config
import util

# Enable requests compatibility with GAE (needed for authlib)
# From https://toolbelt.readthedocs.io/en/latest/adapters.html#appengineadapter
requests_toolbelt.adapters.appengine.monkeypatch()

class GaeRequest(flask.Request):
  trusted_hosts = config.TRUSTED_HOSTS


app = flask.Flask(__name__)
app.config.from_object(config)
app.request_class = GaeRequest if config.TRUSTED_HOSTS else flask.Request

app.jinja_env.line_statement_prefix = '#'
app.jinja_env.line_comment_prefix = '##'
app.jinja_env.globals.update(
  check_form_fields=util.check_form_fields,
  datetime=datetime,
  is_iterable=util.is_iterable,
  slugify=util.slugify,
  update_query_argument=util.update_query_argument,
  camel_to_snake=util.camel_to_snake,
)

import auth
import control
import model
import task

from api import helpers

api_v1 = helpers.Api(app, prefix='/api/v1')

import api.v1

if config.DEVELOPMENT:
  from werkzeug import debug
  try:
    app.wsgi_app = debug.DebuggedApplication(
      app.wsgi_app, evalex=True, pin_security=False,
    )
  except TypeError:
    app.wsgi_app = debug.DebuggedApplication(app.wsgi_app, evalex=True)
  app.testing = False
