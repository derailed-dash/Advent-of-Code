---
layout: default
title: Advent of Code 2015
---
# {{ page.topic}} {{ page.year }}

Welcome to [AoC 2015](https://adventofcode.com/2015){:target="_blank"}, the first ever Advent of Code!

Santa's weather machine is fresh out of stars.  You need to collect stars in order to power the machine.

Ready to save Christmas?  Follow the links below.

## Day Index

<ol>
  {% assign the_year = site.data.navigation.pages | where: 'name', page.year %}
  {% for member in the_year[0].members %}
      <li><a href="{{ member.link | absolute_url }}">{{ member.problem }}</a></li>
  {% endfor %}
</ol>