---
title: Advent of Code
year: "2021"
---

# {{ page.title }}-{{ page.year }} 

## Day Index

<ul>
  {% assign the_year = site.data.navigation | where: 'name', page.year %}
  {% for member in the_year[0].members %}
      <li><a href="{{ site.url }}{{ site.baseurl }}{{ member.link }}">{{ member.name }}</a></li>
  {% endfor %}
</ul>