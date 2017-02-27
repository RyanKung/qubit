import React from 'react'


export class DataTable extends React.Component {
    render() {
        let data = this.props.data
        return (
            <table>
              <tbody>
                <tr>
                  {Object.keys(data).map(function(d, i) {
                      return (<th key={i}>{d}</th>)
                  })}
                </tr>
                <tr>
                  {Object.keys(data).map(function(d, i) {
                      return (<td key={i}>{JSON.stringify(data[d])}</td>)
                  })}
                </tr>
              </tbody>
            </table>
        )
    }
    
}
