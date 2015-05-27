# coding: utf-8

from google.appengine.ext import ndb
from flask.ext import wtf
import flask
import wtforms
import random

import auth
import config
import model
import task
import util

from main import app


###############################################################################
# Model Update
###############################################################################
class ModelUpdateForm(wtf.Form):
  name = wtforms.StringField(
      model.Model.name._verbose_name,
      [wtforms.validators.required()],
      filters=[util.strip_filter],
      description='Use CamelCase.',
    )
  verbose_name = wtforms.StringField(
      model.Model.verbose_name._verbose_name,
      [wtforms.validators.optional()],
      filters=[util.strip_filter],
    )
  icon = wtforms.SelectField(
      model.Model.icon._verbose_name,
      [wtforms.validators.required()],
      filters=[util.strip_filter],
      choices=config.ICON_CHOICES,
    )
  auth_user = wtforms.BooleanField(
      'User Authentication',
      [wtforms.validators.optional()],
    )
  auth_user_key = wtforms.SelectField(
      model.Model.auth_user_key._verbose_name,
      [wtforms.validators.optional()],
      description='Choose a KeyProperty to assign it with the model.User'
    )
  admin_only = wtforms.BooleanField(
      model.Model.admin_only._verbose_name,
      [wtforms.validators.optional()],
    )
  public_view = wtforms.BooleanField(
      model.Model.public_view._verbose_name,
      [wtforms.validators.optional()],
    )


@app.route('/project/<int:project_id>/model/create/', methods=['GET', 'POST'])
@app.route('/project/<int:project_id>/model/<int:model_id>/update/', methods=['GET', 'POST'])
@auth.login_required
def model_update(project_id, model_id=0):
  user_key = auth.current_user_key()
  project_db = model.Project.get_by_id(project_id)
  if not project_db or project_db.user_key != user_key:
    flask.abort(404)

  auth_choices = [('', '-')]

  if model_id:
    model_db = model.Model.get_by_id(model_id, parent=project_db.key)
    property_dbs, property_cursor = model_db.get_property_dbs()
    for property_db in property_dbs:
      if property_db.ndb_property == 'ndb.KeyProperty':
        auth_choices.append((property_db.key.urlsafe(), property_db.name))
  else:
    model_db = model.Model(
        parent=project_db.key,
        name='',
        rank=project_db.model_count + 1,
        icon=random.choice(config.ICONS),
      )
  if not model_db:
    flask.abort(404)

  form = ModelUpdateForm(obj=model_db)
  form.auth_user_key.choices = auth_choices

  if form.validate_on_submit():
    if model_id and not form.admin_only.data and form.auth_user_key.data:
      form.auth_user_key.data = ndb.Key(urlsafe=form.auth_user_key.data)
    else:
      form.auth_user_key.data = None

    form.populate_obj(model_db)
    model_db.put()

    if not model_id and form.auth_user.data:
      property_db = model.Property(
          parent=model_db.key,
          name='user_key',
          kind='model.User',
          rank=1,
          show_on_view=False,
          show_on_update=False,
          show_on_list=False,
          show_on_admin_update=False,
          show_on_admin_list=False,
          required=True,
          ndb_property='ndb.KeyProperty',
          field_property='fields.Key',
        )
      property_db.put()
      model_db.admin_only = False
      model_db.property_count = 1
      model_db.auth_user_key = property_db.key
      model_db.put()

    task.model_count(project_db)
    return flask.redirect(flask.url_for('model_view', project_id=project_db.key.id(), model_id=model_db.key.id()))

  if model_id and not form.errors:
    if model_db.auth_user_key:
      form.auth_user_key.data = model_db.auth_user_key.urlsafe()

  return flask.render_template(
      'model/model_update.html',
      title=model_db.name or 'NewModel',
      html_class='model-update',
      form=form,
      project_db=project_db,
      model_db=model_db,
    )


