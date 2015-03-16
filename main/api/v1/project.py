# coding: utf-8

from __future__ import absolute_import

from google.appengine.ext import ndb
from flask.ext import restful

from api import helpers
import model
import util

from main import api


@api.resource('/api/v1/project/', endpoint='api.projects')
class ProjectsAPI(restful.Resource):
  def get(self):
    project_keys = util.param('project_keys', list)
    if project_keys:
      project_db_keys = [ndb.Key(urlsafe=k) for k in project_keys]
      project_dbs = ndb.get_multi(project_db_keys)
      return helpers.make_response(project_dbs, model.Project.FIELDS)

    project_dbs, project_cursor = model.Project.get_dbs()
    return helpers.make_response(project_dbs, model.Project.FIELDS, project_cursor)


@api.resource('/api/v1/project/<int:project_id>/', endpoint='api.project')
class ProjectAPI(restful.Resource):
  def get(self, project_id):
    project_db = model.Project.get_by_id(project_id)
    if not project_db:
      helpers.make_not_found_exception('Project %s not found' % project_id)
    return helpers.make_response(project_db, model.Project.FIELDS)
