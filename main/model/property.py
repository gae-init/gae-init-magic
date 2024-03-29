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
  tags = ndb.BooleanProperty(default=False)
  indexed = ndb.BooleanProperty(default=True)
  auto_now = ndb.BooleanProperty(default=False)
  auto_now_add = ndb.BooleanProperty(default=False)
  compressed = ndb.BooleanProperty(default=False)
  ndb_choices = ndb.StringProperty(verbose_name='Choices')

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

  def ndb_field(self, include_babel=False):
    args = [
      'kind=%s' % self.kind if self.kind else '',
      'default=%s' % self.default if self.default else '',
      'required=True' if self.required else '',
      'repeated=%s' % self.repeated if self.repeated else '',
      'indexed=False' if not self.indexed else '',
      'compressed=True' if self.compressed else '',
      'choices=[%s]' % self.ndb_choices if self.ndb_choices else '',
    ]
    if include_babel:
      args.append("verbose_name=_(u'%s')" % self.verbose_name_)
    else:
      args.append("verbose_name=u'%s'" % self.verbose_name if self.verbose_name else '')

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
    validators = ['wtforms.validators.%s()' % ('required' if self.required else 'optional')]
    if self.ndb_property == 'ndb.StringProperty' and self.wtf_property in ['wtforms.TextAreaField', 'wtforms.StringField']:
      validators.append('wtforms.validators.length(max=500)')
    filters = [
        'util.strip_filter' if self.strip_filter else '',
        'util.email_filter' if self.email_filter else '',
        'util.sort_filter' if self.sort_filter else '',
      ]

    filters = [f for f in filters if f]
    filters = '    filters=[%s],\n' % ', '.join(filters) if filters else ''
    description = "    description='%s',\n" % self.description if self.description else ''

    choices = ''
    if self.wtf_property in ['wtforms.RadioField', 'wtforms.SelectField', 'wtforms.SelectMultipleField']:
      choices = '    choices=%s,\n' % (self.choices if self.choices else '[]')

    date_format = ''
    if self.wtf_property == 'wtforms.DateTimeField':
      date_format = "    format='%Y-%m-%dT%H:%M',\n"

    title = '%r' % self.verbose_name_
    if self.ndb_property:
      title = 'model.%s.%s._verbose_name' % (self.key.parent().get().name, self.name)

    if self.wtf_property == 'wtforms.GeoPtField':
      validators += ['wtforms.validators.NumberRange(min=-90, max=90)']
      validatorss = '[%s]' % ', '.join(validators)
      lat = (
            '%s_lat = wtforms.FloatField(\n'
            '    %s,\n'
            '    %s,\n%s%s%s%s'
            '  )'
        % (self.name, title + " + ' Latitude'", validatorss, filters, choices, description, date_format))
      validators.pop()
      validators += ['wtforms.validators.NumberRange(min=-180, max=180)']
      validatorss = '[%s]' % ', '.join(validators)
      lon = (
            '\n  %s_lon = wtforms.FloatField(\n'
            '    %s,\n'
            '    %s,\n%s%s%s%s'
            '  )'
        % (self.name, title + " + ' Longtitute'", validatorss, filters, choices, description, date_format))
      return '%s %s' % (lat, lon)

    validators = '[%s]' % ', '.join(validators)
    return (
      '%s = %s(\n'
      '    %s,\n'
      '    %s,\n%s%s%s%s'
      '  )'
      % (self.name, self.wtf_property, title, validators, filters, choices, description, date_format))

  @ndb.ComputedProperty
  def forms_field(self):
    autofocus = ', autofocus=True' if self.autofocus else ''
    readonly = ', readonly=True' if self.readonly else ''
    placeholder = ", placeholder='%s'" % self.placeholder if self.placeholder else ''
    if self.forms_property == 'forms.geo_pt_field':
      lat = "{{forms.number_field(form.%s_lat%s%s%s)}}" % (self.name, autofocus, readonly, placeholder)
      lon = "{{forms.number_field(form.%s_lon%s%s%s)}}" % (self.name, autofocus, readonly, placeholder)
      return ('<div class="row">\n'
        '          <div class="col-sm-6">%s</div>\n          <div class="col-sm-6">%s</div>\n         </div>' %(lat, lon))
    return "{{%s(form.%s%s%s%s)}}" % (self.forms_property, self.name, autofocus, readonly, placeholder)

  @ndb.ComputedProperty
  def default_verbose_name(self):
    return util.snake_to_verbose(self.name)

  @ndb.ComputedProperty
  def verbose_name_(self):
    return self.verbose_name or self.default_verbose_name

  def get_title_name(self):
    if self.ndb_property != 'ndb.KeyProperty' or not self.kind:
      return None
    if self.kind == 'model.User':
      return 'name'
    model_qry = model.Model.query(ancestor=self.key.parent().parent())
    model_qry = model_qry.filter(model.Model.name == self.kind.split('.')[1])
    model_db = model_qry.get()
    if model_db and model_db.title_property_key:
      return model_db.title_property_key.get().name
    return None

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
