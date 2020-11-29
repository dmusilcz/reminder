var modal_window = $("#modal");
var modal_content = $(".modal-content");

var verifyDate = function () {
  var expiry_date = $("#id_expiry_date");
  var reminder_div = $("#div_id_reminder");
  const value = expiry_date.val();
  if (value) {
    const trimmed = value.trim();
    if (trimmed) {
        reminder_div.show();
      } else {
        reminder_div.hide();
      }
    } else {
    reminder_div.hide();
  }
  };

$(function () {
  var hideMessages = function(){
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
        modal_window.modal("show");
        var body = document.getElementsByTagName("body");
        $(body).css('padding-right', '0px');
      },
      success: function (data) {
        modal_content.html(data.modal_content);
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
          modal_window.modal("hide");
          $("#main").html(data.html_items_list);
          $(".messages-container").html(data.messages);
          hideMessages();
        }
        else {
          modal_content.html(data.modal_content);
          if (data.action_update){
            verifyDate();
          }
        }
      }
    });
    return false;
  };


  /* Binding */

  // Detail doc
  $(document).on("click", ".js-doc-detail", loadForm);

  // Update doc
  $(document).on("click", ".js-update-doc", loadForm);
  modal_window.on("submit", ".js-doc-update-form", saveForm);

  // Delete doc
  $(document).on("click", ".js-delete-doc", loadForm);
  modal_window.on("submit", ".js-doc-delete-form", saveForm);

  // Update cat
  $(document).on("click", ".js-update-cat", loadForm);
  modal_window.on("submit", ".js-cat-update-form", saveForm);

  // Delete cat
  $(document).on("click", ".js-delete-cat", loadForm);
  modal_window.on("submit", ".js-cat-delete-form", saveForm);

  // Search
  $(document).on("click", ".js-search", loadForm);
  modal_window.on("submit", ".js-search-form", saveForm);

  // Origin
  $(document).on("click", ".js-origin", loadForm);

  // Terms
  $(document).on("click", ".js-terms", loadForm);

  // Privacy policy
  $(document).on("click", ".js-privacy", loadForm);


  hideMessages();

  $("#id_expiry_date").on('textInput input unload', verifyDate);
  verifyDate()

});