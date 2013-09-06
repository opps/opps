// this functions are just a proxy
function opps_editor_popup_selector(path){
    top.tinymce.activeEditor.windowManager.
        getParams().selectfunction(path);
}

function opps_editor_popup_selecto_embed(path){
    top.tinymce.activeEditor.windowManager.
        getParams().selectembedfunction(path);
}

function CustomFileBrowser(field_name, url, type, win) {

    // default functions, meant to be overrided
    var selectfunction = function (){console.log('selecting')}
    var selectembedfunction = function (){
         console.log('selecting embed')
    }

    if (type == 'image'){
        var cmsURL = '/admin/images/get_images/'
        selectfunction = function (path){
            console.log(path);
            window.document.getElementById(field_name).value = path;

            // Try to set the image dimension to 300
            try {
                dt = field_name.split('_');
                new_number = parseInt(dt[1])+3
                dm_selector = dt[0] + "_" + new_number.toString();
                window.document.getElementById(dm_selector).value = '600';
            } catch(err) {
                console.log(err);
            }

            tinymce.activeEditor.windowManager.close();
        };
    }
    tinyMCE.activeEditor.windowManager.open({
        url: cmsURL,
        width: 980,
        height: 500,
        resizable: 'yes',
        scrollbars: 'yes',
        inline: 'no',
        close_previous: 'no',
        buttons: [{
            text: 'Close',
            onclick: 'close'
        }]
    }, {
       field_name: field_name,
       win: win,
       type: type,
       selectfunction: selectfunction,
       selectembedfunction: selectembedfunction
    });
    return false;

}
