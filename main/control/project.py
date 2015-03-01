# coding: utf-8

from flask.ext import wtf
import flask
import wtforms

import auth
import model
import util

from main import app


###############################################################################
# Update
###############################################################################
class ProjectUpdateForm(wtf.Form):
  description = wtforms.TextAreaField(
      model.Project.description._verbose_name,
      [wtforms.validators.optional()],
      filters=[util.strip_filter],
    )
  name = wtforms.StringField(
      model.Project.name._verbose_name,
      [wtforms.validators.required()],
      filters=[util.strip_filter],
    )
  public = wtforms.BooleanField(
      model.Project.public._verbose_name,
      [wtforms.validators.optional()],
    )
  url = wtforms.StringField(
      model.Project.url._verbose_name,
      [wtforms.validators.optional()],
      filters=[util.strip_filter],
    )


@app.route('/project/create/', methods=['GET', 'POST'])
@app.route('/project/<int:project_id>/update/', methods=['GET', 'POST'])
@auth.login_required
def project_update(project_id=0):
  user_key = auth.current_user_key()
  if project_id:
    project_db = model.Project.get_by_id(project_id)
  else:
    project_db = model.Project(user_key=user_key)

  if not project_db or project_db.user_key != user_key:
    flask.abort(404)

  form = ProjectUpdateForm(obj=project_db)
  if form.validate_on_submit():
    form.populate_obj(project_db)
    project_db.put()
    return flask.redirect(flask.url_for('model_list', project_id=project_db.key.id()))

  return flask.render_template(
      'project/project_update.html',
      title=project_db.name or 'New Project',
      html_class='project-update',
      form=form,
      project_db=project_db,
    )


###############################################################################
# List
###############################################################################
@app.route('/projects/')
@auth.login_required
def project_list():
  project_dbs, project_cursor = auth.current_user_db().get_project_dbs()
  return flask.render_template(
      'project/project_list.html',
      html_class='project-list',
      title='Projects',
      project_dbs=project_dbs,
      next_url=util.generate_next_url(project_cursor),
      api_url=flask.url_for('api.projects'),
    )


###############################################################################
# Admin List
###############################################################################
@app.route('/admin/project/')
@auth.admin_required
def admin_project_list():
  project_dbs, project_cursor = model.Project.get_dbs()
  return flask.render_template(
      'project/admin_project_list.html',
      html_class='admin-project-list',
      title='Projects',
      project_dbs=project_dbs,
      next_url=util.generate_next_url(project_cursor),
      api_url=flask.url_for('api.projects'),
    )
