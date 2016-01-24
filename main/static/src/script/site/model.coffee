window.init_model_view = ->
  hljs.initHighlightingOnLoad()

  $('.expand').click (event) ->
    $current = $(event.currentTarget)
    $target = $("##{$current.data 'for'}")
    $target.toggleClass 'expand'


window.init_model_update = ->
  $('#btn-delete').click (event) ->
    event.preventDefault()
    if confirm 'Are you sure you want to delete this model?'
      $('#btn-delete').parent().submit()
