---
layout: default
title: Advent of Code 2020
---
# {{ page.topic}} {{ page.year }}

Sorry, still working through 2021 documentation!

## Day Index

<ul>
  {% assign the_year = site.data.navigation.pages | where: 'name', page.year %}
  {% for member in the_year[0].members %}
      <li><a href="{{ member.link | relative_url }}">{{ member.name }} - {{ member.problem }}</a></li>
  {% endfor %}
</ul>