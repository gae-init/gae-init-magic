'use strict';

angular.
  module('core.{{model_db.variable_name}}').
  factory('{{model_db.name}}', ['$resource',
    function($resource) {
      return $resource('/api/v1/admin/{{model_db.variable_name}}/', {}, {
        query: {
          method: 'GET',
          cache: true
        }
      });
    }
  ]);
