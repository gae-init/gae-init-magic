$(() => {
  initCommon();
  hljs.initHighlighting();

  $('#icon').selectize({
    render: {
      item: function(item, escape) {
        return (
          "<div> <i class='fa fa-" +
          item.value +
          " fa-fw'></i> " +
          item.text +
          '</div>'
        );
      },
      option: function(item, escape) {
        return (
          "<div> <i class='fa fa-" +
          item.value +
          " fa-fw'></i> " +
          item.text +
          '</div>'
        );
      },
    },
    sortField: 'text',
  });

  $('html.auth').each(() => {
    initAuth();
  });

  $('html.user-list').each(() => {
    initUserList();
  });

  $('html.user-merge').each(() => {
    initUserMerge();
  });

  $('html.model-view').each(() => {
    init_model_view();
  });

  $('html.project-update').each(() => {
    init_project_update();
  });

  $('html.model-update').each(() => {
    init_model_update();
  });

  $('html.property-update').each(() => {
    init_property_update();
  });
});
