from flask import (Flask, render_template, Response, request, 
    Blueprint, redirect, send_from_directory, send_file, jsonify, g, url_for)

splash = Blueprint('splash', __name__, template_folder="")

@splash.route('/')
def home():
    if g.user is not None and g.user.is_authenticated():
        return redirect(url_for('party.index'))
    else:
        return render_template('templates/home.html')