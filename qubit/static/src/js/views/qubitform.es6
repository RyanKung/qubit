import React from 'react'
import $ from 'jquery'
import ReactDOM from 'react-dom'
import Form from 'libs/ajaxform'
import { str, getattr, bool } from 'libs/fn'
import { TSChart } from 'views/vision'
import { DataTable } from 'libs/object2table'


export class QubitForm extends React.Component {
    componentWillMount() {
        this.setState({
            result: false,
            hint: ''
        })
    }
    success(res) {
        if (res.result == 'ok') {
            this.setState({
                result: 'successed! qubit id: ' + res.data
            })
            this.props.submit && this.props.submit(this.data)
        } else {
            window.alert('failed to post data')
        }
    }
    cancel() {
        this.props.cancel && this.props.cancel()
    }
    testMonad(e) {
        let self = this
        let content = e.target.value
        let url = '/qubit/monad/test/'
        let data = {'monad': content}
        $.ajax({
            'url': url,
            'type': 'POST',
            'data': JSON.stringify(data),
            'dataType': 'json',
            'contentType': 'application/json',
            'success': (resp) => {
                self.setState({
                    monadInfo: resp.data
                })
            }
        })
    }
    showMonadData() {
        return (<DataTable data={this.state.monadInfo} />)
    }
    toDict(data) {
        return data.reduce(function(x, y) {
            x[y.name] = y.value
            return x
        }, {})
    }
    series($dom) {
        let resp = this.toDict($dom.serializeArray())
        return JSON.stringify(resp)
    }
    render() {
        let data = this.props.data
        return (
            <section className="card">
              <div className="hd"><h1>New Qubit</h1></div>
              <Form className="bd" action="/qubit/"
                    series={this.series.bind(this)}
                    contentType='application/json'
                    success={this.success.bind(this)}
                    method='post'>
                <fieldset>
                  <input placeholder="name" name="name"
                         required
                         defaultValue={bool(getattr(data, 'name', ''))}/>
                  <input placeholder='rate (ms)' name='rate'
                         type='number'
                         defaultValue={getattr(data, 'rate', '')}/>
                  <input placeholder='Qubit:%s'
                         name='entangle'
                         defaultValue={bool(getattr(data, 'rate', ''))}
                         type='text' />
                </fieldset>
                <fieldset>
                  <label>
                    <span>flying</span>
                    <input placeholder='flying'
                           defaultChecked={bool(getattr(data, 'flying', ''))}
                           name='flying'
                           type='checkbox' />
                  </label>
                  <label>
                    <span>is spout</span>
                    <input name='is_spout'
                           defaultChecked={bool(getattr(data, 'is_spout', ''))}
                           type='checkbox' />
                    </label>
                  <label>
                    <span>is stem</span>
                    <input name='is_stem'
                           defaultChecked={bool(getattr(data, 'is_stem', ''))}
                           type='checkbox' />
                  </label>
                  <label>
                    <span>store</span>
                    <input name='store'
                           defaultChecked={bool(getattr(data, 'store', ''))}
                           type='checkbox' />
                    </label>
                </fieldset>
                <fieldset className="long">
                  <label>monad</label>
                  <textarea onBlur={this.testMonad.bind(this)}
                            name="monad" placeholder="monad"
                            defaultValue={ getattr(data, 'monad', '') } />
                  <em className="monadInfo">
                    {this.state.monadInfo && this.showMonadData()}
                  </em>
                </fieldset>
                <fieldset className="long">
                  <label>comment</label>
                  <textarea name="comment"
                            defaultValue={ getattr(data, 'comment', '') }
                            placeholder="coment" />
                </fieldset>

                <fieldset className="submit block">
                  <input name="submit"
                         type="submit"
                         value="submmit" />
                  <input name="cancel" type="button"
                         onClick={this.cancel.bind(this)}
                         value="cancel" />
                </fieldset>
              </Form>

              <div className="ft">
                <em>{this.state.hint}</em>
                <div>{this.state.result}</div>
              </div>
            </section>
        )
    }
}
