# coding: utf-8

from __future__ import absolute_import

from google.appengine.ext import ndb
from flask.ext import restful

from api import helpers
import auth
import model

from main import api


@api.resource('/api/v1/admin/upgrade/model/', endpoint='api.admin.upgrade.model')
class AdminUpgradeModelAPI(restful.Resource):
  @auth.admin_required
  def get(self):
    model_dbs, model_cursor = model.Model.get_dbs()
    ndb.put_multi(model_dbs)
    return helpers.make_response(model_dbs, model.Model.FIELDS, model_cursor)


@api.resource('/api/v1/admin/upgrade/property/', endpoint='api.admin.upgrade.property')
class AdminUpgradePropertyAPI(restful.Resource):
  @auth.admin_required
  def get(self):
    property_dbs, property_cursor = model.Property.get_dbs()
    ndb.put_multi(property_dbs)
    return helpers.make_response(property_dbs, model.Property.FIELDS, property_cursor)
