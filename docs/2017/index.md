---
layout: default
title: Advent of Code 2017
---
# {{ page.topic}} {{ page.year }}

Welcome to [AoC 2017](https://adventofcode.com/2017){:target="_blank"}!

Walkthroughs coming soon!

## Day Index

<ol>
  {% assign the_year = site.data.navigation.pages | where: 'name', page.year %}
  {% for member in the_year[0].members %}
      <li><a href="{{ member.link | absolute_url }}">{{ member.problem }}</a></li>
  {% endfor %}
</ol>