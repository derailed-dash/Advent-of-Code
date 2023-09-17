---
layout: default
title: Advent of Code 2016
---
# {{ page.topic}} {{ page.year }}

Welcome to [AoC 2016](https://adventofcode.com/2016){:target="_blank"}, the second Advent of Code!

Walkthroughs are coming soon!

## Day Index

<ol>
  {% assign the_year = site.data.navigation.pages | where: 'name', page.year %}
  {% for member in the_year[0].members %}
      <li><a href="{{ member.link | absolute_url }}">{{ member.problem }}</a></li>
  {% endfor %}
</ol>