window.init_property_update = ->
  $('select').change on_change

  $('#ndb_property').change on_ndb_change
  $('#kind').change on_kind_change
  $('#wtf_property').change on_wtf_change
  $('#forms_property').change on_forms_change
  $('#generic_property').change on_generic_change

  $('#tags').change ->
    if $('#tags').prop 'checked'
      $('#repeated').prop 'checked', true
      $('#strip_filter').prop 'checked', false

  $('#repeated').change ->
    if not $('#repeated').prop 'checked'
      $('#tags').prop 'checked', false

  $('#use_as_title').change ->
    if $('#generic_property') and $('#use_as_title').prop 'checked'
      $('#generic_property').val('string').change()
      $('#required').prop 'checked', true
      $('#autofocus').prop 'checked', true

  $('select').each (i, val) ->
    $($('select')[i]).change()

  $('#btn-delete').click (event) ->
    event.preventDefault()
    if confirm 'Are you sure you want to delete this property?'
      $('#btn-delete').parent().submit()


on_change = (event) ->
  $this = $(event.currentTarget)
  id = $this.attr 'id'
  val = $this.val()
  $("fieldset[data-for='##{id}']").toggle Boolean val


on_ndb_change = ->
  value = $('#ndb_property').val()
  show_kind = Boolean value.indexOf('ndb.Key') == 0
  $('#kind').parent().toggle show_kind

  show_compressed = Boolean value.indexOf('ndb.Json') == 0
  $('#compressed').parent().toggle show_compressed

  show_tags = Boolean value.indexOf('ndb.String') == 0
  $('#tags').parent().toggle show_tags

  show_choices = Boolean value.indexOf('ndb.String') == 0
  $('#ndb_choices').parent().toggle show_choices

  show_computed = Boolean value.indexOf('ndb.Computed') == 0
  $('#default').parent().toggle not show_computed
  $('#ndb-checkboxes').toggle not show_computed

  if $('#ndb_property').is(':focus')
    if not show_kind
      $('#kind').val ''
    if not show_tags
      $('#tags').prop 'checked', false
    if not show_choices
      $('#ndb_choices').val ''


on_kind_change = ->
  if not $('#kind').is(':focus')
    return
  value = $('#kind').val()
  if value and value isnt 'model.User'
    $('#wtf_property').val('wtforms.SelectField').change()
    $('#forms_property').val('forms.select_field').change()
  else
    $('#wtf_property').val('').change()
    $('#forms_property').val('').change()


on_wtf_change = ->
  value = $('#wtf_property').val()
  show_choices = Boolean value.indexOf('wtforms.Select') == 0 or value.indexOf('wtforms.Radio') == 0
  $('#choices').parent().toggle show_choices
  show_strip_filters = value in [
      'wtforms.StringField'
      'wtforms.TextAreaField'
    ]
  $('#strip_filter, #email_filter').parent().toggle show_strip_filters
  if show_strip_filters
    $('#strip_filter').prop 'checked', true
    $('#email_filter').prop 'checked', false
  else
    $('#strip_filter, #email_filter').prop 'checked', false


on_forms_change = ->
  value = $('#forms_property').val()
  show_placeholder = value in [
      'forms.date_field'
      'forms.email_field'
      'forms.input_field'
      'forms.number_field'
      'forms.password_field'
      'forms.password_visible_field'
      'forms.text_field'
      'forms.textarea_field'
    ]
  $('#placeholder').parent().toggle show_placeholder

  if not show_placeholder
    $('#placeholder').val ''


on_generic_change = ->
  value = $('#generic_property').val()

  $('#strip_filter').prop 'checked', false
  $('#repeated').prop 'checked', false
  $('#tags').prop 'checked', false

  if value == 'boolean'
    $('#ndb_property').val('ndb.BooleanProperty').change()
    $('#wtf_property').val('wtforms.BooleanField').change()
    $('#forms_property').val('forms.checkbox_field').change()
    $('#field_property').val('fields.Boolean').change()

  else if value == 'computed'
    $('#ndb_property').val('ndb.ComputedProperty').change()
    $('#wtf_property').val('').change()
    $('#forms_property').val('').change()
    $('#field_property').val('').change()

  else if value == 'string'
    $('#ndb_property').val('ndb.StringProperty').change()
    $('#wtf_property').val('wtforms.StringField').change()
    $('#forms_property').val('forms.text_field').change()
    $('#field_property').val('fields.String').change()
    $('#strip_filter').prop 'checked', true

  else if value == 'string_text'
    $('#ndb_property').val('ndb.StringProperty').change()
    $('#wtf_property').val('wtforms.TextAreaField').change()
    $('#forms_property').val('forms.textarea_field').change()
    $('#field_property').val('fields.String').change()
    $('#strip_filter').prop 'checked', true

  else if value == 'string_tags'
    $('#ndb_property').val('ndb.StringProperty').change()
    $('#wtf_property').val('wtforms.StringField').change()
    $('#forms_property').val('forms.text_field').change()
    $('#field_property').val('fields.String').change()
    $('#strip_filter').prop 'checked', false
    $('#repeated').prop 'checked', true
    $('#tags').prop 'checked', true

  else if value == 'text'
    $('#ndb_property').val('ndb.TextProperty').change()
    $('#wtf_property').val('wtforms.TextAreaField').change()
    $('#forms_property').val('forms.textarea_field').change()
    $('#field_property').val('fields.String').change()
    $('#strip_filter').prop 'checked', true

  else if value == 'integer'
    $('#ndb_property').val('ndb.IntegerProperty').change()
    $('#wtf_property').val('wtforms.IntegerField').change()
    $('#forms_property').val('forms.number_field').change()
    $('#field_property').val('fields.Integer').change()

  else if value == 'float'
    $('#ndb_property').val('ndb.FloatProperty').change()
    $('#wtf_property').val('wtforms.FloatField').change()
    $('#forms_property').val('forms.number_field').change()
    $('#field_property').val('fields.Float').change()

  else if value == 'date'
    $('#ndb_property').val('ndb.DateProperty').change()
    $('#wtf_property').val('wtforms.DateField').change()
    $('#forms_property').val('forms.date_field').change()
    $('#field_property').val('fields.DateTime').change()

  else if value == 'datetime'
    $('#ndb_property').val('ndb.DateTimeProperty').change()
    $('#wtf_property').val('wtforms.DateTimeField').change()
    $('#forms_property').val('forms.datetime_field').change()
    $('#field_property').val('fields.DateTime').change()

  else if value == 'key'
    $('#ndb_property').val('ndb.KeyProperty').change()
    $('#wtf_property').val('').change()
    $('#forms_property').val('').change()
    $('#field_property').val('fields.Key').change()

  else if value == 'json'
    $('#ndb_property').val('ndb.JsonProperty').change()
    $('#wtf_property').val('').change()
    $('#forms_property').val('').change()
    $('#field_property').val('fields.Raw').change()

  else
    $('#ndb_property').val('').change()
    $('#wtf_property').val('').change()
    $('#forms_property').val('').change()
    $('#field_property').val('').change()
