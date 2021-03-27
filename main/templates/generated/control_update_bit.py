{% raw -%}
###############################################################################
# Update
###############################################################################
{%- endraw %}
class {{model_db.name}}UpdateForm(flask_wtf.FlaskForm):

# for property_db in property_dbs if property_db.wtf_property and property_db.show_on_update
  {{property_db.wtf_field}}
# else
  pass
# endfor

{% raw %}{% endraw %}

@app.route('/{{model_db.variable_name}}/create/', methods=['GET', 'POST'])
@app.route('/{{model_db.variable_name}}/&lt;int:{{model_db.variable_name}}_id&gt;/update/', methods=['GET', 'POST'])
# if model_db.auth_user_key
@auth.login_required
# endif
def {{model_db.variable_name}}_update({{model_db.variable_name}}_id=0):
  if {{model_db.variable_name}}_id:
    {{model_db.variable_name}}_db = model.{{model_db.name}}.get_by_id({{model_db.variable_name}}_id)
  else:
    {{model_db.variable_name}}_db = model.{{model_db.name}}({{'%s=auth.current_user_key()' % model_db.auth_user_key_property if model_db.auth_user_key else ''}})

  if not {{model_db.variable_name}}_db{{' or %s_db.%s != auth.current_user_key()' % (model_db.variable_name, model_db.auth_user_key_property) if model_db.auth_user_key else ''}}:
    flask.abort(404)

  form = {{model_db.name}}UpdateForm(obj={{model_db.variable_name}}_db)

{{model_db.get_property_key_choices()}}

#- for property_db in property_dbs if property_db.show_on_update and ((property_db.wtf_property and property_db.kind and property_db.kind != 'model.User') or property_db.tags)
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
    # for property_db in property_dbs if property_db.show_on_update and property_db.kind
    form.{{property_db.name}}.data = ndb.Key(urlsafe=form.{{property_db.name}}.data) if form.{{property_db.name}}.data else None
    # endfor
    # for property_db in property_dbs if property_db.show_on_update and property_db.tags
    form.{{property_db.name}}.data = util.parse_tags(form.{{property_db.name}}.data)
    # endfor
    form.populate_obj({{model_db.variable_name}}_db)
    {{model_db.variable_name}}_db.put()
    return flask.redirect(flask.url_for('{{model_db.variable_name}}_view', {{model_db.variable_name}}_id={{model_db.variable_name}}_db.key.id()))

  return flask.render_template(
    '{{model_db.variable_name}}/{{model_db.variable_name}}_update.html',
  # if model_db.title_property_key
    title={{model_db.variable_name}}_db.{{model_db.title_property_key.get().name}} if {{model_db.variable_name}}_id else 'New {{model_db.verbose_name_}}',
  # else
    title='%s' % '{{model_db.verbose_name_}}' if {{model_db.variable_name}}_id else 'New {{model_db.verbose_name_}}',
  # endif
    html_class='{{model_db.css_name}}-update',
    form=form,
    {{model_db.variable_name}}_db={{model_db.variable_name}}_db,
  )
