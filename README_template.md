<div style="background-color:#1e2030; width: 100vw">

<!-- Banner -->
<img src="./assets/banner.jpeg" style="width: 100vw"/>

<div align="center">

## Hi, I am [Hyperoot](hyperoot.dev)

I am a python developer. I [learn in public](https://mindmaze.hyperoot.dev/).
</div>

<div align="center">

## Connect with Me

<a href="https://github.com/HYP3R00T" target="_blank">
<img src="https://img.shields.io/badge/github-181717?style=for-the-badge&logo=github&logoColor=white" style="height: 32px"/>
</a>
<a href="https://www.linkedin.com/in/rajesh-kumar-das/" target="_blank">
<img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white" style="height: 32px"/>
</a>
<a href="https://mastodon.social/@hyp3r00t" target="_blank">
<img src="https://img.shields.io/badge/mastodon-6364FF?style=for-the-badge&logo=mastodon&logoColor=white" style="height: 32px"/>
</a>
<a href="https://www.youtube.com/@hyp3r00t" target="_blank">
<img src="https://img.shields.io/badge/youtube-FF0000?style=for-the-badge&logo=youtube&logoColor=white" style="height: 32px"/>
</a>
<a href="https://discord.gg/tWZRBhaPhd" target="_blank">
<img src="https://img.shields.io/badge/discord-5865F2?style=for-the-badge&logo=discord&logoColor=white" style="height: 32px"/>
</a>
<a href="https://blogs.hyperoot.dev/" target="_blank">
<img src="https://img.shields.io/badge/hashnode-2962FF?style=for-the-badge&logo=hashnode&logoColor=white" style="height: 32px"/>
</a>
</div>

<div align="center">

## Latest YouTube Videos
</div>

{% for title, link in videos %}
- [{{ title }}]({{ link }})
{% endfor %}

<div align="center">

## Latest Blog Posts
</div>

{% for title, link in blogs %}
- [{{ title }}]({{ link }})
{% endfor %}
</div>