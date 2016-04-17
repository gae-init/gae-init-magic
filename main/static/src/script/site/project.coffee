window.init_project_update = ->
  $('#btn-delete').click (event) ->
    event.preventDefault()
    if confirm 'Are you sure you want to delete this project?'
      $('#btn-delete').parent().submit()
