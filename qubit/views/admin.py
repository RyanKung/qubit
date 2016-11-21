from flask import render_template
from qubit.core.app import app

__all__ = ['admin']


@app.route('/qubit/admin/')
def admin():
    return render_template('index.html')
