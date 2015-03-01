window.init_model_view = ->
  hljs.initHighlightingOnLoad()
  $('code').click (event) ->
    id = $(event.currentTarget).attr 'id'
    if $(".auto-select[data-for='#{id}']").is ':checked'
      select_text id

  $('.expand').click (event) ->
    $current = $(event.currentTarget)
    $target = $("##{$current.data 'for'}")
    $target.toggleClass 'expand'


window.init_model_update = ->
  $('#auth_user_key').prop 'disabled', $('#admin_only').is ':checked'
  $('#admin_only').on 'change', ->
    admin_only = $('#admin_only').is ':checked'
    $('#auth_user_key').prop 'disabled', admin_only
    $('#auth_user').prop 'disabled', admin_only
    $('#auth_user').parent().parent().toggleClass 'disabled', admin_only
    $('#auth_user_key').val ''
    $('#auth_user').prop 'checked', false


window.select_text = (containerid) ->
  if document.selection
    range = document.body.createTextRange()
    range.moveToElementText document.getElementById containerid
    range.select()
  else if window.getSelection
    range = document.createRange()
    range.selectNode document.getElementById containerid
    window.getSelection().addRange range
