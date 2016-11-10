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
  public_view = ndb.BooleanProperty(default=False)
  title_property_key = ndb.KeyProperty(verbose_name='Title Property')
  default_order = ndb.StringProperty(default='')

  @ndb.ComputedProperty
  def variable_name(self):
    return util.camel_to_snake(self.name)

  @ndb.ComputedProperty
  def variable_name_camel(self):
    return util.lower_first(self.name)

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

  @ndb.ComputedProperty
  def show_in_header(self):
    return not self.admin_only or self.public_view

  @classmethod
  def get_dbs(cls, order=None, **kwargs):
    return super(Model, cls).get_dbs(
      order=util.param('order') or 'rank',
      **kwargs
    )

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

  def get_property_key_choices(self, admin=False):
    model_names = []
    model_dbs, model_cursor = self.key.parent().get().get_model_dbs()
    property_dbs, property_cursor = self.get_property_dbs()
    for property_db in property_dbs:
      kind = property_db.kind.replace('model.', '')
      if kind and kind not in model_names:
        model_names.append(kind)

    result = ''
    for model_name in model_names:
      variable_name = util.camel_to_snake(model_name)
      user_specific = ''
      for model_db in model_dbs:
        if model_db.name == model_name and model_db.auth_user_key_property and not model_db.public_view:
          user_specific = ', %s=auth.current_user_key()' % model_db.auth_user_key_property
          break
      result += '  %s_dbs, %s_cursor = model.%s.get_dbs(limit=-1%s)\n' % (variable_name, variable_name, model_name, user_specific)

    for property_db in property_dbs:
      # For showing in user update
      if not admin and not (property_db.wtf_property and property_db.show_on_update):
        continue

      # For showing in admin update
      if admin and not (property_db.wtf_property and property_db.show_on_admin_update):
        continue

      kind = property_db.kind.replace('model.', '')
      if kind in model_names:
        result += '  form.%s.choices = ' % property_db.name
        if not property_db.required:
          result += u"[('', u'-')] + "
        model_name = util.camel_to_snake(property_db.kind.replace('model.', ''))

        title = 'key.id()'
        if kind == 'User':
          title = 'name'
        else:
          for model_db in model_dbs:
            if model_db.name == kind and model_db.title_property_key:
              title = model_db.title_property_key.get().name

        result += '[(c.key.urlsafe(), c.%s) for c in %s_dbs]' % (title, model_name)
        result += '\n'

    return result

  @ndb.ComputedProperty
  def get_child_get_dbs(self):
    result = ''
    for model_db in self.get_dbs(ancestor=self.key.parent())[0]:
      property_dbs = model_db.get_property_dbs(ndb_property='ndb.KeyProperty', kind='model.%s' % self.name)[0]
      if property_dbs:
        result += ('\n'
          '  def get_%s_dbs(self, **kwargs):\n'
          '    return model.%s.get_dbs(%s=self.key, **kwargs)\n'
          % (model_db.variable_name, model_db.name, property_dbs[0].name)
        )
    return result

  @ndb.ComputedProperty
  def get_child_dbs_names(self):
    result = []
    for model_db in self.get_dbs(ancestor=self.key.parent())[0]:
      property_dbs = model_db.get_property_dbs(ndb_property='ndb.KeyProperty', kind='model.%s' % self.name)[0]
      if property_dbs:
        result.append(model_db.variable_name)
    return result

  def get_child_dbs(self):
    result = []
    for model_db in self.get_dbs(ancestor=self.key.parent())[0]:
      property_dbs = model_db.get_property_dbs(ndb_property='ndb.KeyProperty', kind='model.%s' % self.name)[0]
      if property_dbs:
        result.append(model_db)
    return result

  @classmethod
  def _pre_delete_hook(cls, key):
    model_db = key.get()
    property_keys, _null = model_db.get_property_dbs(keys_only=True, limit=-1)
    ndb.delete_multi(property_keys)

  FIELDS = {
      'admin_only': fields.Boolean,
      'auth_user_key_property': fields.String,
      'auth_user_key': fields.Key,
      'css_name': fields.String,
      'default_verbose_name': fields.String,
      'icon': fields.String,
      'name': fields.String,
      'property_count': fields.Integer,
      'public_view': fields.Boolean,
      'rank': fields.Integer,
      'title_property_key': fields.Key,
      'variable_name': fields.String,
      'verbose_name_': fields.String,
      'verbose_name': fields.String,
      'default_order': fields.String,
    }

  FIELDS.update(model.Base.FIELDS)
