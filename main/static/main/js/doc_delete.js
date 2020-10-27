var close_messages = function (element) {
    // $(element).children("p").hide()
    element.classList.remove('message-shown');
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
        var navbar = document.getElementById("menu_navbar_container_wrapper");
        $(navbar).css('margin-right', 'auto')
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
            // var messages = document.getElementById("messages");
            // $(messages).html("<p id='message'>Document deleted successfully</p>");
            // $("#docs-col").html(data.html_docs_list);
            $("#main").html(data.html_docs_list);
            var messages = document.getElementById("message");
            messages.classList.add('message-shown');
            setTimeout(function () {
                $(close_messages(messages));
            }, 3000);
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
  // $("#docs-col").on("click", ".js-delete-doc", loadForm);
  $(document).on("click", ".js-delete-doc", loadForm);
  // $("#doc-col").on("click", ".js-delete-doc", loadForm);
  $("#modal-doc").on("submit", ".js-doc-delete-form", saveForm);
  // $(".js-doc-delete-form").on("submit", saveForm);

});