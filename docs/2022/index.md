---
layout: default
title: Advent of Code 2022

main_img:
  name: "Star Fruit"
  link: /assets/images/star-fruit.jpg
---
# {{ page.topic}} {{ page.year }}

<img src="{{ page.main_img.link | relative_url }}" alt="{{ page.main_img.name }}" style="margin:15px 10px 10px 10px; float: right; width:300px" />

**Welcome to AoC 2022!**

It's time to [save Christmas](https://adventofcode.com/2022/){:target="_blank"} once more!

We do this by collecting stars each day.  This year, the stars are food for the reindeer!

Follow the links below.

## Day Index

<ol>
  {% assign the_year = site.data.navigation.pages | where: 'name', page.year %}
  {% for member in the_year[0].members %}
      <li><a href="{{ member.link | absolute_url }}">{{ member.problem }}</a></li>
  {% endfor %}
</ol>