# -*- coding: utf-8 -*-
import datetime
import json

from flask import Flask, render_template, request
from flask_wtf import CSRFProtect

from flask_bootstrap import Bootstrap5, SwitchField
from flask_sqlalchemy import SQLAlchemy
import waitress
import logging
from argparse import ArgumentParser


def process_args():
    parser = ArgumentParser()
    parser.add_argument('--port', default='6003')
    parser.add_argument('--db_url', default='sqlite:///test.db')
    args = parser.parse_args()
    return args


args = process_args()

app = Flask(__name__)
app.secret_key = 'dev'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = args.db_url

# set default button sytle and size, will be overwritten by macro parameters
app.config['BOOTSTRAP_BTN_STYLE'] = 'primary'
app.config['BOOTSTRAP_BTN_SIZE'] = 'sm'

# set default icon title of table actions
app.config['BOOTSTRAP_TABLE_VIEW_TITLE'] = 'Read'
app.config['BOOTSTRAP_TABLE_EDIT_TITLE'] = 'Update'
app.config['BOOTSTRAP_TABLE_DELETE_TITLE'] = 'Remove'
app.config['BOOTSTRAP_TABLE_NEW_TITLE'] = 'Create'

app.config.setdefault('BOOTSTRAP_SERVE_LOCAL', True)

bootstrap = Bootstrap5(app)
db = SQLAlchemy(app)
csrf = CSRFProtect(app)


class AirData(db.Model):
    __tablename__ = "air_data"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    time = db.Column(db.DateTime)
    CO2 = db.Column(db.Integer)
    CH2O = db.Column(db.Integer)
    TVOC = db.Column(db.Integer)
    PM2_5 = db.Column(db.Integer)
    PM10 = db.Column(db.Integer)
    Temperature = db.Column(db.Float)
    Humidity = db.Column(db.Float)
    fullname = db.Column(db.String)

    def __repr__(self):
        return "ID:%d, DateTime:%s, CO2: %d, CH2O:%d" % (self.id, self.time, self.CO2, self.CH2O)


@app.before_first_request
def before_first_request_func():
    db.session.commit()


@app.route('/')
def index():
    cur_time = datetime.datetime.now()
    data = AirData.query.filter(AirData.time >= cur_time - datetime.timedelta(hours=8)).order_by(
        db.asc(AirData.time)).filter(AirData.id % 8 == 0).all()
    names = ['CO2',
             'CH2O',
             'TVOC',
             'PM2.5',
             'PM10',
             'Temperature',
             'Humidity']
    Xs = [[] for i in names]
    Ys = [[] for i in names]
    for i, name in enumerate(names):
        if name == 'PM2.5':
            name = 'PM2_5'
        for j in range(len(data)):
            try:
                Ys[i].append(data[j].__getattribute__(name))
            except Exception as e:
                print(name, e)
            Xs[i].append('%s' % datetime.datetime.strptime(str(data[j].time).split('.')[0].strip(),
                                                           '%Y-%m-%d %H:%M:%S').strftime('%m-%d %H:%M'))

    return render_template('index.html',
                           names=names,
                           XVs=Xs,
                           YVs=Ys)


logger = logging.getLogger()
logger.setLevel(logging.NOTSET)


@app.before_request
def log_the_request():
    logger.info(" " + str(datetime.datetime.now()) + ", request from: " + str(request.remote_addr))


if __name__ == '__main__':
    waitress.serve(app, port=args.port, url_scheme='https')
