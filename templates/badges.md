## Tech Stack
{% for badge in list %}<img src="{{ badge.url }}" alt="{{ badge.name | default("badge") }}"/>{% endfor %}