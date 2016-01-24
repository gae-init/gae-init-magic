# coding: utf-8

import flask

import config
import model
import util

from main import app


###############################################################################
# Welcome
###############################################################################
@app.route('/')
def welcome():
  project_dbs, project_cursor = model.Project.get_dbs(
      public=True,
      order=util.param('order') or '-created'
    )
  return flask.render_template(
      'welcome.html',
      html_class='welcome',
      project_dbs=project_dbs,
      next_url=util.generate_next_url(project_cursor),
    )


###############################################################################
# Sitemap stuff
###############################################################################
@app.route('/sitemap.xml')
def sitemap():
  response = flask.make_response(flask.render_template(
    'sitemap.xml',
    lastmod=config.CURRENT_VERSION_DATE.strftime('%Y-%m-%d'),
  ))
  response.headers['Content-Type'] = 'application/xml'
  return response


###############################################################################
# Warmup request
###############################################################################
@app.route('/_ah/warmup')
def warmup():
  # TODO: put your warmup code here
  return 'success'
