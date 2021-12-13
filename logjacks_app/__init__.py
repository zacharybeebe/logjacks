from flask import Flask, request, render_template, redirect, url_for, session, flash, send_file
from os import remove
from os.path import isfile
from datetime import timedelta
# from flask_login import ()
# from flask_mail import ()
# from flask_wft import ()
# from flask_debugtoolbar import ()
from logjacks_app.config.app_config import *
from logjacks_app.fake_data.fake_data import populate_fake_stand, choice

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config[''] = ''
# app.config[''] = ''
# app.config[''] = ''
# app.config[''] = ''

from logjacks_app.database.models import (
    db,
    User,
    Stand,
    Plot,
    Tree,
    Log
)


create_data = False
if create_data:
    db.drop_all()
    db.create_all()
    populate_fake_stand(db, User, Stand, Plot, Tree, Log, 'puget wa con', 45, 40, 'test', 5)
    for plot_factor in [-25, -30, 20, 33.3, 40]:
        locale = choice(['puget wa con', 'puget wa hwd', 'coastal wa con', 'coastal wa hwd'])
        age = choice([25, 35, 45, 65])
        populate_fake_stand(db, User, Stand, Plot, Tree, Log, locale, age, plot_factor, 'fake', 5)

app.permanent_session_lifetime = timedelta(seconds=360)

from logjacks_app.routes import public#, dashboard
