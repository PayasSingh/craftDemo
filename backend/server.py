
from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
import json
import uuid
import sys, os

sys.path.insert(0, os.getcwd() +'/helpers')
import os

from totals import Totals
from convertCurrency import ConvertCurrency
from fileOperations import FileOperations

# Initializing flask app
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

def create_response(data):
    response = jsonify(data)
    # response.headers.add("Access-Control-Allow-Origin", "*")
    return response

# APIs
@app.route('/-net-worth/users/<int:userId>/', methods=['GET'])
def get_data(userId: int):
  '''
  GET: returns data of user with the given user id
  '''
  f = FileOperations()
  dataList = f.read_file()

  for userData in dataList:
    currUserId = userData.get('userId')
    if currUserId == userId:
      response = create_response(userData)
      return response, 200

  # if no user was found, return error
  error = {}
  error["errorMsg"] = "User Not Found"
  return jsonify(error), 404

@app.route('/-net-worth/', methods=['POST'])
def post_data():
  '''
  POST : add new users to the data
  automatically creates a new UID for a new user
  automatically calculates totals
  '''
  newData = json.loads(request.data.decode('utf-8'))

  if "userId" in newData:
    error = {}
    error["errorMsg"] = "Incorrect data: POST request cannot have a user ID"
    return jsonify(error), 400

  # create new user
  user = { "userId": int(str(uuid.uuid1().int)[:8])}
  newData.update(user)

  # calculate totals
  t = Totals()
  totalAssets = t.calculate_total_assets_or_liabilities(newData, "assets")
  newData["assets"]["totalAssets"] = totalAssets
  totalLiabilities = t.calculate_total_assets_or_liabilities(newData, "liabilities")
  newData["liabilities"]["totalLiabilities"] = totalLiabilities
  newData["netWorth"] = t.calculate_total_networth(totalAssets, totalLiabilities, newData["currency"]["currencyCode"])

  f = FileOperations()
  dataList = f.read_file()
  dataList.append(newData)

  # add new user and their data to the data file
  with open('data.txt', 'r+') as f:
    f.seek(0)
    f.write(json.dumps(dataList, indent=2))
    f.truncate()

  response = create_response(newData)
  return response, 200

@app.route('/-net-worth/users/<int:userId>/', methods=['PUT'])
@cross_origin()
def put_currency(userId: int):
  '''
  PUT: calculates values of all input fields in the new currency value
  '''
  reqData = json.loads(request.data.decode('utf-8'))
  f = FileOperations()
  dataList = f.read_file()

  userFound = False
  for userData in dataList:
    currUserId = userData.get('userId')
    if currUserId == userId:
      userFound = True
      c = ConvertCurrency()
      updatedData = c.convert_currency(reqData, userData["currency"]["currencyCode"])
      updatedData["userId"] = userId
      dataList.remove(userData)
      userData = updatedData
      dataList.append(userData)
      break

  if not userFound:
    error = {}
    error["errorMsg"] = "User Not Found"
    return jsonify(error), 404

  with open('data.txt', 'r+') as f:
    f.seek(0)
    f.write(json.dumps(dataList, indent=2))
    f.truncate()

  response = create_response(userData)
  return response, 200


@app.route('/-net-worth/users/<int:userId>/assets/', methods=['PUT'])
@cross_origin()
def put_assets(userId: int):
  '''
  update assets to reflect user changes and
  update asset totals
  '''
  reqData = json.loads(request.data.decode('utf-8'))
  f = FileOperations()
  dataList = f.read_file()

  # check JSON data
  if (not reqData["assets"]):
    response = create_response(reqData)
    return response, 400

  userFound = False
  for userData in dataList:
    currUserId = userData.get('userId')
    if currUserId == userId:
      userFound = True
      # calculate total assets
      t = Totals()
      totalAssets = t.calculate_total_assets_or_liabilities(reqData, "assets")
      reqData["assets"]["totalAssets"] = totalAssets
      # calculate new net worth
      netWorth = t.calculate_total_networth(reqData["assets"]["totalAssets"],userData["liabilities"]["totalLiabilities"], reqData["currency"]["currencyCode"])
      reqData["netWorth"] = netWorth
      reqData["liabilities"] = userData["liabilities"]
      # update the data
      dataList.remove(userData)
      dataList.append(reqData)
      break

  # return error if user not found
  if not userFound:
    error = {}
    error["errorMsg"] = "User Not Found"
    return jsonify(error), 404

  # write the changes to the data file
  with open('data.txt', 'r+') as f:
    f.seek(0)
    f.write(json.dumps(dataList, indent=2))
    f.truncate()

  response = create_response(reqData)
  return response


@app.route('/-net-worth/users/<int:userId>/liabilities/', methods=['PUT'])
@cross_origin()
def put_liabilities(userId: int):
  '''
  update liabilities to reflect user changes and
  update liabilities totals
  '''
  reqData = json.loads(request.data.decode('utf-8'))
  f = FileOperations()
  dataList = f.read_file()

    # check JSON data
  if (not reqData["liabilities"]):
    response = create_response(reqData)
    return response, 400

  userFound =  False
  for userData in dataList:
    currUserId = userData.get('userId')
    if currUserId == userId:
      # calculate total liabilities
      userFound = True
      t = Totals()
      totalLiabilities = t.calculate_total_assets_or_liabilities(reqData, "liabilities")
      reqData["liabilities"]["totalLiabilities"] = totalLiabilities
      # calculate new networth
      netWorth = t.calculate_total_networth(userData["assets"]["totalAssets"],reqData["liabilities"]["totalLiabilities"], reqData["currency"]["currencyCode"])
      reqData["netWorth"] = netWorth
      reqData["assets"] = userData["assets"]
      # update the data
      dataList.remove(userData)
      dataList.append(reqData)
      break

  # return error if user not found
  if not userFound:
    error = {}
    error["errorMsg"] = "User Not Found"
    return jsonify(error), 404

    # write the changes to the data file
  with open('data.txt', 'r+') as f:
    f.seek(0)
    f.write(json.dumps(dataList, indent=2))
    f.truncate()

  response = create_response(reqData)
  return response, 200

if __name__ == "__main__":
  # run() runs the app in a local server, DO NOT use in production code
  app.run(debug=True)

