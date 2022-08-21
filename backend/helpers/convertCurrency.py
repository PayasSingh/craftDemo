from forex_python.converter import CurrencyRates, CurrencyCodes

class ConvertCurrency:

  def convert_currency(self, data, oldCurrency):
    '''
    apply exchange rate to the currency
    '''
    typeOfData = ["assets", "liabilities"]
    newCurrency = data["currency"]["currencyCode"]
    c = CurrencyRates()
    rate = c.get_rate(oldCurrency, newCurrency)

    for i in typeOfData:
      fields = data[i]
      for field in fields:
        if field != "totalAssets" and field != "totalLiabilities":
          subField = fields[field]
          for key, item in subField.items():
            if item != " ":
              fields[field][key] = str(round(float(item) * rate,2))
        else:
          fields[field] = str(round(float(fields[field]) * rate,2))
    data["netWorth"] = str(round(float(data["netWorth"]) * rate,2))

    c = CurrencyCodes()
    data["currency"]["currencySymbol"] = c.get_symbol(newCurrency)

    return data