## 🎥 Latest YouTube Videos
{% if videos %}
{% for video in videos %}- [{{ video.title }}]({{ video.link }})
{% endfor %}
{% else %}
_No recent videos available._
{% endif %}