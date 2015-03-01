# import 'macro/utils.html' as utils

&#35; coding: utf-8

from flask.ext import wtf
import flask
import wtforms

import auth
import model
import util

from main import app
{{utils.empty_line()}}
# if not model_db.admin_only
# include 'generated/control_user_bit.py'
{% raw %}{% endraw %}
{% raw %}{% endraw %}
{% raw %}{% endraw %}
# endif

# include 'generated/control_admin_bit.py'
