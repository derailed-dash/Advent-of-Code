---
layout: default
title: Advent of Code 2021
---
# {{ page.topic}} {{ page.year }}

## Day Index

<ul>
  {% assign the_year = site.data.navigation.pages | where: 'name', page.year %}
  {% for member in the_year[0].members %}
      <li><a href="{{ member.link | relative_url }}">{{ member.name }}</a></li>
  {% endfor %}
</ul>