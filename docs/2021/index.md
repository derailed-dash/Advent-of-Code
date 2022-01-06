---
title: Advent of Code
year: "2021"
---

# {{ page.title }}-{{ page.year }} 

## Day Index

<ul>
  {% assign the_year = site.data.navigation.pages | where: 'name', page.year %}
  {% for member in the_year[0].members %}
      <li><a href="{{ member.link | relative_url }}">{{ member.name }}</a></li>
  {% endfor %}
</ul>