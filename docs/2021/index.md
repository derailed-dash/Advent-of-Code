---
title: Advent of Code 2021
---
# {{ page.title }} 

## Day Index

<ul>
  {% for item in site.data.navigation %}
  {% if item.type == "day" and item.year == "2021" %}
      <li><a href="{{ site.url }}{{ site.baseurl }}{{ item.link }}">{{ item.name }}</a></li>
  {% endif %}
  {% endfor %}
</ul>