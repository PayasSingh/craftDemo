# TODO: add Response Status Codes
# TODO: add "Liabilities"
# TODO: split assets and liabilities into different ƒiles??
# TODO: input validation - can be done in the frontend too ? send 0 if null ??
# TODO: do error handling for missing user

from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
import json
import uuid
import sys

sys.path.insert(0, '/Users/payassingh/Desktop/net-worth-calculator/backend/helpers')

from totals import Totals
from convertCurrency import ConvertCurrency
from fileOperations import FileOperations

# Initializing flask app
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/-net-worth/users/<int:userId>/', methods=['PUT'])
@cross_origin()
def put_currency(userId: int):
  '''
  calculate values in new currency
  '''

  reqData = json.loads(request.data.decode('utf-8'))
  f = FileOperations()
  dataList = f.read_file()

  for userData in dataList:
    currUserId = userData.get('userId')
    if currUserId == userId:
      c = ConvertCurrency()
      updatedData = c.convert_currency(reqData, userData["currency"]["currencyCode"])
      updatedData["userId"] = userId
      dataList.remove(userData)
      userData = updatedData
      dataList.append(userData)

  with open('data.txt', 'r+') as f:
    f.seek(0)
    f.write(json.dumps(dataList, indent=2))

  response = jsonify(userData)

  response.headers.add("Access-Control-Allow-Origin", "*")
  response.headers.add("Access-Control-Allow-Methods", "PUT")
  response.headers.add("Access-Control-Allow-Headers", "Content-Type, Authorization")
  response.headers.add("Access-Control-Max-Age", "86400")
  response.headers.add("Access-Control-Allow-Private-Network", "true")

  return response

# TODO: currency exchange - probs don't need it here, post is only for new enteries
@app.route('/-net-worth/assets/', methods=['POST'])
def post_data():
  '''
  add new users to the data
  '''
  # create new user
  user = { "userId": uuid.uuid1().int }
  newData = json.loads(request.data.decode('utf-8'))
  newData.update(user)

  # calculate totals
  t = Totals()
  totalAssets = t.calculate_total_assets_or_liabilities(newData, "assets")
  newData["assets"]["totalAssets"] = totalAssets
  totalLiabilities = t.calculate_total_assets_or_liabilities(newData, "liabilities")
  newData["liabilities"]["totalLiabilities"] = totalLiabilities
  newData["netWorth"] = t.calculate_total_networth(totalAssets, totalLiabilities)

  f = FileOperations()
  dataList = f.read_file()
  dataList.append(newData)

  # add new user and their data to the data file
  with open('data.txt', 'r+') as f:
    f.seek(0)
    f.write(json.dumps(dataList, indent=2))

  response = jsonify(newData)
  response.headers.add("Access-Control-Allow-Origin", "*")
  return response

### Start of ASSETS

# route() tells Flask which URL should trigger this function
@app.route('/-net-worth/users/<int:userId>/assets/', methods=['GET'])
def get_assets(userId: int):
  '''
  return assets of the user with the provided userId
  '''
  f = FileOperations()
  dataList = f.read_file()

  for userData in dataList:
    currUserId = userData.get('userId')
    if currUserId == userId:
      response = jsonify(userData["assets"])
      response.headers.add("Access-Control-Allow-Origin", "*")
      return response

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

  for userData in dataList:
    currUserId = userData.get('userId')
    if currUserId == userId:
      # calculate total assets
      t = Totals()
      totalAssets = t.calculate_total_assets_or_liabilities(reqData, "assets")
      reqData["assets"]["totalAssets"] = totalAssets
      # calculate new net worth
      netWorth = t.calculate_total_networth(reqData["assets"]["totalAssets"],reqData["liabilities"]["totalLiabilities"])
      reqData["netWorth"] = netWorth
      # update the data
      dataList.remove(userData)
      dataList.append(reqData)

  # write the changes to the data file
  with open('data.txt', 'r+') as f:
    f.seek(0)
    f.write(json.dumps(dataList, indent=2))

  response = jsonify(reqData)

  response.headers.add("Access-Control-Allow-Origin", "*")
  response.headers.add("Access-Control-Allow-Methods", "PUT")
  response.headers.add("Access-Control-Allow-Headers", "Content-Type, Authorization")
  response.headers.add("Access-Control-Max-Age", "86400")
  response.headers.add("Access-Control-Allow-Private-Network", "true")

  return response

### End of Assets

### Start of LIABILITIES
@app.route('/-net-worth/users/<int:userId>/liabilities/', methods=['GET'])
def get_liabilities(userId: int):
  '''
  return assets of the user with the provided userId
  '''
  f = FileOperations()
  dataList = f.read_file()

  for userData in dataList:
    currUserId = userData.get('userId')
    if currUserId == userId:
      response = jsonify(userData["liabilities"])
      response.headers.add("Access-Control-Allow-Origin", "*")
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

  for userData in dataList:
    currUserId = userData.get('userId')
    if currUserId == userId:
      # calculate total liabilities
      t = Totals()
      totalLiabilities = t.calculate_total_assets_or_liabilities(reqData, "liabilities")
      reqData["liabilities"]["totalLiabilities"] = totalLiabilities
      # calculate new networth
      netWorth = t.calculate_total_networth(reqData["assets"]["totalAssets"],reqData["liabilities"]["totalLiabilities"])
      reqData["netWorth"] = netWorth
      # update the data
      dataList.remove(userData)
      dataList.append(reqData)

    # write the changes to the data file
  with open('data.txt', 'r+') as f:
    f.seek(0)
    f.write(json.dumps(dataList, indent=2))

  response = jsonify(reqData)

  response.headers.add("Access-Control-Allow-Origin", "*")
  response.headers.add("Access-Control-Allow-Methods", "PUT")
  response.headers.add("Access-Control-Allow-Headers", "Content-Type, Authorization")
  response.headers.add("Access-Control-Max-Age", "86400")
  response.headers.add("Access-Control-Allow-Private-Network", "true")

  return response

if __name__ == "__main__":
  # run() runs the app in a local server, DO NOT use in production code
  app.run(debug=True)


# @app.route('/-net-worth/assets/', methods=['POST'])
# def post_assets():
#   '''
#   add new users to the data
#   '''
#   # create new user
#   user = { "userId": uuid.uuid1().int }
#   newData = json.loads(request.data.decode('utf-8'))
#   newData.update(user)

#   # calculate total assets
#   t = Totals()
#   totalAssets = t.calculate_total_assets(newData)
#   newData["assets"]["totalAssets"] = totalAssets

#   f = FileOperations()
#   dataList = f.read_file()
#   dataList.append(newData)

#   # add new user and their data to the data file
#   with open('data.txt', 'r+') as f:
#     f.seek(0)
#     f.write(json.dumps(dataList, indent=2))

#   response = jsonify(newData)
#   response.headers.add("Access-Control-Allow-Origin", "*")
#   return response