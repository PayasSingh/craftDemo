from forex_python.converter import CurrencyRates, CurrencyCodes
import babel.numbers
import decimal
import datetime
import re

class ConvertCurrency:

  def format_currency(self, amount, newCurrency):
    formattedNumber = babel.numbers.format_currency(decimal.Decimal(amount), newCurrency)
    formattedNumber = re.sub('[^0-9|\.|\+|\-|,]', '', formattedNumber)
    return formattedNumber

  def convert_currency(self, data, oldCurrency):
    '''
    apply exchange rate to the currency
    '''
    newCurrency = data["currency"]["currencyCode"]

    # specify date time for currency exchnage - prevent upstream error
    dateObj = datetime.datetime(2022, 8, 22, 18, 50, 28, 151012)
    c = CurrencyCodes()
    newSymbol = c.get_symbol(newCurrency)
    data["currency"]["currencySymbol"] = newSymbol

    typeOfData = ["assets", "liabilities"]
    c = CurrencyRates()
    rate = c.get_rate(oldCurrency, newCurrency, dateObj)

    for i in typeOfData:
      fields = data[i]
      for field in fields:
        if field != "totalAssets" and field != "totalLiabilities":
          subField = fields[field]
          for key, item in subField.items():
            if item != " ":
              convertedNumber = round(float(item) * rate,2)
              formattedCurrency = self.format_currency(convertedNumber, newCurrency)
              fields[field][key] = str(formattedCurrency)
        else:
          convertedNumber = round(float(fields[field]) * rate,2)
          formattedCurrency = self.format_currency(convertedNumber, newCurrency)
          fields[field] = str(formattedCurrency)

    convertedNumber = round(float(data["netWorth"]) * rate,2)
    formattedCurrency = self.format_currency(convertedNumber, newCurrency)
    data["netWorth"] = str(formattedCurrency)


    return data