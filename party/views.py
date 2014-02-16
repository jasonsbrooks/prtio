from flask import (Flask, render_template, Response, request, 
    Blueprint, redirect, send_from_directory, send_file, jsonify, g)

party = Blueprint('party', __name__, template_folder="")

@party.route('/')
def index():
    return render_template('templates/party.html')