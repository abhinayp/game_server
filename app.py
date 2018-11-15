from flask import Flask, render_template,request,redirect,url_for # For flask implementation from bson import ObjectId # For ObjectId to work
from flask import jsonify
import json
from flask import Response
from bson import json_util
from pymongo import MongoClient
import os
from flask_cors import CORS, cross_origin
from models.user import User

app = Flask(__name__)

cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

title = "TODO sample application with Flask and MongoDB"
heading = "TODO Reminder with Flask and MongoDB"

client = MongoClient("mongodb://127.0.0.1:27017") #host uri
db = client.adventure_game #Select the database
users = db.users #Select the collection name


def redirect_url():
  return request.args.get('next') or \
  request.referrer or \
  url_for('index')

def newEncoder(o):
    if type(o) == ObjectId:
        return str(o)
    return o.__str__

@app.route("/")
@app.route("/users")
@cross_origin()
def tasks ():
  #Display the Uncompleted Tasks
  todos_l = users.find()
  return json_util.dumps(todos_l, default=lambda o: o.__dict__)

@app.route("/create_user", methods=['POST'])
def create_user():
  req = request.get_json(silent=True)
  user = User(req.get('name'), req.get('role'))
  resp = users.insert_one(user.__dict__)
  return json_util.dumps(resp, default=lambda o: o.__dict__)


# @app.route("/action3", methods=['POST'])

if __name__ == "__main__":
  app.run()
