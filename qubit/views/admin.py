from flask import render_template
from qubit.core.app import app
from qubit.io.redis import pubsub

__all__ = ['admin']


@app.route('/qubit/admin/')
def admin():
    return render_template('index.html')


@app.route('/qubit/admin/test/')
def test():
    pubsub.publish('mychannel', 'fuck')
    pubsub.publish('eventsocket', 'fuck')
    return render_template('index.html')
