// $(function () {
// var reminder_div = $(document.getElementById("div_id_reminder"));
// reminder_div.hide();
// var expiry_date = $(document.getElementById("id_expiry_date"));
//
// expiry_date.on('input', function () {
//     const value = expiry_date.val();
//     const trimmed = value.trim();
//
// if (trimmed) {
//   reminder_div.show();
// } else {
//   reminder_div.hide();
// }
// });
    // });

// $(function () {
// var reminder_div = $(document.getElementById("div_id_reminder"));
// // reminder_div.hide();
// var expiry_date = $(document.getElementById("id_expiry_date"));
//
// var check_expiry_date = function () {
//     const value = expiry_date.val();
//     alert(value);
//     const trimmed = value.trim();
//     alert(trimmed);
//
//     if (trimmed) {
//       reminder_div.show();
//     } else {
//       reminder_div.hide();
//     }
// };
//
// expiry_date.on('input', check_expiry_date());
// check_expiry_date();
    // });

// $(function () {
//   var reminder_div = $(document.getElementById("div_id_reminder"));
//   // reminder_div.hide();
//   var expiry_date = $(document.getElementById("id_expiry_date"));
//
//   expiry_date.on('input', function () {
//       const value = expiry_date.val();
//       const trimmed = value.trim();
//
//       if (trimmed) {
//         reminder_div.show();
//       } else {
//         reminder_div.hide();
//       }
//   });
//
//   const value = expiry_date.val();
//   const trimmed = value.trim();
//
//   if (trimmed) {
//     reminder_div.show();
//   } else {
//     reminder_div.hide();
//   }
// });

// $(function () {
//   var reminder_div = $(document.getElementById("div_id_reminder"));
//   // reminder_div.hide();
//   var expiry_date = $(document.getElementById("id_expiry_date"));
//
//   expiry_date.on('input', function () {
//       const value = expiry_date.val();
//       const trimmed = value.trim();
//
//       if (trimmed) {
//         reminder_div.show();
//       } else {
//         reminder_div.hide();
//       }
//   });
//
//   const value = expiry_date.val();
//   const trimmed = value.trim();
//
//   if (trimmed) {
//     reminder_div.show();
//   } else {
//     reminder_div.hide();
//   }
//     });


var verifyDate = function () {
    var expiry_date = $(document.getElementById("id_expiry_date"));
    console.log(expiry_date);
    var reminder_div = $(document.getElementById("div_id_reminder"));
    const value = expiry_date.val();
    console.log(value);
    const trimmed = value.trim();
    console.log(trimmed);
    if (trimmed) {
        console.log('trimmed true');
        reminder_div.show();
      } else {
        console.log('trimmed false');
        reminder_div.hide();
      }
};


    // var modal_doc = document.getElementById("modal-doc");
    // modal_doc.addEventListener('open', verifyExpiryDate);
    // console.log(verifyExpiryDate);
    // var expiry_date = $(document.getElementById("id_expiry_date"));
    // expiry_date.addEventListener('onload', verifyExpiryDate);


  // $(document).on("change", ".fengyuanchendatepickerinput", baf);
