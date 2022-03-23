---
layout: default
title: Advent of Code 2021
---
# {{ page.topic}} {{ page.year }}

**Welcome to AoC 2021!**

A clumsy elf has dropped the sleigh keys into the ocean.  You need to recover the keys in order to save Christmas.

This was a tough AoC.  The first half was easy enough.  But the second half had a lot of time-consuming challenges. I had taken a few days off work over Christmas.  And it was just as well.  I needed the time!!

Ready to save Christmas?  Follow the links below.

## Day Index

<ol>
  {% assign the_year = site.data.navigation.pages | where: 'name', page.year %}
  {% for member in the_year[0].members %}
      <li><a href="{{ member.link | absolute_url }}">{{ member.problem }}</a></li>
  {% endfor %}
</ol>