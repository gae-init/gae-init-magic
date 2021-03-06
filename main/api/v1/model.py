# coding: utf-8

from __future__ import absolute_import

import flask_restful
import flask

from api import helpers
import model

from main import api_v1


@api_v1.resource('/project/<int:project_id>/model/', endpoint='api.models')
class ModelsAPI(flask_restful.Resource):
  def get(self, project_id):
    project_db = model.Project.get_by_id(project_id)
    if not project_db:
      flask.abort(404)

    model_dbs, model_cursor = project_db.get_model_dbs()
    return helpers.make_response(model_dbs, model.Model.FIELDS, model_cursor)


@api_v1.resource('/project/<int:project_id>/model/<int:model_id>/', endpoint='api.model')
class ModelAPI(flask_restful.Resource):
  def get(self, project_id, model_id):
    project_db = model.Project.get_by_id(project_id)
    if not project_db:
      flask.abort(404)

    model_db = model.Model.get_by_id(model_id, parent=project_db.key)
    if not model_db:
      helpers.make_not_found_exception('Model %s not found' % model_id)
    return helpers.make_response(model_db, model.Model.FIELDS)
