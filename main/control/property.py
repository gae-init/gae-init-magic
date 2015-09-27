# coding: utf-8

from google.appengine.ext import ndb
from flask.ext import wtf
import flask
import wtforms

import auth
import config
import model
import task
import util

from main import app


###############################################################################
# Property Update
###############################################################################
class PropertyUpdateForm(wtf.Form):
  name = wtforms.StringField(
      model.Property.name._verbose_name,
      [wtforms.validators.required()],
      description=u'Use snake_case.',
      filters=[util.strip_filter],
    )
  use_as_title = wtforms.BooleanField(
      u'Serves as title property',
      [wtforms.validators.optional()],
    )
  verbose_name = wtforms.StringField(
      model.Property.verbose_name._verbose_name,
      [wtforms.validators.optional()],
    )
  generic_property = wtforms.SelectField(
      'Generic Property Type',
      [wtforms.validators.optional()],
      choices=config.GENERIC_PROPERIES,
      description='Actual properties will be updated automatically below.',
    )
  rank = wtforms.IntegerField(
      model.Property.rank._verbose_name,
      [wtforms.validators.optional()],
    )
  show_on_view = wtforms.BooleanField(
      model.Property.show_on_view._verbose_name,
      [wtforms.validators.optional()],
    )
  show_on_update = wtforms.BooleanField(
      model.Property.show_on_update._verbose_name,
      [wtforms.validators.optional()],
    )
  show_on_list = wtforms.BooleanField(
      model.Property.show_on_list._verbose_name,
      [wtforms.validators.optional()],
    )
  show_on_admin_update = wtforms.BooleanField(
      model.Property.show_on_admin_update._verbose_name,
      [wtforms.validators.optional()],
    )
  show_on_admin_list = wtforms.BooleanField(
      model.Property.show_on_admin_list._verbose_name,
      [wtforms.validators.optional()],
    )
  ndb_property = wtforms.SelectField(
      model.Property.ndb_property._verbose_name,
      [wtforms.validators.optional()],
      choices=config.NDB_PROPERIES,
    )
  required = wtforms.BooleanField(
      model.Property.required._verbose_name,
      [wtforms.validators.optional()],
    )
  default = wtforms.StringField(
      model.Property.default._verbose_name,
      [wtforms.validators.optional()],
      filters=[util.strip_filter],
    )
  repeated = wtforms.BooleanField(
      model.Property.repeated._verbose_name,
      [wtforms.validators.optional()],
    )
  tags = wtforms.BooleanField(
      model.Property.tags._verbose_name,
      [wtforms.validators.optional()],
    )
  indexed = wtforms.BooleanField(
      model.Property.indexed._verbose_name,
      [wtforms.validators.optional()],
    )
  kind = wtforms.SelectField(
      model.Property.kind._verbose_name,
      [wtforms.validators.optional()],
      choices=[],
    )
  auto_now = wtforms.BooleanField(
      model.Property.auto_now._verbose_name,
      [wtforms.validators.optional()],
    )
  auto_now_add = wtforms.BooleanField(
      model.Property.auto_now_add._verbose_name,
      [wtforms.validators.optional()],
    )
  ndb_choices = wtforms.StringField(
      model.Property.ndb_choices._verbose_name,
      [wtforms.validators.optional()],
    )
  wtf_property = wtforms.SelectField(
      model.Property.wtf_property._verbose_name,
      [wtforms.validators.optional()],
      choices=config.WTF_PROPERIES,
    )
  description = wtforms.StringField(
      model.Property.description._verbose_name,
      [wtforms.validators.optional()],
    )
  email_filter = wtforms.BooleanField(
      model.Property.email_filter._verbose_name,
      [wtforms.validators.optional()],
    )
  strip_filter = wtforms.BooleanField(
      model.Property.strip_filter._verbose_name,
      [wtforms.validators.optional()],
    )
  sort_filter = wtforms.BooleanField(
      model.Property.sort_filter._verbose_name,
      [wtforms.validators.optional()],
    )
  choices = wtforms.StringField(
      model.Property.choices._verbose_name,
      [wtforms.validators.optional()],
    )
  forms_property = wtforms.SelectField(
      model.Property.forms_property._verbose_name,
      [wtforms.validators.optional()],
      choices=config.FORMS_PROPERIES,
    )
  autofocus = wtforms.BooleanField(
      model.Property.autofocus._verbose_name,
      [wtforms.validators.optional()],
    )
  readonly = wtforms.BooleanField(
      model.Property.readonly._verbose_name,
      [wtforms.validators.optional()],
    )
  placeholder = wtforms.StringField(
      model.Property.placeholder._verbose_name,
      [wtforms.validators.optional()],
    )
  field_property = wtforms.SelectField(
      model.Property.field_property._verbose_name,
      [wtforms.validators.optional()],
      choices=config.FIELD_PROPERIES,
    )


