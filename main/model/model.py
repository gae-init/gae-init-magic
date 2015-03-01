# coding: utf-8

from __future__ import absolute_import

from google.appengine.ext import ndb

from api import fields
import model
import util


class Model(model.Base):
  name = ndb.StringProperty(required=True)
  verbose_name = ndb.StringProperty(default='')
  icon = ndb.StringProperty(default='list')
  property_count = ndb.IntegerProperty(default=0)
  rank = ndb.IntegerProperty(default=0)
  auth_user_key = ndb.KeyProperty(kind=model.Property, verbose_name='User Authentication with')
  admin_only = ndb.BooleanProperty(default=False, verbose_name='Only for Admins')
  title_property_key = ndb.KeyProperty(verbose_name='Title Property')

  @ndb.ComputedProperty
  def variable_name(self):
    return util.camel_to_snake(self.name)

  @ndb.ComputedProperty
  def css_name(self):
    return util.camel_to_snake(self.name).replace('_', '-')

  @ndb.ComputedProperty
  def default_verbose_name(self):
    return util.camel_to_verbose(self.name)

  @ndb.ComputedProperty
  def auth_user_key_property(self):
    return ndb.Key(urlsafe=self.auth_user_key.urlsafe()).get().name if self.auth_user_key else None

  @ndb.ComputedProperty
  def verbose_name_(self):
    return self.verbose_name or self.default_verbose_name

  def get_title_property(self):
    if self.title_property_key:
      return self.title_property_key.get().name
    return None

  def get_property_dbs(self, **kwargs):
    return model.Property.get_dbs(
        ancestor=self.key,
        order=util.param('order') or 'rank',
        **kwargs
      )

  FIELDS = {
      'admin_only': fields.Boolean,
      'auth_user_key_property': fields.String,
      'auth_user_key': fields.Key,
      'css_name': fields.String,
      'default_verbose_name': fields.String,
      'icon': fields.String,
      'name': fields.String,
      'property_count': fields.Integer,
      'rank': fields.Integer,
      'title_property_key': fields.Key,
      'variable_name': fields.String,
      'verbose_name_': fields.String,
      'verbose_name': fields.String,
    }

  FIELDS.update(model.Base.FIELDS)
