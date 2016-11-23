import d3 from 'd3js'
import React from 'react'
import ReactDOM from 'react-dom'


export class SVG extends React.Component {
    render () {
        return (<svg width={this.props.width || 500} height={this.props.height || 500}></svg>)
    }
}

export class Group extends React.Component {
     render () {
         return (<g transform={this.props.transform}></g>)
    }
   
}
