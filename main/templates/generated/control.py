&#35; coding: utf-8

from google.appengine.ext import ndb
import flask
import flask_wtf
import wtforms

import auth
import config
import model
import util

from main import app

{% raw %}{% endraw %}
# if not model_db.admin_only
# include 'generated/control_update_bit.py'
{% raw %}{% endraw %}
{% raw %}{% endraw %}
{% raw %}{% endraw %}
# endif

# if not model_db.admin_only or model_db.public_view
# include 'generated/control_view_bit.py'
{% raw %}{% endraw %}
{% raw %}{% endraw %}
{% raw %}{% endraw %}
# endif

# include 'generated/control_admin_bit.py'
