import React from 'react'
import $ from 'jquery'
import ReactDOM from 'react-dom'
import Modal from 'react-modal'
import { SpoutForm } from 'views/spoutform'
import { SpoutList } from 'views/spoutlist'


export class SpoutView extends React.Component {
    componentWillMount() {
        this.setState({
        })
    }
    render () {
        return (
            <section className="spout">
              <div className="hd">
                <button className='new' onClick={this.openForm.bind(this)}>+</button>
             </div>
              <div className="bd"></div>
              <SpoutList></SpoutList>
              <SpoutForm></SpoutForm>
              <Modal isOpen={this.state.modal_open}>
                <SpoutForm submit={this.closeForm.bind(this)}></SpoutForm>
              </Modal>
            </section>
        )
    }
    openForm() {
        this.setState({
            modal_open: true
        })
    }
    onSuccessAdded() {
        this.closeForm()
    }
    closeForm() {
        this.setState({
            modal_open: false
        })
    }

}
