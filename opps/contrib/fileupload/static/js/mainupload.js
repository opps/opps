/*
 * jQuery File Upload Plugin JS Example 6.7
 * https://github.com/blueimp/jQuery-File-Upload
 *
 * Copyright 2010, Sebastian Tschan
 * https://blueimp.net
 *
 * Licensed under the MIT license:
 * http://www.opensource.org/licenses/MIT
 */

/*jslint nomen: true, unparam: true, regexp: true */
/*global $, window, document */

(function ($) {
  'use strict';

  // Initialize the jQuery File Upload widget:
  $('#fileupload').fileupload();

  // Enable iframe cross-domain access via redirect option:
  $('#fileupload').fileupload(
    'option',
    'redirect',
    window.location.href.replace(
      /\/[^\/]*$/,
      '/cors/result.html?%s'
      )
    );

  if (window.location.hostname === 'blueimp.github.com') {
    // Demo settings:
    $('#fileupload').fileupload('option', {
      url: '//jquery-file-upload.appspot.com/',
      maxFileSize: 5000000,
      acceptFileTypes: /(\.|\/)(gif|jpe?g|png)$/i,
      process: [
    {
      action: 'load',
      fileTypes: /^image\/(gif|jpeg|png)$/,
      maxFileSize: 20000000 // 20MB
    },
      {
        action: 'resize',
      maxWidth: 1440,
      maxHeight: 900
      },
      {
        action: 'save'
      }
    ]
    });
    // Upload server status check for browsers with CORS support:
    if ($.support.cors) {
      $.ajax({
        url: '//jquery-file-upload.appspot.com/',
        type: 'HEAD'
      }).fail(function () {
        $('<span class="alert alert-error"/>')
        .text('Upload server currently unavailable - ' +
          new Date())
        .appendTo('#fileupload');
      });
    }
  } else {
    // Load existing files:
    $('#fileupload').each(function () {
      var that = this;
      $.getJSON(this.action, function (result) {
        if (result && result.length) {
          $(that).fileupload('option', 'done')
        .call(that, null, {result: result});
        }
      });
    });
  }

  $('#replicate').click(function(e){
    var title = $("[name='title']").first().val();
    var caption = $("[name='caption']").first().val();
    var source = $("[name='source']").first().val();
    var order = $("[name='order']").first().val();
    var tags = $("[name='tags']").first().val();

    $("[name='title']").val(title);
    $("[name='caption']").val(caption);
    $("[name='source']").val(source);
    $("[name='order']").val(order);
    $("[name='tags']").val(tags);

    arrange_orders();
    e.preventDefault();
    return false;
  });

  $('#clear-replicate').click(function(e){
    var title = $("[name='title']").first().val();
    var caption = $("[name='caption']").first().val();
    var source = $("[name='source']").first().val();
    var order = $("[name='order']").first().val();
    var tags = $("[name='tags']").first().val();

    $("[name='title']").val('');
    $("[name='caption']").val('');
    $("[name='source']").val('');
    $("[name='order']").val('');
    $("[name='tags']").val('');

    $("[name='title']").first().val(title);
    $("[name='caption']").first().val(caption);
    $("[name='source']").first().val(source);
    $("[name='order']").first().val(order);
    $("[name='tags']").first().val(tags);

    e.preventDefault();
    return false;
  });

  $('#arrange-orders').click(function(e){
    arrange_orders();
    e.preventDefault();
    return false;
  });

  function arrange_orders(){
    var order = $("[name='order']").first().val();
    if (order == "") {order = 0;}
    order = parseInt(order);
    $("[name='order']").each(function(){
      $(this).val(order);
      order = order + 1;
    });
  }

})(django.jQuery);
