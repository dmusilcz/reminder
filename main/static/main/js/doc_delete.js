var close_messages = function (element) {
    $(element).hide()
};

$(function () {

  /* Functions */

  var loadForm = function () {
    var btn = $(this);
    $.ajax({
      url: btn.attr("data-url"),
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        $("#modal-doc").modal("show");
      },
      success: function (data) {
        $("#modal-doc .modal-content").html(data.html_form);
      }
    });
  };

  var saveForm = function () {
    var form = $(this);
    $.ajax({
      url: form.attr("action"),
      data: form.serialize(),
      type: form.attr("method"),
      dataType: 'json',
      success: function (data) {
        if (data.form_is_valid) {
          $("#modal-doc").modal("hide");
          // location.href= "";
          if (data.view === 'L') {
              $(data.doc_id).remove();
              var messages = document.getElementById("messages");
              $(messages).html("<p>Document deleted successfully</p>");
              setTimeout(function () {
                  $(close_messages(messages));
              }, 3000);
          } else {
              location.href = "";
          }
        }
        else {
          $("#modal-doc .modal-content").html(data.html_form);
        }
      }
    });
    return false;
  };


  /* Binding */

  // // Create book
  // $(".js-create-book").click(loadForm);
  // $("#modal-book").on("submit", ".js-book-create-form", saveForm);
  //
  // // Update book
  // $("#book-table").on("click", ".js-update-book", loadForm);
  // $("#modal-book").on("submit", ".js-book-update-form", saveForm);

  // Delete book
  $("#docs-col").on("click", ".js-delete-doc", loadForm);
  $("#doc-col").on("click", ".js-delete-doc", loadForm);
  $("#modal-doc").on("submit", ".js-doc-delete-form", saveForm);

});