###############################################################################
# Model View
###############################################################################
@app.route('/project/<int:project_id>/model/<int:model_id>/')
@auth.login_required
def model_view(project_id, model_id):
  user_key = auth.current_user_key()
  project_db = model.Project.get_by_id(project_id)
  if not project_db or project_db.user_key != user_key:
    flask.abort(404)

  model_db = model.Model.get_by_id(model_id, parent=project_db.key)
  if not model_db:
    flask.abort(404)

  property_dbs, property_cursor = model_db.get_property_dbs()

  files = [
      ('main/control/__init__.py', 'generated/control_init.py', 'python'),
      ('main/model/__init__.py', 'generated/model_init.py', 'python'),
      ('main/api/v1/__init__.py', 'generated/model_init.py', 'python'),
      ('main/templates/bit/header.html', 'generated/bit/header.html', 'html'),
      ('main/templates/admin/admin.html', 'generated/admin/admin.html', 'html'),

      ('main/model/%s.py' % model_db.variable_name, 'generated/model.py', 'python'),
      ('main/control/%s.py' % model_db.variable_name, 'generated/control.py', 'python'),

      ('main/templates/%(name)s/%(name)s_update.html' % {'name': model_db.variable_name}, 'generated/update.html', 'html'),
      ('main/templates/%(name)s/%(name)s_view.html' % {'name': model_db.variable_name}, 'generated/view.html', 'html'),
      ('main/templates/%(name)s/%(name)s_list.html' % {'name': model_db.variable_name}, 'generated/list.html', 'html'),

      ('main/templates/%(name)s/admin_%(name)s_update.html' % {'name': model_db.variable_name}, 'generated/admin_update.html', 'html'),
      ('main/templates/%(name)s/admin_%(name)s_list.html' % {'name': model_db.variable_name}, 'generated/admin_list.html', 'html'),
      ('main/api/v1/%s.py' % model_db.variable_name, 'generated/api.py', 'python'),
    ]

  return flask.render_template(
      'model/model_view.html',
      title=model_db.name,
      html_class='model-view',
      project_db=project_db,
      model_db=model_db,
      property_dbs=property_dbs,
      next_url=util.generate_next_url(property_cursor),
      files=files,
    )


###############################################################################
# Model List
###############################################################################
@app.route('/project/<int:project_id>/models/')
@auth.login_required
def model_list(project_id):
  user_key = auth.current_user_key()
  project_db = model.Project.get_by_id(project_id)
  if not project_db or project_db.user_key != user_key:
    flask.abort(404)

  model_dbs, model_cursor = project_db.get_model_dbs()
  return flask.render_template(
      'model/model_list.html',
      html_class='model-list',
      title=project_db.name,
      project_db=project_db,
      model_dbs=model_dbs,
      next_url=util.generate_next_url(model_cursor),
    )


# TODO: eventually do it via API and do not allow GET
@app.route('/project/<int:project_id>/model/<int:model_id>/<direction>/', methods=['GET', 'POST'])
@auth.login_required
def model_rank(project_id, model_id, direction='up'):
  if direction not in ['up', 'down']:
    flask.abort(404)
  user_key = auth.current_user_key()
  project_db = model.Project.get_by_id(project_id)
  if not project_db or project_db.user_key != user_key:
    flask.abort(404)

  model_db = model.Model.get_by_id(model_id, parent=project_db.key)
  if not model_db:
    flask.abort(418)

  model_dbs, model_cursor = project_db.get_model_dbs(limit=config.MAX_DB_LIMIT)

  found_rank = 1
  for i, m_db in enumerate(model_dbs):
    rank = i + 1
    m_db.rank = rank
    if m_db.key == model_db.key:
      found_rank = rank

  if direction == 'up' and found_rank > 1:
    model_dbs[found_rank - 1].rank = found_rank - 1
    model_dbs[found_rank - 2].rank = found_rank

  if direction == 'down' and found_rank < len(model_dbs):
    model_dbs[found_rank - 1].rank = found_rank + 1
    model_dbs[found_rank].rank = found_rank

  ndb.put_multi(model_dbs)
  return flask.redirect(flask.url_for('model_list', project_id=project_db.key.id()))
