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
        var navbar = document.getElementById("menu_navbar_container");
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
          $("#docs-list").html(data.html_docs_list);
          $("#modal-doc").modal("hide");
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
  $("#doc-function-buttons").on("click", ".js-search", loadForm);
  $("#modal-doc").on("submit", ".js-search-form", saveForm);

});