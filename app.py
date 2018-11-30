from flask import Flask, render_template,request,redirect,url_for # For flask implementation from bson import ObjectId # For ObjectId to work
from flask import jsonify
from flask import Response
from flask_login import LoginManager, login_user, logout_user , current_user , login_required

import json
from bson import json_util
from bson.objectid import ObjectId
import uuid
import base64
import random

from pymongo import MongoClient
import os

from flask_cors import CORS, cross_origin

from models.user import User
from models.trap import Trap
from models.game import Game
from models.riddle import Riddle

app = Flask(__name__)

cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['SECRET_KEY'] = 'info6250'
login_manager = LoginManager()
login_manager.init_app(app)

title = "TODO sample application with Flask and MongoDB"
heading = "TODO Reminder with Flask and MongoDB"

client = MongoClient("mongodb://127.0.0.1:27017") #host uri
db = client.adventure_game #Select the database
users = db.users #Select the collection name
traps = db.traps
detraps = db.detraps
games = db.games
riddles = db.riddles
game = 0

@login_manager.user_loader
def load_user(user_id):
    return User.get(db.users, user_id)

def redirect_url():
  return request.args.get('next') or \
  request.referrer or \
  url_for('index')

def newEncoder(o):
    if type(o) == ObjectId:
        return str(o)
    return o.__str__

# ------------------- USERS -----------------------

@app.route("/")
@app.route("/users")
@cross_origin()
def get_all_users ():
  #Display the Uncompleted Tasks
  todos_l = users.find()
  return json_util.dumps(todos_l, default=lambda o: o.__dict__)

@app.route("/create_user", methods=['POST'])
def create_user():
  req = request.get_json(silent=True)
  role = role_decider()
  api_token = uuid.uuid4().hex
  user = User(req.get('name'), 'hero', api_token)
  resp = users.insert_one(user.__dict__)
  user_id = resp.inserted_id
  u = User.get(users, user_id)
  login_user(u)
  createGame()
  generate_traps_grid()
  return redirect(f"/users/{user_id}")

@app.route("/users/<id>")
@cross_origin()
def get_user(id):
  user = users.find_one({"_id": ObjectId(id)})
  u = User.get(users, str(user.get('_id')))
  return json_util.dumps(u.__dict__, default=lambda o: o.__dict__)


# ------------------- TRAPS -----------------------

@app.route("/traps")
@cross_origin()
@login_required
def get_all_traps ():
  #Display the Uncompleted Tasks
  traps_result = traps.find({'game.user.id': current_user.id})
  return json_util.dumps(traps_result, default=lambda o: o.__dict__)

@app.route("/traps/<role>")
@cross_origin()
@login_required
def get_role_traps (role):
  #Display the Uncompleted Tasks
  traps_result = traps.find({'user.role': role, 'game.user.id': current_user.id})
  return json_util.dumps(traps_result, default=lambda o: o.__dict__)

@app.route("/create_trap", methods=['POST'])
@login_required
def create_trap():
  req = request.get_json(silent=True)

  trap = Trap(req.get('x'), req.get('y'), current_user)
  resp = traps.insert_one(trap.__dict__)
  trap_id = resp.inserted_id
  return redirect(f"/traps/{trap_id}")

@app.route("/create_multiple_traps", methods=['POST'])
@login_required
def create_multiple_traps():
  req = request.get_json(silent=True)
  traps_req = req.get('traps')
  trap_array = []

  for t in traps_req:
      trap = Trap(req.get('x'), req.get('y'), current_user)
      trap_array.append(trap.__dict__)

  resp = traps.insert_many(trap_array)
  return redirect("/traps")

@app.route("/traps/<id>")
def get_trap(id):
  trap = traps.find_one({"_id": ObjectId(id)})
  return json_util.dumps(trap, default=lambda o: o.__dict__)

def removeTraps(game_id):
  traps.delete_many({'game._id': game_id})


# ------------------- DETRAPS -----------------------

@app.route("/detraps/<role>")
@cross_origin()
@login_required
def get_role_detraps (role):
  #Display the Uncompleted Tasks
  traps_result = detraps.find({'game.user.id': current_user.id})
  return json_util.dumps(traps_result, default=lambda o: o.__dict__)

@app.route("/create_detrap", methods=['POST'])
@login_required
def create_detrap():
  req = request.get_json(silent=True)

  trap = Trap(req.get('x'), req.get('y'), current_user, getGame(current_user.id))
  resp = detraps.insert_one(trap.__dict__)
  trap_id = resp.inserted_id
  return redirect(f"/detraps/{trap_id}")

