import React from 'react'
import Modal from 'react-modal'
import { qubitModalBus, QubitModalForm } from 'views/qubitModalForm'
import { StemList } from 'views/qubitlist'
import { MeasureList } from 'views/measurelist'

export class QubitView extends React.Component {
    constructor(props) {
        super(props)
        this.modalBus = qubitModalBus
    }
    componentWillMount() {
        this.setState({
        })
    }
    openForm() {
        this.modalBus.push({cmd: 'open', value: {}})
    }
    render () {
        return (
            <section>
              <div className="hd">
                <button className='new'
                        onClick={this.openForm.bind(this)}>+</button>
             </div>
              <div className="bd"></div>
              <MeasureList></MeasureList>
              <StemList></StemList>
              <QubitModalForm />
            </section>
        )
    }

}
