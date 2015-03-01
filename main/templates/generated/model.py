&#35; coding: utf-8

from __future__ import absolute_import

from google.appengine.ext import ndb

from api import fields
import model


class {{model_db.name}}(model.Base):
# for property_db in property_dbs if property_db.ndb_property
  {{property_db.ndb_field}}
# endfor
{% raw %}{% endraw %}
  FIELDS = {
    # for property_db in property_dbs if property_db.field_property
      {{property_db.api_field}}
    # endfor
    }

  FIELDS.update(model.Base.FIELDS)
