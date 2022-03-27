---
layout: default
title: "Python Journey"
---
# {{ page.topic}}

Follow the pages here to get up and running with Python. Pages include:

- How to get up and running with Python, how to install a development environment, and how to get started with Git.
- Common frameworks, modules and tools which are used frequently in my AoC solutions.

## Links Index

<ol>
  {% assign top_level = site.data.navigation.pages | where: 'name', page.title %}
  {% for member in top_level[0].members %}
      <li><a href="{{ member.link | absolute_url }}">{{ member.name }}</a></li>
  {% endfor %}
</ol>