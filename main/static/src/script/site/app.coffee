$ ->
  init_common()

$ -> $('html.welcome').each ->
  LOG('init welcome')

$ -> $('html.profile').each ->
  init_profile()

$ -> $('html.auth').each ->
  init_auth()

$ -> $('html.feedback').each ->

$ -> $('html.user-list').each ->
  init_user_list()

$ -> $('html.user-merge').each ->
  init_user_merge()

$ -> $('html.admin-config').each ->
  init_admin_config()

$ -> $('html.model-view').each ->
  init_model_view()

$ -> $('html.model-update').each ->
  init_model_update()

$ -> $('html.model-list').each ->
  hljs.initHighlightingOnLoad()

$ -> $('html.property-update').each ->
  init_property_update()
