import * as d3 from 'd3'
import React from 'react'
import ReactDOM from 'react-dom'

var n = 40,
    random = d3.randomNormal(0, .2),
    data = d3.range(n).map(random)


export class TSChart extends React.Component {
    componentWillMount () {
        var margin = {top: 20, right: 20, bottom: 20, left: 40}
        var width = +this.props.width - margin.left - margin.right
        var height = +this.props.height - margin.top - margin.bottom
        var transform = 'translate(' + margin.left + ',' + margin.top + ')'
        var x = d3.scaleLinear().domain([0, n - 1]).range([0, width])
        var y = d3.scaleLinear().domain([-1, 1]).range([height, 0])
        var line = d3.line()
            .x(function(d, i) { return x(i); })
            .y(function(d, i) { return y(d); })

        this.setState({
            width: width,
            height: height,
            transform: transform,
            x: x,
            y: y,
            line: line
        })
    }
    renderChart() {
        var svg = d3.select(this.getDOMNode())
    }
    render () {
        return (
            <svg width={this.props.width} height={this.props.height}>
              <g transform={this.state.transform}>
                <defs>
                  <chilpPath id='chip'>
                    <rect width={this.state.width} height={this.state.height}></rect>
                  </chilpPath>
                </defs>
              </g>
            </svg>)
    }
}
