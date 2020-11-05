
var verifyDate = function () {
      var expiry_date = $("#id_expiry_date");
      var reminder_div = $("#div_id_reminder");
      const value = expiry_date.val();
      const trimmed = value.trim();
      if (trimmed) {
          reminder_div.show();
        } else {
          reminder_div.hide();
        }
  };

$(function () {
  var showMessages = function(){
    setTimeout(function(){
          var m = document.getElementsByClassName("alert");
          if (m && m.length) {
              m[0].classList.add('hide');
          }
      }, 3000);
  };

  var loadForm = function () {
    var btn = $(this);
    $.ajax({
      url: btn.attr("data-url"),
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        $("#modal-doc").modal("show");
        var body = document.getElementsByTagName("body");
        $(body).css('padding-right', '0px');
      },
      success: function (data) {
        $("#modal-doc .modal-content").html(data.modal_content);
        if (data.action_update){
            verifyDate();
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
          $("#main").html(data.html_docs_list);
          $(".messages-container").html(data.messages);
        }
        else {
          $("#modal-doc .modal-content").html(data.modal_content);
        }
      }
    });
    return false;
  };


  /* Binding */
  var modal_doc = $("#modal-doc");

  // Detail
  $(document).on("click", ".js-doc-detail", loadForm);

  // Update
  $(document).on("click", ".js-update-doc", loadForm);
  modal_doc.on("submit", ".js-doc-update-form", saveForm);

  // Delete
  $(document).on("click", ".js-delete-doc", loadForm);
  modal_doc.on("submit", ".js-doc-delete-form", saveForm);

  // Search
  $(document).on("click", ".js-search", loadForm);
  modal_doc.on("submit", ".js-search-form", saveForm);

  showMessages()

});