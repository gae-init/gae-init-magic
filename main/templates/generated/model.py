&#35; coding: utf-8

from __future__ import absolute_import

from google.appengine.ext import ndb

from api import fields
import model
import util


class {{model_db.name}}(model.Base):
# for property_db in property_dbs if property_db.ndb_property
  {{property_db.ndb_field}}
# endfor

# if model_db.default_order
{% raw %}{% endraw %}
  @classmethod
  def get_dbs(cls, order=None, **kwargs):
    return super({{model_db.name}}, cls).get_dbs(
      order=util.param('order') or '{{model_db.default_order}}',
      **kwargs
    )
# endif
# set foreign_dbs = model_db.get_foreign_dbs()
# if foreign_dbs
{% raw %}{% endraw %}
{{foreign_dbs}}
#- else
{% raw %}{% endraw %}
# endif
  FIELDS = {
  # for property_db in property_dbs if property_db.field_property
    {{property_db.api_field}}
  # endfor
  }

  FIELDS.update(model.Base.FIELDS)
