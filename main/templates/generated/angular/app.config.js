# set model_dbs = model_dbs or [model_db]
# for model_db in model_dbs
  when('/admin/{{model_db.css_name}}/', {
    template: '&lt;{{model_db.css_name}}-list&gt;&lt;/{{model_db.css_name}}-list&gt;'
  }).
# endfor
