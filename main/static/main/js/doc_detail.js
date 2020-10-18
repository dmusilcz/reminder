$(function () {

  /* Functions */

  var loadDetail = function () {
    var btn = $(this);
    $.ajax({
      url: btn.attr("data-url"),
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        $("#modal-doc").modal("show");
      },
      success: function (data) {
        $("#modal-doc .modal-content").html(data.modal_content);
      }
    });
  };


  /* Binding */

  $(document).on("click", ".js-doc-detail", loadDetail);
});