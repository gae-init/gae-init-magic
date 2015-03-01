# coding: utf-8

from __future__ import absolute_import

from google.appengine.ext import ndb

from api import fields
import model
import util


class Property(model.Base):
  name = ndb.StringProperty(required=True)
  rank = ndb.IntegerProperty(default=0)
  verbose_name = ndb.StringProperty(default='')

  show_on_view = ndb.BooleanProperty(default=True, verbose_name='Show on View')
  show_on_update = ndb.BooleanProperty(default=True, verbose_name='Show on Update')
  show_on_list = ndb.BooleanProperty(default=True, verbose_name='Show on List')
  show_on_admin_update = ndb.BooleanProperty(default=True, verbose_name='Show on Admin Update')
  show_on_admin_list = ndb.BooleanProperty(default=True, verbose_name='Show on Admin List')

  ndb_property = ndb.StringProperty(default='', verbose_name='NDB Property')
  kind = ndb.StringProperty()
  default = ndb.StringProperty()
  required = ndb.BooleanProperty(default=False)
  repeated = ndb.BooleanProperty(default=False)
  indexed = ndb.BooleanProperty(default=True)
  auto_now = ndb.BooleanProperty(default=False)
  auto_now_add = ndb.BooleanProperty(default=False)

  field_property = ndb.StringProperty(default='')

  wtf_property = ndb.StringProperty(default='', verbose_name='WTF Property')
  description = ndb.StringProperty(default='')
  strip_filter = ndb.BooleanProperty(default=False)
  email_filter = ndb.BooleanProperty(default=False)
  sort_filter = ndb.BooleanProperty(default=False)
  choices = ndb.StringProperty()

  forms_property = ndb.StringProperty(default='')
  placeholder = ndb.StringProperty(default='')
  autofocus = ndb.BooleanProperty(default=False)
  readonly = ndb.BooleanProperty(default=False)

  @ndb.ComputedProperty
  def ndb_field(self):
    args = [
        "kind=%s" % self.kind if self.kind else '',
        "default=%s" % self.default if self.default else '',
        "required=True" if self.required else '',
        "repeated=%s" % self.repeated if self.repeated else '',
        "indexed=False" if not self.indexed else '',
        "verbose_name='%s'" % self.verbose_name if self.verbose_name else '',
      ]
    return '%s = %s(%s)' % (
        self.name,
        self.ndb_property,
        ', '.join([arg for arg in args if arg]),
      )

  @ndb.ComputedProperty
  def api_field(self):
    if not self.field_property:
      return ''

    if self.repeated:
      return "'%s': fields.List(%s)," % (self.name, self.field_property)
    return "'%s': %s," % (self.name, self.field_property)

  @ndb.ComputedProperty
  def wtf_field(self):
    required = 'wtforms.validators.%s()' % ('required' if self.required else 'optional')
    validators = '[%s]' % required
    filters = [
        'util.strip_filter' if self.strip_filter else '',
        'util.email_filter' if self.email_filter else '',
        'util.sort_filter' if self.sort_filter else '',
      ]

    filters = [f for f in filters if f]
    filters = '      filters=[%s],\n' % ', '.join(filters) if filters else ''
    description = "      description='%s',\n" % self.description if self.description else ''

    choices = ''
    if self.wtf_property in ['wtforms.RadioField', 'wtforms.SelectField', 'wtforms.SelectMultipleField']:
      choices = '      choices=%s,\n' % (self.choices if self.choices else '[]')

    title = '%r' % self.verbose_name_
    if self.ndb_property:
      title = 'model.%s.%s._verbose_name' % (self.key.parent().get().name, self.name)
    s = (
      '%s = %s(\n'
      '      %s,\n'
      '      %s,\n%s%s%s'
      '    )'
      % (self.name, self.wtf_property, title, validators, filters, choices, description))
    return s

  @ndb.ComputedProperty
  def forms_field(self):
    autofocus = ', autofocus=True' if self.autofocus else ''
    readonly = ', readonly=True' if self.readonly else ''
    placeholder = ", placeholder='%s'" % self.placeholder if self.placeholder else ''
    return "{{%s(form.%s%s%s%s)}}" % (self.forms_property, self.name, autofocus, readonly, placeholder)

  @ndb.ComputedProperty
  def default_verbose_name(self):
    return util.snake_to_verbose(self.name)

  @ndb.ComputedProperty
  def verbose_name_(self):
    return self.verbose_name or self.default_verbose_name

  FIELDS = {
      'auto_now': fields.Boolean,
      'auto_now_add': fields.Boolean,
      'autofocus': fields.Boolean,
      'choices': fields.String,
      'default': fields.String,
      'description': fields.String,
      'email_filter': fields.Boolean,
      'field_property': fields.String,
      'forms_property': fields.String,
      'kind': fields.String,
      'name': fields.String,
      'ndb_property': fields.String,
      'placeholder': fields.String,
      'rank': fields.Integer,
      'readonly': fields.Boolean,
      'repeated': fields.Boolean,
      'required': fields.Boolean,
      'sort_filter': fields.Boolean,
      'strip_filter': fields.Boolean,
      'verbose_name': fields.String,
      'wtf_property': fields.String,
    }

  FIELDS.update(model.Base.FIELDS)
