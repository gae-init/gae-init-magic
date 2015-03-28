# coding: utf-8

from __future__ import absolute_import

from flask.ext import restful
import flask

from api import helpers
import model

from main import api_v1


@api_v1.resource('/project/<int:project_id>/model/<int:model_id>/property/', endpoint='api.properties')
class PropertiesAPI(restful.Resource):
  def get(self, project_id, model_id):
    project_db = model.Project.get_by_id(project_id)
    if not project_db:
      flask.abort(404)

    model_db = model.Model.get_by_id(model_id, parent=project_db.key)
    if not model_db:
      flask.abort(404)

    property_dbs, property_cursor = model_db.get_property_dbs()
    return helpers.make_response(property_dbs, model.Property.FIELDS, property_cursor)


@api_v1.resource('/project/<int:project_id>/model/<int:model_id>/property/<int:property_id>/', endpoint='api.property')
class PropertyAPI(restful.Resource):
  def get(self, project_id, model_id, property_id):
    project_db = model.Project.get_by_id(project_id)
    if not project_db:
      flask.abort(404)

    model_db = model.Model.get_by_id(model_id, parent=project_db.key)
    if not model_db:
      flask.abort(404)

    property_db = model.Property.get_by_id(property_id, parent=model_db.key)
    if not property_db:
      helpers.make_not_found_exception('Property %s not found' % property_id)
    return helpers.make_response(property_db, model.Property.FIELDS)
