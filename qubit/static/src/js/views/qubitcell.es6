import React from 'react'
import $ from 'jquery'
import ReactDOM from 'react-dom'
import Modal from 'react-modal'
import { socketStream, updatedSteam } from 'bus'

export class QubitCell extends React.Component {

    render() {
        return (
            <div className="qubit cell" key={i}>
              <div className="hd">
                <label>{this.props.data.name}<span>id: {this.props.data.id}</span></label>
              </div>
              <div className='bd'>
                <ul>
                  <li><label>flying: </label><span>{this.props.data.flying.toString()}</span></li>
                  <li><label>is_spout: </label><span>{this.props.data.is_spout.toString()}</span></li>
                  <li><label>is_stem: </label><span>{this.props.data.is_stem.toString()}</span></li>
                  <li><label>entangle: </label><span>{this.props.data.entangle}</span></li>
                  <li><label>created at: </label><span>{this.props.data.created_at}</span></li>
                </ul>
                <pre>{this.props.data.monad}</pre>
              </div>
              <div className='ft'>
                <button data-name={this.props.data.name} data-qid={this.props.data.id}
                        onClick={self.getLast.bind(self)}>get last</button>
                <button data-name={this.props.data.name} data-qid={this.props.data.id}
                        onClick={self.delete.bind(self)}>delete</button>
                <div className="last">
                  {self.showData(this.props.data.id)}
                </div>
                <div className="chart">
                  <TSChart width='500' height='200'></TSChart>
                </div>
              </div>
            </div>
        ) 
    }
}
