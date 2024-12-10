
from app import app
from flask import request, session, redirect, url_for


@app.errorhandler(404)
def page_not_found(error):
    if 'conectado' in session:
        print("Usuario conectado, redirigiendo al inicio.")
    else:
        print("Usuario no conectado, redirigiendo al inicio.")
    return redirect(url_for('inicio'))