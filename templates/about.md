{% if path %}
{{ read_custom_file(path) }}
{% elif content %}
{{ content }}
{% else %}
<!-- No custom content provided -->
{% endif %}