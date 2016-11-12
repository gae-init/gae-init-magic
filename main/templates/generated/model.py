&#35; coding: utf-8

from __future__ import absolute_import
{% raw %}{% endraw %}
# if project_db.include_babel
from flask_babel import lazy_gettext as _
# endif
from google.appengine.ext import ndb

from api import fields
import model
import util


class {{model_db.name}}(model.Base):
# for property_db in property_dbs if property_db.ndb_property
  {{property_db.ndb_field(project_db.include_babel)}}
# endfor

# if model_db.default_order
{% raw %}{% endraw %}
  @classmethod
  def get_dbs(cls, order=None, **kwargs):
    return super({{model_db.name}}, cls).get_dbs(
      order=order or util.param('order') or '{{model_db.default_order}}',
      **kwargs
    )
# endif
# set get_child_model_stuff = model_db.get_child_model_stuff
# set model_names = get_child_model_stuff.split('\n')[0].split(',')
# set get_model_dbs = '\n'.join(get_child_model_stuff.split('\n')[1:])

# if get_model_dbs
{{get_model_dbs}}
  @classmethod
  def _pre_delete_hook(cls, key):
    {{model_db.variable_name}}_db = key.get()
  # for child_db_name in model_names
    {{child_db_name}}_keys = {{model_db.variable_name}}_db.get_{{child_db_name}}_dbs(keys_only=True, limit=-1)[0]
  # endfor
    ndb.delete_multi({{'_keys + '.join(model_names)}}_keys)
{% raw %}{% endraw %}
# else
{% raw %}{% endraw %}
# endif
  FIELDS = {
  # for property_db in property_dbs if property_db.field_property
    {{property_db.api_field}}
  # endfor
  }

  FIELDS.update(model.Base.FIELDS)