@app.route("/detraps/<id>")
def get_detrap(id):
  trap = detraps.find_one({"_id": ObjectId(id)})
  return json_util.dumps(trap, default=lambda o: o.__dict__)

def removeDetraps(game_id):
  detraps.delete_many({'game._id': game_id})


# ------------------- GAME ---------------------------------

@app.route("/finish_game", methods=['POST'])
@login_required
def finish_game():
  g = getGame(current_user.id)
  removeGame(current_user.id)
  removeTraps(g.get('_id'))
  removeDetraps(g.get('_id'))
  return json_util.dumps({'status': True})

@app.route("/generate_game", methods=['POST'])
@login_required
def generate_game():

  riddlesTypes = Riddle.riddleTypes()
  riddle_random = random.choice(riddlesTypes)

  createGame(riddle_random)
  generate_traps_grid(riddle_random)
  return json_util.dumps({'status': True})

def createGame(answer):
    global game
    game += 1
    g = Game(game, current_user, answer)
    games.insert_one(g.__dict__)

def getGame(id):
    g = games.find_one({"user.id": id})
    return g

def removeGame(id):
    g = games.delete_one({"user.id": id})

def removeAllGame():
    g = games.delete_many({})


# ---------------------- RIDDLES ---------------------------

def createRiddle(answer):
  riddle = {}
  rQuestions = Riddle.riddleQuestions()
  if rQuestions.get(answer) is not None:
    riddle['answer'] = answer
    riddle['question'] = rQuestions.get(answer)
    g = riddles.insert_one(riddle)

def createRiddles():
  riddleTypes = Riddle.riddleTypes()
  for rType in riddleTypes:
    createRiddle(rType)

def removeAllRiddles():
  riddles.delete_many({})


# ------------------- AUTHENTICATION -----------------------

@app.route("/login", methods=['POST'])
def login():
  req = request.get_json(silent=True)
  id = req.get('user_id')
  user1 = User.get(users, id)
  login_user(user1)
  return json_util.dumps(user1.__dict__, default=lambda o: o.__dict__)

@app.route("/login/api_token", methods=['POST'])
def login_api_token():
  req = request.get_json(silent=True)
  api_token = req.get('api_token')
  user1 = User.get_by_api_token(users, api_token)
  if user1 is not None:
      login_user(user1)
  return json_util.dumps(current_user.__dict__, default=lambda o: o.__dict__)

@app.route("/logout", methods=['POST'])
def logout():
  logout_user()
  return {'status': true}

@login_manager.header_loader
def load_user_from_header(header_val):
    header_val = header_val.replace('Basic ', '', 1)
    u = User.get_by_api_token(users, header_val)
    return u


def role_decider():
  roles = ['hero', 'villian']
  role = random.choice(roles)

  h = list(users.find({'role': 'hero'}))
  hero_role = len(h)

  v = list(users.find({'role': 'villian'}))
  villian_role = len(v)

  if hero_role < villian_role:
      return 'hero'
  elif villian_role < hero_role:
      return 'villian'

  return role

def getQuadrants():
  quadrants = []
  max_x = 16
  max_y = 16

  for q_x in range(1, 3):
    for q_y in range(1, 3):
      qx_start = max_x*(q_x-1)/2
      qx_end = max_x*(q_x)/2

      qy_start = max_y*(q_y-1)/2
      qy_end = max_y*(q_y)/2

      q = {'x': {'min': qx_start, 'max': qx_end}, 'y': {'min': qy_start, 'max': qy_end}}
      quadrants.append(q)

  return quadrants

def generate_traps_grid(answer):
    quadrants = getQuadrants()
    riddleQuestions = Riddle.riddleQuestions()

    total = random.randint(1, 5)

    for index, q in enumerate(quadrants):
      x_start = q.get('x').get('min')
      x_end = q.get('x').get('max')
      y_start = q.get('y').get('min')
      y_end = q.get('y').get('max')

      for i in range(0, total):
        x = random.randint(x_start, x_end)
        y = random.randint(y_start, y_end)

        traps_result = list(traps.find({'user.role': 'villian'}))
        trap_created = list(filter(lambda x: (x.get('x') == x and x.get('y') == y) , traps_result))
        if len(trap_created) < 1:
          r_riddle = riddleQuestions.get(answer)[index]
          trap = Trap(x, y, User.get(users, '5bee0c3ae93f73258b1d49f7'), getGame(current_user.id), r_riddle)
          resp = traps.insert_one(trap.__dict__)

def deleteAllTraps():
    traps.delete_many({})
    detraps.delete_many({})

deleteAllTraps()
removeAllGame()

removeAllRiddles()
createRiddles()


if __name__ == "__main__":
  app.run()
