from django import template
from django.utils.translation import ugettext_lazy as _

register = template.Library()


@register.simple_tag
def upload_js(container=None):
    if container:
        container_sources = container.source if container.source else ''
        container_tags = container.tags if container.tags else ''
        title = container.title
    else:
        container_sources = container_tags = title = ''
    return u"""
<!-- The template to display files available for upload -->
<script id="template-upload" type="text/x-tmpl">
{% for (var i=0, file; file=o.files[i]; i++) { %}
    <tr class="template-upload fade">
        <td class="preview"><span class="fade"></span></td>
        <td class="name"><span>{%=file.name%}</span></td>
        <td class="size"><span>{%=o.formatFileSize(file.size)%}</span></td>

        <td class="extra">
        <label>
        """ + unicode(_(u'Title')) + u""": <input type="text"
        name="title" value='""" + \
        title + u"""' required></label>
        <label>""" + unicode(_(u'Caption')) + u""":
            <textarea name="caption" rows="2" colums="1">
                        </textarea></label>
        <label>""" + unicode(_(u'Order')) + u""": <input type="text"
        name="order" value="0"/></label>
        <label>""" + unicode(_(u'Source')) + u""":
            <input type="text" name="source" value='""" + \
        container_sources + u"""'></label>
        <label>""" + unicode(_(u'Tags')) + u""":
            <input type="text" name="tags" value='""" + \
        container_tags + u"""'></label>
        </td>
        {% if (file.error) { %}
            <td class="error" colspan="2">
            <span class="label label-important">
            {%=locale.fileupload.error%}
            </span>
            {%=locale.fileupload.errors[file.error] || file.error%}</td>
        {% } else if (o.files.valid && !i) { %}
            <td>
            <div class="progress progress-success progress-striped active">
                <div class="bar" style="width:0%;"></div>
            </div>
            </td>
            <td class="start">{% if (!o.options.autoUpload) { %}
                <button class="btn btn-success">
                    <i class="icon-upload icon-white"></i>
                    <span>{%=locale.fileupload.start%}</span>
                </button>
            {% } %}</td>
        {% } else { %}
            <td colspan="2"></td>
        {% } %}
        <td class="cancel">{% if (!i) { %}
            <button class="btn btn-warning">
                <i class="icon-ban-circle icon-white"></i>
                <span>{%=locale.fileupload.cancel%}</span>
            </button>
        {% } %}</td>
    </tr>
{% } %}
</script>
<!-- The template to display files available for download -->
<script id="template-download" type="text/x-tmpl">
{% for (var i=0, file; file=o.files[i]; i++) { %}
    <tr class="template-download fade">
        {% if (file.error) { %}
            <td></td>
            <td class="name"><span>{%=file.name%}</span></td>
            <td class="size">
            <span>{%=o.formatFileSize(file.size)%}</span></td>
            <td class="error" colspan="2">
            <span class="label label-important">
            {%=locale.fileupload.error%}</span>
            {%=locale.fileupload.errors[file.error] || file.error%}</td>
        {% } else { %}
            <td class="preview">{% if (file.thumbnail_url) { %}
                <a href="{%=file.url%}" title="{%=file.name%}"
                   rel="gallery" download="{%=file.name%}">
                   <img src="{%=file.thumbnail_url%}"></a>
            {% } %}</td>
            <td class="name">
                <a href="{%=file.url%}" title="{%=file.name%}"
                   rel="{%=file.thumbnail_url&&'gallery'%}"
                   download="{%=file.name%}">{%=file.name%}</a>
            </td>
            <td class="size">
            <span>{%=o.formatFileSize(file.size)%}</span></td>
            <td class="success-message" colspan="2">
                {%=locale.fileupload.success%}
            </td>
        {% } %}
        <!-- td class="delete">
            <button class="btn btn-danger"
            data-type="{%=file.delete_type%}" data-url="{%=file.delete_url%}">
                <i class="icon-trash icon-white"></i>
                <span>{%=locale.fileupload.destroy%}</span>
            </button>
            <input type="checkbox" name="delete" value="1">
        </td -->
    </tr>
{% } %}
</script>
"""
