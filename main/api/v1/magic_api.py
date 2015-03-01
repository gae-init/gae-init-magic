# coding: utf-8

import flask

import config
import model

from main import app


@app.route('/api/v1/project/<int:project_id>/magic/main/<what>/<variable_name>.py')
def generate_python_modules(project_id, what, variable_name):
  if what not in ['control', 'model']:
    flask.abort(404)
  project_db = model.Project.get_by_id(project_id)
  if not project_db:
    flask.abort(404)

  if '__init__.py' in flask.request.path:
    model_dbs, model_cursor = project_db.get_model_dbs()
    response = flask.make_response(flask.render_template(
        'generated/%s_init.py' % what,
        project_db=project_db,
        model_dbs=model_dbs,
      ))
  else:
    model_db = project_db.get_model_by_variable_name(variable_name)
    if not model_db:
      flask.abort(404)
    property_dbs, property_cursor = model_db.get_property_dbs(limit=config.MAX_DB_LIMIT)
    response = flask.make_response(flask.render_template(
        'generated/%s.py' % what,
        project_db=project_db,
        model_db=model_db,
        property_dbs=property_dbs,
      ))

  response.headers['Content-Type'] = 'text/plain'
  return response


@app.route('/api/v1/project/<int:project_id>/magic/main/templates/<path:path>')
def generate_bits(project_id, path):
  project_db = model.Project.get_by_id(project_id)
  if not project_db:
    flask.abort(404)
  model_dbs, model_cursor = project_db.get_model_dbs()
  response = flask.make_response(flask.render_template(
      'generated/%s' % path,
      project_db=project_db,
      model_dbs=model_dbs,
    ))
  response.headers['Content-Type'] = 'text/plain'
  return response


@app.route('/api/v1/project/<int:project_id>/magic/main/templates/<directory>/<variable_name>_<what>.html')
@app.route('/api/v1/project/<int:project_id>/magic/main/templates/<directory>/admin_<variable_name>_<what>.html')
def generate_templates(project_id, directory, variable_name, what):
  if directory != variable_name:
    flask.abort(404)

  project_db = model.Project.get_by_id(project_id)
  if not project_db:
    flask.abort(404)

  model_db = project_db.get_model_by_variable_name(variable_name)
  if not model_db:
    flask.abort(404)

  property_dbs, property_cursor = model_db.get_property_dbs(limit=config.MAX_DB_LIMIT)

  path = 'generated/%s.html' % what
  if '/admin_' in flask.request.path:
    path = 'generated/admin_%s.html' % what

  response = flask.make_response(flask.render_template(
      path,
      project_db=project_db,
      model_db=model_db,
      property_dbs=property_dbs,
    ))

  response.headers['Content-Type'] = 'text/plain'
  return response
