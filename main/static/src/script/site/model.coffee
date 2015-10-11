window.init_model_view = ->
  hljs.initHighlightingOnLoad()

  $('.expand').click (event) ->
    $current = $(event.currentTarget)
    $target = $("##{$current.data 'for'}")
    $target.toggleClass 'expand'
