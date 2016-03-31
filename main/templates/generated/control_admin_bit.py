{% raw -%}
###############################################################################
# Admin List
###############################################################################
{%- endraw %}
@app.route('/admin/{{model_db.variable_name}}/')
@auth.admin_required
def admin_{{model_db.variable_name}}_list():
  {{model_db.variable_name}}_dbs, {{model_db.variable_name}}_cursor = model.{{model_db.name}}.get_dbs(
    order=util.param('order') or '-modified',
  )
  return flask.render_template(
    '{{model_db.variable_name}}/admin_{{model_db.variable_name}}_list.html',
    html_class='admin-{{model_db.css_name}}-list',
    title='{{model_db.verbose_name_}} List',
    {{model_db.variable_name}}_dbs={{model_db.variable_name}}_dbs,
    next_url=util.generate_next_url({{model_db.variable_name}}_cursor),
    api_url=flask.url_for('api.admin.{{model_db.variable_name}}.list'),
  )

{% raw %}
###############################################################################
# Admin Update
###############################################################################
{%- endraw %}

# if model_db.admin_only
class {{model_db.name}}UpdateAdminForm(wtf.Form):
# for property_db in property_dbs if property_db.wtf_property and (property_db.show_on_update or property_db.show_on_admin_update)
  {{property_db.wtf_field}}
# else
  pass
# endfor
# else
class {{model_db.name}}UpdateAdminForm({{model_db.name}}UpdateForm):
# for property_db in property_dbs if property_db.wtf_property and property_db.show_on_admin_update and not property_db.show_on_update
  {{property_db.wtf_field}}
# else
  pass
# endfor
# endif


{% raw %}{% endraw %}
{% raw %}{% endraw %}
@app.route('/admin/{{model_db.variable_name}}/create/', methods=['GET', 'POST'])
@app.route('/admin/{{model_db.variable_name}}/&lt;int:{{model_db.variable_name}}_id&gt;/update/', methods=['GET', 'POST'])
@auth.admin_required
def admin_{{model_db.variable_name}}_update({{model_db.variable_name}}_id=0):
  if {{model_db.variable_name}}_id:
    {{model_db.variable_name}}_db = model.{{model_db.name}}.get_by_id({{model_db.variable_name}}_id)
  else:
    {{model_db.variable_name}}_db = model.{{model_db.name}}({{'%s=auth.current_user_key()' % model_db.auth_user_key_property if model_db.auth_user_key else ''}})

  if not {{model_db.variable_name}}_db:
    flask.abort(404)

  form = {{model_db.name}}UpdateAdminForm(obj={{model_db.variable_name}}_db)

{{model_db.get_property_key_choices(True)}}

#- for property_db in property_dbs if (property_db.show_on_update or property_db.show_on_admin_update) and ((property_db.wtf_property and property_db.kind) or property_db.tags)
  # if loop.first
  if flask.request.method == 'GET' and not form.errors:
  # endif
    # if property_db.tags
    form.{{property_db.name}}.data = config.TAG_SEPARATOR.join(form.{{property_db.name}}.data)
    # else
    form.{{property_db.name}}.data = {{model_db.variable_name}}_db.{{property_db.name}}.urlsafe() if {{model_db.variable_name}}_db.{{property_db.name}} else None
    # endif
  # if loop.last
{% raw %}{% endraw %}
  # endif
# endfor
  if form.validate_on_submit():
  # for property_db in property_dbs if property_db.wtf_property and (property_db.show_on_update or property_db.show_on_admin_update) and property_db.kind
    form.{{property_db.name}}.data = ndb.Key(urlsafe=form.{{property_db.name}}.data) if form.{{property_db.name}}.data else None
  # endfor
    # for property_db in property_dbs if property_db.tags and (property_db.show_on_update or property_db.show_on_admin_update)
    form.{{property_db.name}}.data = util.parse_tags(form.{{property_db.name}}.data)
    # endfor
    form.populate_obj({{model_db.variable_name}}_db)
    {{model_db.variable_name}}_db.put()
    return flask.redirect(flask.url_for('admin_{{model_db.variable_name}}_list', order='-modified'))

  return flask.render_template(
    '{{model_db.variable_name}}/admin_{{model_db.variable_name}}_update.html',
  # if model_db.auth_user_key and model_db.title_property_key
    title={{model_db.variable_name}}_db.{{model_db.title_property_key.get().name}},
  # elif model_db.auth_user_key and not model_db.title_property_key
    title='%s' % '{{model_db.verbose_name_}}',
  # elif not model_db.auth_user_key and model_db.title_property_key
    title='%s' % {{model_db.variable_name}}_db.{{model_db.title_property_key.get().name}} if {{model_db.variable_name}}_id else 'New {{model_db.verbose_name_}}',
  # else
    title='%s' % '%s{{model_db.verbose_name_}}' % ('' if {{model_db.variable_name}}_id else 'New '),
  # endif
    html_class='admin-{{model_db.css_name}}-update',
    form=form,
    {{model_db.variable_name}}_db={{model_db.variable_name}}_db,
    back_url_for='admin_{{model_db.variable_name}}_list',
    api_url=flask.url_for('api.admin.{{model_db.variable_name}}', {{model_db.variable_name}}_key={{model_db.variable_name}}_db.key.urlsafe() if {{model_db.variable_name}}_db.key else ''),
  )
