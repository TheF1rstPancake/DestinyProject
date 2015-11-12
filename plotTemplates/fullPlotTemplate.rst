{{destinyGraph.title}}
{% for c in destinyGraph.title -%}
    =
{%- endfor %}

:date: {{date}}
:modified: {{date}}
{% if tags %}
:tags: {% for t in tags -%} 
        {{t}}, 
        {%- endfor %}
{% endif %}
:authors: {{author}}
:summary: {{destinyGraph.subtitle}}
:category: {{category}}
{% if url %}
:url: {{url}}
:save_as: {{url}}
{% endif %}

`View project on Github <https://github.com/Jalepeno112/DestinyProject/>`_

.. html::
    <div id="{{destinyGraph.divTitle}}">
            <svg></svg>
            <script src='{{destinyGraph.javascriptFileLocation}}'></script>
    </div>

{% if destinyGraph.plotText %}
{{destinyGraph.plotText}}
{% endif %}
