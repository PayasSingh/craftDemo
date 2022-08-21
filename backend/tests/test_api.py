import unittest
from copy import deepcopy
import sys
import json

sys.path.insert(0, '/Users/payassingh/Desktop/net-worth-calculator/backend/')

import server as app


class ApiTest(unittest.TestCase):

  def setUp(self):
    self.app = app.app.test_client()
    self.app.testing = True
    self.jsonAssets = {
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
        }
    }
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

  # get_data
  def test_getData_validUser_shouldReturnUser(self):
    response = self.app.get("http://127.0.0.1:5000/-net-worth/users/24590375/")
    data = json.loads(response.get_data())
    self.assertEqual(response.status_code, 200)

  def test_getData_invalidUser_shouldReturnError(self):
    response = self.app.get("http://127.0.0.1:5000/-net-worth/users/2/")
    data = json.loads(response.get_data())
    self.assertEqual(response.status_code, 404)

  # post_data
  def test_postData_noUserId_shouldCreateNewUser(self):
    del self.jsonData["userId"]
    response = self.app.post("http://127.0.0.1:5000/-net-worth/",
      data=json.dumps(self.jsonData),
      content_type='application/json')
    data = json.loads(response.get_data())
    self.assertEqual(response.status_code, 200)

  def test_postData_noUserId_shouldCalculateTotals(self):
    del self.jsonData["userId"]
    response = self.app.post("http://127.0.0.1:5000/-net-worth/",
      data=json.dumps(self.jsonData),
      content_type='application/json')
    data = json.loads(response.get_data())
    self.assertEqual(data["assets"]["totalAssets"], "2120427.0")
    self.assertEqual(data["liabilities"]["totalLiabilities"], "908297.0")
    self.assertEqual(data["netWorth"], "1212130.0")

  def test_postData_withUser_shouldReturnError(self):
    response = self.app.post("http://127.0.0.1:5000/-net-worth/",
      data=json.dumps(self.jsonData),
      content_type='application/json')
    data = json.loads(response.get_data())
    self.assertEqual(response.status_code, 400)

  # put_assets
  def test_putAssets_validUser_shouldUpdateTotalAssetsAndNetworth(self):
    self.jsonAssets["assets"]["cashAndInvestments"]["investment2"] = '60567'
    response = self.app.put("http://127.0.0.1:5000/-net-worth/users/24590375/assets/",
      data=json.dumps(self.jsonAssets),
      content_type='application/json')
    data = json.loads(response.get_data())
    print(data)
    self.assertEqual(data["assets"]["totalAssets"], "2120994.0")
    self.assertEqual(data["netWorth"], "1212697.0")


if __name__ == '__main__':
  unittest.main()