@app.route('/project/<int:project_id>/model/<int:model_id>/property/create/', methods=['GET', 'POST'])
@app.route('/project/<int:project_id>/model/<int:model_id>/property/<int:property_id>/update/', methods=['GET', 'POST'])
@auth.login_required
def property_update(project_id, model_id, property_id=0):
  user_key = auth.current_user_key()
  project_db = model.Project.get_by_id(project_id)
  if not project_db or project_db.user_key != user_key:
    flask.abort(404)

  model_db = model.Model.get_by_id(model_id, parent=project_db.key)
  if not model_db:
    flask.abort(404)

  if property_id:
    property_db = model.Property.get_by_id(property_id, parent=model_db.key)
  else:
    property_db = model.Property(
        parent=model_db.key,
        name='',
        rank=model_db.property_count + 1,
      )
  if not property_db:
    flask.abort(404)

  form = PropertyUpdateForm(obj=property_db)

  model_dbs, model_cursor = project_db.get_model_dbs()
  form.kind.choices = [('', '-'), ('model.User', 'model.User')]
  form.kind.choices += [('model.%s' % m.name, 'model.%s' % m.name) for m in model_dbs if m.key != model_db.key]

  if form.validate_on_submit():
    form.populate_obj(property_db)
    property_db.put()
    if form.use_as_title.data and model_db.title_property_key != property_db.key:
      model_db.title_property_key = property_db.key
      model_db.put()
    elif not form.use_as_title.data and model_db.title_property_key == property_db.key:
      model_db.title_property_key = None
      model_db.put()

    task.property_count(model_db)
    return flask.redirect(flask.url_for('model_view', project_id=project_db.key.id(), model_id=model_db.key.id()))

  if not form.errors and model_db.title_property_key == property_db.key:
    form.use_as_title.data = True

  return flask.render_template(
      'property/property_update.html',
      title=property_db.name or 'new_property',
      html_class='property-update',
      form=form,
      project_db=project_db,
      model_db=model_db,
      property_db=property_db,
    )


# TODO: eventually do it via API and do not allow GET
@app.route('/project/<int:project_id>/model/<int:model_id>/property/<int:property_id>/<direction>/', methods=['GET', 'POST'])
@auth.login_required
def property_rank(project_id, model_id, property_id, direction='up'):
  if direction not in ['up', 'down']:
    flask.abort(404)
  user_key = auth.current_user_key()
  project_db = model.Project.get_by_id(project_id)
  if not project_db or project_db.user_key != user_key:
    flask.abort(404)

  model_db = model.Model.get_by_id(model_id, parent=project_db.key)
  if not model_db:
    flask.abort(418)

  property_db = model.Property.get_by_id(property_id, parent=model_db.key)
  if not property_db:
    flask.abort(404)

  property_dbs, property_cursor = model_db.get_property_dbs(limit=config.MAX_DB_LIMIT)

  found_rank = 1
  for i, p_db in enumerate(property_dbs):
    rank = i + 1
    p_db.rank = rank
    if p_db.key == property_db.key:
      found_rank = rank

  if direction == 'up' and found_rank > 1:
    property_dbs[found_rank - 1].rank = found_rank - 1
    property_dbs[found_rank - 2].rank = found_rank

  if direction == 'down' and found_rank < len(property_dbs):
    property_dbs[found_rank - 1].rank = found_rank + 1
    property_dbs[found_rank].rank = found_rank

  ndb.put_multi(property_dbs)
  return flask.redirect(flask.url_for('model_view', project_id=project_db.key.id(), model_id=model_db.key.id()))


@app.route('/project/<int:project_id>/model/<int:model_id>/property/<int:property_id>/delete/', methods=['GET', 'POST'])
@auth.login_required
def property_delete(project_id, model_id, property_id):
  user_key = auth.current_user_key()
  project_db = model.Project.get_by_id(project_id)
  if not project_db or project_db.user_key != user_key:
    flask.abort(404)

  model_db = model.Model.get_by_id(model_id, parent=project_db.key)
  if not model_db:
    flask.abort(404)

  property_db = model.Property.get_by_id(property_id, parent=model_db.key)
  if not property_db:
    flask.abort(404)

  property_db.key.delete()
  flask.flash('Property "%s" deleted.' % property_db.name, category='success')
  return flask.redirect(flask.url_for('model_view', project_id=project_db.key.id(), model_id=model_db.key.id()))
