angular.
  module('{{model_db.variable_name_camel}}List').
  component('{{model_db.variable_name_camel}}List', {
    templateUrl: 'app/{{model_db.variable_name}}/{{model_db.variable_name}}-list.template.html',
    controller: ['{{model_db.name}}',
      function {{model_db.name}}ListController({{model_db.name}}) {
        var self = this;
        {{model_db.name}}.query().$promise.then(function(response) {
          self.{{model_db.variable_name}}_dbs = response.result;
        }, function(error) {
          self.error = error;
        });
      }
    ]
  });
