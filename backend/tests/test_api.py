import unittest
from copy import deepcopy
import json
import sys, os

sys.path.insert(0, os.getcwd())
import server as app

sys.path.insert(-1, 'helpers/')
import fileOperations

BASE_URL = "http://127.0.0.1:5000/-net-worth/"
USER_ID = "15186823"

class ApiTest(unittest.TestCase):

  def setUp(self):
    self.app = app.app.test_client()
    self.app.testing = True
    self.jsonData = {
      "assets": {
        "cashAndInvestments": {
          "chequing": "2000",
          "savingsForTaxes": "4000",
          "rainyDayFund": "506",
          "savingsForFun": "5000",
          "savingsForTravel": "400",
          "savingsForPersonalDevelopment": "200",
          "investment1": "5000",
          "investment2": "60000",
          "investment3": "24000"
        },
        "longTermAssets": {
          "primaryHome": "455000",
          "secondHome": "1564321",
          "other": "0"
        },
        "totalAssets": "0"
        },
        "liabilities": {
          "shortTermLiabilities": {
            "creditCard1": "4342",
            "creditCard2": "322"
          },
          "longTermDebt": {
            "mortgage1": "250999",
            "mortgage2": "632634",
            "lineOfCredit": "10000",
            "investmentLoan": "10000"
          },
          "totalLiabilities": "0"
        },
        "currency": {
          "currencyCode": "CAD",
          "currencySymbol": "$"
        },
        "netWorth": "0",
        "userId": 24590375
      }
    f = fileOperations.FileOperations()
    self.dataList = f.read_file()

  # get_data
  def test_getData_validUser_shouldReturnUser(self):
    apiCall = BASE_URL + "users/" + USER_ID + "/"
    response = self.app.get(apiCall)
    data = json.loads(response.get_data())
    self.assertEqual(response.status_code, 200)

  def test_getData_invalidUser_shouldReturnError(self):
    apiCall = BASE_URL + "users/" + "2" + "/"
    response = self.app.get(apiCall)
    data = json.loads(response.get_data())
    self.assertEqual(response.status_code, 404)

  # post_data
  def test_postData_noUserId_shouldCreateNewUser(self):
    apiCall = BASE_URL

    del self.jsonData["userId"]
    response = self.app.post(apiCall,
      data=json.dumps(self.jsonData),
      content_type='application/json')
    data = json.loads(response.get_data())
    self.assertEqual(response.status_code, 200)

  def test_postData_noUserId_shouldCalculateTotals(self):
    apiCall = BASE_URL

    del self.jsonData["userId"]
    response = self.app.post(BASE_URL,
      data=json.dumps(self.jsonData),
      content_type='application/json')
    data = json.loads(response.get_data())
    self.assertEqual(data["assets"]["totalAssets"], "2120427.0")
    self.assertEqual(data["liabilities"]["totalLiabilities"], "908297.0")
    self.assertEqual(data["netWorth"], "1212130.0")

  def test_postData_withUser_shouldReturnError(self):
    apiCall = BASE_URL

    response = self.app.post(BASE_URL,
      data=json.dumps(self.jsonData),
      content_type='application/json')
    data = json.loads(response.get_data())
    self.assertEqual(response.status_code, 400)

  # put_assets
  def test_putAssets_validUser_shouldUpdateAssetsAndNetworth(self):
    apiCall = BASE_URL + "users/" + USER_ID + "/assets/"
    self.jsonData["assets"]["cashAndInvestments"]["investment2"] = '60567'
    response = self.app.put(apiCall,
      data=json.dumps(self.jsonData),
      content_type='application/json')
    data = json.loads(response.get_data())

    self.assertEqual(response.status_code, 200)
    self.assertEqual(data["assets"]["cashAndInvestments"]["investment2"], "60567")
    self.assertEqual(data["netWorth"], "1212697.0")

  def test_putAssets_invalidUser_shouldReturnError(self):
    apiCall = BASE_URL + "users/" + "2" + "/assets/"
    response = self.app.put(apiCall,
      data=json.dumps(self.jsonData),
      content_type='application/json')
    data = json.loads(response.get_data())
    self.assertEqual(response.status_code, 404)

  # put_liabilities
  def test_putLiabilities_validUser_shouldUpdateLiabilitiesAndNetworth(self):
    apiCall = BASE_URL + "users/" + USER_ID + "/liabilities/"
    self.jsonData["liabilities"]["longTermDebt"]["investmentLoan"] = "10050"
    response = self.app.put(apiCall,
      data=json.dumps(self.jsonData),
      content_type='application/json')
    data = json.loads(response.get_data())
    self.assertEqual(response.status_code, 200)
    self.assertEqual(data["liabilities"]["longTermDebt"]["investmentLoan"], "10050")
    self.assertEqual(data["liabilities"]["totalLiabilities"], "908347.0")

  def test_putLiabilities_invalidUser_shouldReturnError(self):
    apiCall = BASE_URL + "users/" + "2" + "/liabilities/"
    response = self.app.put(apiCall,
      data=json.dumps(self.jsonData),
      content_type='application/json')
    data = json.loads(response.get_data())
    self.assertEqual(response.status_code, 404)

  # put_currency
  def test_putCurrency_validUser_ReturnNewValues(self):
    apiCall = BASE_URL + "users/" + USER_ID + "/"
    self.jsonData["currency"]["currencyCode"] = "EUR"
    response = self.app.put(apiCall,
      data=json.dumps(self.jsonData),
      content_type='application/json')
    data = json.loads(response.get_data())
    self.assertEqual(response.status_code, 200)
    self.assertEqual(data["currency"]["currencySymbol"], "€")
    self.assertEqual(data["assets"]["cashAndInvestments"]["chequing"], "1,531.16")

  def test_putCurrency_invalidUser_shouldReturnError(self):
    apiCall = BASE_URL + "users/" + "2" + "/"
    response = self.app.put(apiCall,
      data=json.dumps(self.jsonData),
      content_type='application/json')
    data = json.loads(response.get_data())
    self.assertEqual(response.status_code, 404)

  def tearDown(self):
    # reset data.txt to it's initial state
    f = fileOperations.FileOperations()
    f.write_file(self.dataList)

if __name__ == '__main__':
  unittest.main()