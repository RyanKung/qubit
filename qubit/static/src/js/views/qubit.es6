import React from 'react'
import Modal from 'react-modal'
import { QubitForm } from 'views/qubitform'
import { QubitList } from 'views/qubitlist'


export class QubitView extends React.Component {
    componentWillMount() {
        this.setState({
        })
    }
    render () {
        return (
            <section>
              <div className="hd">
                <button className='new' onClick={this.openForm.bind(this)}>+</button>
             </div>
              <div className="bd"></div>
              <QubitList></QubitList>
              <Modal isOpen={this.state.modal_open}>
                <QubitForm cancel={this.closeForm.bind(this)}
                           submit={this.closeForm.bind(this)}></QubitForm>
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
