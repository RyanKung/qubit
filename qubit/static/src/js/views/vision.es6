import * as d3 from 'd3'
import React from 'react'
import ReactDOM from 'react-dom'

export class Axis extends React.Component {
    static propTypes = {
        axis: React.PropTypes.func.isRequired,
        transform: React.PropTypes.string
    }
    static defaultProps = {
        tranform: 'translate(0 100)'
    }
    constructor(props) {
        super(props)
    }
    componentDidMount() {
        this.renderAxis()
    }
    componentDidUpdate() {
        this.renderAxis()
    }
    renderAxis() {
        d3.select(this.refs.axis).call(this.props.axis)
    }
    render() {
        return (<g className="axis" ref="axis" transform={this.props.transform} />)
    }
}


export class Line extends React.Component {
    static propTypes = {
        colors: React.PropTypes.func,
        data: React.PropTypes.object,
        interpolationType: React.PropTypes.string
    }
    static defaultProps = {
        stroke: 'blue',
        fill: 'none',
        strokeWidth: 1
    }
    constructor(props){
        super(props)
    }
    render() {
        let { path, stroke, fill, strokeWidth } = this.props
        return (
            <path
              ref='path'
              d={path}
              fill={fill}
              stroke={stroke}
              strokeWidth={strokeWidth}
              />
        )
    }
}

export class DataSeries extends React.Component {
    static propTypes = {
        colors: React.PropTypes.func,
        data: React.PropTypes.array.isRequired,
        interpolationType: React.PropTypes.func,
        xScale: React.PropTypes.func,
        yScale: React.PropTypes.func,
        getValue: React.PropTypes.func
    }
    static defaultProps = {
        data: [],
        interpolationType: d3.curveCardinal,
        colors: d3.scaleOrdinal(d3.schemeCategory10),
        getValue: (x) => { return x.raw },
        metris: ['mean']
    }
    constructor (props) {
        super(props)
    }
    render () {
        let { data, colors, interpolationType,
              xScale, yScale, getValue, metris } = this.props
        let genLine = (key) => {
            return d3.line()
                .curve(interpolationType)
                .x((d) => { return xScale(new Date(d[0]))})
                .y((d) => { return yScale(getValue(d[1][key]))})
        }
        let lines = metris.map((series, id) => {
            return (
                <g key={id}>
                  <Line path={genLine(series)(data)}
                        stroke={colors(id)}
                        key={id}
                        />
                </g>
            )
        })
        return (
            <g>
              <g>{lines}</g>
            </g>
        )
    }
}

export class TSChart extends React.Component {
    static propTypes = {
        width: React.PropTypes.number,
        height: React.PropTypes.number,
        paddingTop: React.PropTypes.number,
        paddingLeft: React.PropTypes.number,
        data: React.PropTypes.array.isRequired
    }
    static defaultProps = {
        paddingTop: 50,
        paddingLeft: 50,
        width:  300,
        height: 300,
        xMapper: (d) => {return new Date(d)},
        yMapper: (d) => {return d['min']['raw']}
    }
    constructor(props) {
        super(props)
    }
    render() {
        // let self = this
        /** 
        [[ts1, {k1: v1, k2: v2}], [ts2, {k1: v1, k2: v2}], ..]
        **/
        let getYMaxMin = (fn) => {
            return (data) => {
                let judgeValue = (data) => {
                    var res
                    return fn(Object.keys(data).map((i) => {  // {k1:v1, k2:v2, ..}
                        if (data[i] !== null && data[i] !== undefined && typeof data[i] == 'object') {
                            res = fn([judgeValue(data[i])])
                        } else {
                            res = data[i]  // [v1, v2, ..]
                        }
                        return res
                    }))
                }
                return judgeValue(data[1])
            }
        }
        let { width, height, data, paddingLeft, paddingTop, xMapper, yMapper } = this.props
        data = data.map((d, i) => {
            return [xMapper(d[0]), yMapper(d[1])]
        })
        let yMinMax = [
            d3.min(data, getYMaxMin(d3.min)),
            d3.max(data, getYMaxMin(d3.max))
        ]
        let xMaxMin = [
            d3.min(data.map((d) => { return new Date(d[0]) })), // [t1, t2, .., tn]
            d3.max(data.map((d) => { return new Date(d[0]) }))
        ]

        let xScale = d3.scaleTime()
            .domain(xMaxMin)
            .range([10, width])

        let yScale = d3.scaleLinear()
            .domain(yMinMax)
            .range([height, 10])
        console.log(yMinMax, xMaxMin)

        let xAxis = d3.axisBottom(xScale)
        let yAxis = d3.axisRight(yScale)
        let xTrans = `translate(0, ${ height })`
        let yTrans = `translate(${ width }, 0)`
        return (
            <svg width={width + paddingLeft} height={height + paddingTop}>
              <Axis axis={xAxis} transform={xTrans} />
              <Axis axis={yAxis} transform={yTrans} />

              <DataSeries
                xScale={xScale}
                yScale={yScale}
                xAxis={xAxis}
                yAxis={yAxis}
                xTrans={xTrans}
                yTrans={yTrans}
                data={data}
                width={width}
                height={height}
                />
            </svg>
        )
    }
}
