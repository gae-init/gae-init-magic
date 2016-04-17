# coding: utf-8

from __future__ import absolute_import

from google.appengine.ext import ndb

from api import fields
import model
import util


class Project(model.Base):
  user_key = ndb.KeyProperty(kind=model.User, required=True)
  name = ndb.StringProperty(required=True)
  description = ndb.StringProperty(default='')
  url = ndb.StringProperty(default='', verbose_name='URL')
  public = ndb.BooleanProperty(default=False, verbose_name='Make this project publicly accessible')
  access = ndb.StringProperty(default=util.uuid()[:4], verbose_name='Access Code')
  model_count = ndb.IntegerProperty(default=0)
  include_babel = ndb.BooleanProperty(default=False, verbose_name='Include Babel (Experimental)')

  @ndb.ComputedProperty
  def variable_name(self):
    return util.camel_to_snake(self.name.replace(' ', '')).replace('_', '-')

  def get_model_dbs(self, **kwargs):
    return model.Model.get_dbs(
        ancestor=self.key,
        order=util.param('order') or 'rank',
        **kwargs
      )

  def get_model_by_variable_name(self, variable_name):
    model_qry = model.Model.query(ancestor=self.key)
    model_qry = model_qry.filter(model.Model.variable_name == variable_name)
    return model_qry.get()

  @classmethod
  def _pre_delete_hook(cls, key):
    project_db = key.get()
    model_keys, _null = project_db.get_model_dbs(keys_only=True, limit=-1)
    ndb.delete_multi(model_keys)

  FIELDS = {
      'access': fields.String,
      'description': fields.String,
      'model_count': fields.Integer,
      'name': fields.String,
      'public': fields.Boolean,
      'url': fields.String,
      'user_key': fields.Key,
      'variable_name': fields.String,
    }

  FIELDS.update(model.Base.FIELDS)


