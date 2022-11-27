---
layout: default
title: Advent of Code 2022
---
# {{ page.topic}} {{ page.year }}

**Welcome to AoC 2022!**

Coming soon!!

Ready to save Christmas?  Follow the links below.

## Day Index

<ol>
  {% assign the_year = site.data.navigation.pages | where: 'name', page.year %}
  {% for member in the_year[0].members %}
      <li><a href="{{ member.link | absolute_url }}">{{ member.problem }}</a></li>
  {% endfor %}
</ol>