---
layout: default
title: Home
---

{% include header.html %}
<main class="container">
  {% include work.html %}
  {% include writeups.html %}
  {% include tools.html %}
  {% include talks.html %}
  {% include contact.html %}
</main>
<p class="text-center">&copy; {{ site.time | date: '%Y' }} anand sreekumar</p>
