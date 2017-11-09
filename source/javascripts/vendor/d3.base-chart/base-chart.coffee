d3.chart ?= {}

class d3.chart.BaseChart

    constructor: ->
        @accessors = {} unless @accessors?
        @accessors.width = 100
        @accessors.height = 100
        @accessors.margin =
            top: 0
            right: 0
            bottom: 0
            left: 0
        @accessors.x_scale = d3.scale.linear()
        @accessors.y_scale = d3.scale.linear()
        @buildAccessors()


    #generate getters/setters for properties in accessors
    buildAccessors: ->
        for name, accessor of @accessors
            continue if this[name]?
            do (name, accessor) =>
                this[name] = (value) ->
                    return accessor unless arguments.length
                    accessor = value
                    return this

    draw: (selection) =>
        me = @
        selection.each (d, i) -> me._draw(this, d, i)

    _draw: (element, data, i) ->
        throw "_draw not implemented!"
