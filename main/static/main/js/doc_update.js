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
              var expiry_date = $("#id_expiry_date");
              var reminder_div = $("#div_id_reminder");
              const value = expiry_date.val();
              const trimmed = value.trim();
              if (trimmed) {
                  reminder_div.show();
                } else {
                  reminder_div.hide();
                }
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
          // $("#docs-col").html(data.html_docs_list);
          $("#main").html(data.html_docs_list);
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
  $(document).on("click", ".js-update-doc", loadForm);
  // $("#doc-col").on("click", ".js-delete-doc", loadForm);
  $("#modal-doc").on("submit", ".js-doc-update-form", saveForm);
  // $('#modal-doc').on("click", ".js-update-doc", loadForm);
  // $("#modal-doc").on("click", ".js-update-doc", loadForm);

});