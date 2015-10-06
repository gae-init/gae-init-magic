{% raw -%}
###############################################################################
# List
###############################################################################
{%- endraw %}
@app.route('/{{model_db.variable_name}}/')
# if model_db.auth_user_key
@auth.login_required
# endif
def {{model_db.variable_name}}_list():
  {{model_db.variable_name}}_dbs, {{model_db.variable_name}}_cursor = model.{{model_db.name}}.get_dbs({{'%s=auth.current_user_key()' % model_db.auth_user_key_property if model_db.auth_user_key else ''}})
  return flask.render_template(
      '{{model_db.variable_name}}/{{model_db.variable_name}}_list.html',
      html_class='{{model_db.css_name}}-list',
      title='{{model_db.verbose_name_}} List',
      {{model_db.variable_name}}_dbs={{model_db.variable_name}}_dbs,
      next_url=util.generate_next_url({{model_db.variable_name}}_cursor),
      api_url=flask.url_for('api.{{model_db.variable_name}}.list'),
    )


{% raw -%}
###############################################################################
# View
###############################################################################
{%- endraw %}
@app.route('/{{model_db.variable_name}}/&lt;int:{{model_db.variable_name}}_id&gt;/')
# if model_db.auth_user_key
@auth.login_required
# endif
def {{model_db.variable_name}}_view({{model_db.variable_name}}_id):
  {{model_db.variable_name}}_db = model.{{model_db.name}}.get_by_id({{model_db.variable_name}}_id)
  if not {{model_db.variable_name}}_db{{' or %s_db.%s != auth.current_user_key()' % (model_db.variable_name, model_db.auth_user_key_property) if model_db.auth_user_key else ''}}:
    flask.abort(404)

  return flask.render_template(
      '{{model_db.variable_name}}/{{model_db.variable_name}}_view.html',
      html_class='{{model_db.variable_name}}-view',
      # if model_db.title_property_key
      title={{model_db.variable_name}}_db.{{model_db.title_property_key.get().name}},
      # else
      title='{{model_db.verbose_name_}}',
      # endif
      {{model_db.variable_name}}_db={{model_db.variable_name}}_db,
      api_url=flask.url_for('api.{{model_db.variable_name}}', {{model_db.variable_name}}_key={{model_db.variable_name}}_db.key.urlsafe() if {{model_db.variable_name}}_db.key else ''),
    )
