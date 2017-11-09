d3.base-chart
=============

base class for a reusable d3.js component written in coffeescript
Inspired by [dandavison](https://gist.github.com/dandavison/4152640) and
[wprater](https://gist.github.com/wprater/5682740).

You should inherit from this class, append any parameters to the constructor
`@accessors` that will be useful for the chart, and write a `_draw(element,
data, i)` function that will do the actual drawing.

Example
-------
```coffeescript
class d3.chart.MyChart extends d3.chart.BaseChart
    constructor: ->
        @accessors = {} unless @accessors?
        @accessors.x_value = (d) -> d.x # default value
        super

    _draw: (element, data, i) ->
        g = d3.select element
            .data data

        g.enter()
            .append "rect"
            .attr "x", @x_value()

        g
            .exit()
            .remove()

my = new d3.chart.MyChart()
    .x_value (d) -> d.time # set another function

d3.select "body"
    .datum json
    .call my.draw
```

Everything you add to the `@accessors` in the constructor will be
available with a getter/setter method.

Depends on
----------
[D3](d3js.org)
