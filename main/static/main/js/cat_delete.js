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
        $("#modal-cat").modal("show");
      },
      success: function (data) {
        $("#modal-cat .modal-content").html(data.html_form);
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
          $("#modal-cat").modal("hide");
          // location.href= "";
          $(data.cat_id).remove();
          var messages = document.getElementById("messages");
          $(messages).html("<p>Category deleted successfully</p>");
          setTimeout(function () {
              $(close_messages(messages));
          }, 3000);
        }
        else {
          $("#modal-cat .modal-content").html(data.html_form);
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
  $("#cats-col").on("click", ".js-delete-cat", loadForm);
  $("#modal-cat").on("submit", ".js-cat-delete-form", saveForm);

});