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
# set foreign_get_dbs = model_db.get_foreign_get_dbs()
# if foreign_get_dbs
{{foreign_get_dbs}}
  @classmethod
  def _pre_delete_hook(cls, key):
    {{model_db.variable_name}}_db = key.get()
    # set foreign_dbs_names = model_db.get_foreign_dbs_names()
    # for foreign_db_name in foreign_dbs_names
    {{foreign_db_name}}_keys, _null = {{model_db.variable_name}}_db.get_{{foreign_db_name}}_dbs(keys_only=True, limit=-1)
    # endfor
    ndb.delete_multi({{'_keys + '.join(foreign_dbs_names)}}_keys)
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
